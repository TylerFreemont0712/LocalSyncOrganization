"""LAN mesh sync engine — subnet scanning, peer discovery, and data exchange.

How it works:
1. DISCOVERY: On each cycle, actively scans the local /24 subnet by attempting
   a fast TCP connect to the sync port on every host. Also listens for UDP
   broadcast announcements from other instances. This two-pronged approach
   means peers find each other automatically on the LAN.

2. SYNC: For each discovered peer, opens a TCP connection, exchanges full data
   sets (events, transactions, notes), and merges using last-write-wins on
   the updated_at timestamp. Soft-deleted records are propagated.

3. MESH: Every node is both client and server. There's no central coordinator.
   Any two nodes that can reach each other will converge.

Designed for your setup:
  Desktop (Windows) 192.168.0.4  <-->  Laptop (Linux) 192.168.0.28
  Both on the same 192.168.0.0/24 subnet.
"""

import json
import logging
import socket
import struct
import threading
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path, PurePosixPath

from PyQt6.QtCore import QThread, pyqtSignal

from src.config import load_config, NOTES_DIR
from src.data.database import get_connection
from src.utils.timestamps import now_utc

logger = logging.getLogger(__name__)

SYNC_MAGIC = b"LSYNC2"
PROTOCOL_VERSION = 2


class PeerInfo:
    """Tracks a discovered peer and its health."""

    def __init__(self, ip: str, port: int):
        self.ip = ip
        self.port = port
        self.last_seen: float = time.time()
        self.last_sync: float = 0
        self.fail_count: int = 0
        self.hostname: str = ""

    @property
    def is_stale(self) -> bool:
        return time.time() - self.last_seen > 600  # 10 min without contact

    def __repr__(self):
        return f"Peer({self.ip}:{self.port})"


class SyncEngine(QThread):
    """Background mesh sync thread."""

    # Signals for the UI
    status_changed = pyqtSignal(str)          # Human-readable status
    sync_completed = pyqtSignal()             # Fired after a successful sync cycle
    peer_discovered = pyqtSignal(str)         # IP of a newly found peer
    peer_lost = pyqtSignal(str)               # IP of a peer that went stale
    peers_updated = pyqtSignal(list)          # Full peer list [{"ip":..., "status":...}, ...]
    sync_log = pyqtSignal(str)                # Detailed log line for the network panel

    def __init__(self, parent=None):
        super().__init__(parent)
        self.cfg = load_config()
        self.sync_port: int = self.cfg.get("sync_port", 42069)
        self.discovery_port: int = self.cfg.get("discovery_port", 42070)
        self.interval: int = self.cfg.get("sync_interval_seconds", 300)
        self.subnet: str = self.cfg.get("subnet", "192.168.0")
        self.scan_start: int = self.cfg.get("scan_range_start", 1)
        self.scan_end: int = self.cfg.get("scan_range_end", 254)
        self.scan_threads: int = self.cfg.get("scan_threads", 20)
        self.scan_timeout: float = self.cfg.get("scan_timeout_ms", 150) / 1000.0

        self._running = True
        self._peers: dict[str, PeerInfo] = {}  # ip -> PeerInfo
        self._lock = threading.Lock()

        # Seed known peers from config
        for ip in self.cfg.get("known_peers", []):
            self._peers[ip] = PeerInfo(ip, self.sync_port)

    # ── Main loop ──────────────────────────────────────

    def run(self):
        # Start background listeners
        threading.Thread(target=self._discovery_listener, daemon=True).start()
        threading.Thread(target=self._sync_server, daemon=True).start()

        self._log("Sync engine started")
        self._log(f"Scanning subnet {self.subnet}.0/24 on port {self.sync_port}")
        self._log(f"Sync interval: {self.interval}s")

        while self._running:
            try:
                # Phase 1: Discover peers
                self.status_changed.emit("scanning...")
                self._broadcast_presence()
                self._scan_subnet()
                self._prune_stale_peers()
                self._emit_peer_list()

                # Phase 2: Sync with each peer
                alive_peers = self._get_alive_peers()
                if alive_peers:
                    self.status_changed.emit(f"syncing with {len(alive_peers)} peer(s)...")
                    synced = 0
                    for peer in alive_peers:
                        try:
                            self._sync_with_peer(peer)
                            peer.last_sync = time.time()
                            peer.fail_count = 0
                            synced += 1
                            self._log(f"Synced with {peer.ip}")
                        except Exception as e:
                            peer.fail_count += 1
                            self._log(f"Sync failed with {peer.ip}: {e}")
                            logger.warning(f"Sync with {peer.ip} failed: {e}")

                    self.status_changed.emit(
                        f"synced ({synced}/{len(alive_peers)} peers)"
                    )
                    self.sync_completed.emit()
                else:
                    self.status_changed.emit("no peers on network")
                    self._log("No peers found this cycle")

            except Exception as e:
                logger.error(f"Sync loop error: {e}")
                self.status_changed.emit(f"error: {e}")
                self._log(f"ERROR: {e}")

            # Interruptible sleep
            for _ in range(self.interval):
                if not self._running:
                    break
                time.sleep(1)

        self._log("Sync engine stopped")

    def stop(self):
        self._running = False

    def force_sync(self):
        """Trigger an immediate sync cycle (called from UI)."""
        # Just interrupt the sleep by setting a flag — next iteration runs immediately
        # We achieve this by starting a one-shot thread
        threading.Thread(target=self._force_sync_once, daemon=True).start()

    def _force_sync_once(self):
        self.status_changed.emit("force syncing...")
        self._broadcast_presence()
        self._scan_subnet()
        for peer in self._get_alive_peers():
            try:
                self._sync_with_peer(peer)
                peer.last_sync = time.time()
                peer.fail_count = 0
                self._log(f"Force-synced with {peer.ip}")
            except Exception as e:
                self._log(f"Force-sync failed with {peer.ip}: {e}")
        self._emit_peer_list()
        self.status_changed.emit("idle")
        self.sync_completed.emit()

    def trigger_vault_sync(self):
        """Called by the vault watcher when local vault files changed.

        Immediately syncs with all known peers so the changes propagate.
        """
        threading.Thread(target=self._vault_sync_once, daemon=True).start()

    def _vault_sync_once(self):
        self._log("Vault change detected — pushing to peers")
        self.status_changed.emit("vault changed, syncing...")
        peers = self._get_alive_peers()
        synced = 0
        for peer in peers:
            try:
                self._sync_with_peer(peer)
                peer.last_sync = time.time()
                peer.fail_count = 0
                synced += 1
                self._log(f"Vault sync pushed to {peer.ip}")
            except Exception as e:
                peer.fail_count += 1
                self._log(f"Vault sync to {peer.ip} failed: {e}")
        if synced:
            self.status_changed.emit(f"vault synced ({synced} peer{'s' if synced != 1 else ''})")
        else:
            self.status_changed.emit("vault changed (no peers)")
        self.sync_completed.emit()

    def add_manual_peer(self, ip: str):
        """Add a peer IP manually (from the network settings dialog)."""
        with self._lock:
            if ip not in self._peers:
                self._peers[ip] = PeerInfo(ip, self.sync_port)
                self._log(f"Manually added peer: {ip}")
                self.peer_discovered.emit(ip)
        self._emit_peer_list()

    def reload_config(self):
        """Reload config after settings change."""
        self.cfg = load_config()
        self.subnet = self.cfg.get("subnet", "192.168.0")
        self.interval = self.cfg.get("sync_interval_seconds", 300)
        self.sync_port = self.cfg.get("sync_port", 42069)
        self.scan_timeout = self.cfg.get("scan_timeout_ms", 150) / 1000.0
        self._log(f"Config reloaded — subnet={self.subnet}, interval={self.interval}s")

    # ── Subnet scanning ────────────────────────────────

    def _scan_subnet(self):
        """Actively probe every host in the /24 subnet for our sync port."""
        my_ips = self._get_local_ips()
        targets = [
            f"{self.subnet}.{i}"
            for i in range(self.scan_start, self.scan_end + 1)
            if f"{self.subnet}.{i}" not in my_ips
        ]

        found = []
        with ThreadPoolExecutor(max_workers=self.scan_threads) as pool:
            futures = {
                pool.submit(self._probe_host, ip): ip
                for ip in targets
            }
            for future in as_completed(futures):
                ip = futures[future]
                try:
                    if future.result():
                        found.append(ip)
                except Exception:
                    pass

        with self._lock:
            for ip in found:
                if ip not in self._peers:
                    self._peers[ip] = PeerInfo(ip, self.sync_port)
                    self._log(f"Discovered peer: {ip}")
                    self.peer_discovered.emit(ip)
                else:
                    self._peers[ip].last_seen = time.time()

    def _probe_host(self, ip: str) -> bool:
        """Try a fast TCP connect to see if a peer is listening on sync_port."""
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(self.scan_timeout)
            result = sock.connect_ex((ip, self.sync_port))
            sock.close()
            return result == 0
        except Exception:
            return False

    # ── UDP broadcast discovery (supplement to scanning) ──

    def _broadcast_presence(self):
        """Announce ourselves on the LAN via UDP broadcast."""
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
            sock.settimeout(1)
            hostname = socket.gethostname()[:32]
            payload = (
                SYNC_MAGIC
                + struct.pack("!HB", self.sync_port, PROTOCOL_VERSION)
                + hostname.encode("utf-8")
            )
            sock.sendto(payload, ("<broadcast>", self.discovery_port))
            sock.close()
        except Exception as e:
            logger.debug(f"Broadcast failed: {e}")

    def _discovery_listener(self):
        """Listen for UDP peer announcements."""
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            sock.bind(("", self.discovery_port))
            sock.settimeout(5)
        except Exception as e:
            logger.error(f"Discovery listener bind failed: {e}")
            self._log(f"Discovery listener failed: {e}")
            return

        my_ips = self._get_local_ips()
        while self._running:
            try:
                data, addr = sock.recvfrom(1024)
                if len(data) >= 9 and data[:6] == SYNC_MAGIC and addr[0] not in my_ips:
                    peer_port = struct.unpack("!H", data[6:8])[0]
                    _version = data[8]
                    hostname = data[9:].decode("utf-8", errors="replace")
                    ip = addr[0]
                    with self._lock:
                        if ip not in self._peers:
                            self._peers[ip] = PeerInfo(ip, peer_port)
                            self._log(f"Broadcast discovery: {ip} ({hostname})")
                            self.peer_discovered.emit(ip)
                        self._peers[ip].last_seen = time.time()
                        self._peers[ip].hostname = hostname
            except socket.timeout:
                continue
            except Exception as e:
                logger.debug(f"Discovery error: {e}")

    # ── Sync server (accept incoming connections) ──────

    def _sync_server(self):
        """TCP server that accepts sync requests from peers."""
        try:
            server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            server.bind(("0.0.0.0", self.sync_port))
            server.listen(5)
            server.settimeout(5)
            self._log(f"Sync server listening on port {self.sync_port}")
        except Exception as e:
            logger.error(f"Sync server bind failed: {e}")
            self._log(f"FAILED to bind sync server on port {self.sync_port}: {e}")
            return

        while self._running:
            try:
                conn, addr = server.accept()
                threading.Thread(
                    target=self._handle_incoming, args=(conn, addr), daemon=True
                ).start()
            except socket.timeout:
                continue
            except Exception as e:
                logger.debug(f"Server accept error: {e}")

    def _handle_incoming(self, conn: socket.socket, addr: tuple):
        """Handle an incoming sync connection from a peer."""
        peer_ip = addr[0]
        try:
            msg = self._recv_json(conn)
            if not msg:
                return
            if msg.get("type") == "sync_request" and msg.get("version") == PROTOCOL_VERSION:
                # Register this peer if unknown
                with self._lock:
                    if peer_ip not in self._peers:
                        self._peers[peer_ip] = PeerInfo(peer_ip, self.sync_port)
                        self.peer_discovered.emit(peer_ip)
                    self._peers[peer_ip].last_seen = time.time()

                # Send our data back
                our_data = self._gather_local_data()
                self._send_json(conn, {
                    "type": "sync_response",
                    "version": PROTOCOL_VERSION,
                    "data": our_data,
                })
                # Merge their data into ours
                their_data = msg.get("data", {})
                changes = self._merge_remote_data(their_data)
                if changes:
                    self._log(f"Received {changes} change(s) from {peer_ip}")
                self.sync_completed.emit()
            elif msg.get("type") == "ping":
                self._send_json(conn, {"type": "pong", "hostname": socket.gethostname()})
        except Exception as e:
            logger.warning(f"Incoming sync error from {peer_ip}: {e}")
        finally:
            conn.close()

    # ── Sync client (outbound to a peer) ───────────────

    def _sync_with_peer(self, peer: PeerInfo):
        """Initiate a sync exchange with a specific peer."""
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(15)
        try:
            sock.connect((peer.ip, peer.port))
            our_data = self._gather_local_data()
            self._send_json(sock, {
                "type": "sync_request",
                "version": PROTOCOL_VERSION,
                "data": our_data,
            })
            response = self._recv_json(sock)
            if response and response.get("type") == "sync_response":
                changes = self._merge_remote_data(response.get("data", {}))
                if changes:
                    self._log(f"Merged {changes} change(s) from {peer.ip}")
        finally:
            sock.close()

    def ping_peer(self, ip: str) -> tuple[bool, str]:
        """Ping a specific peer. Returns (reachable, hostname_or_error)."""
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(2)
            sock.connect((ip, self.sync_port))
            self._send_json(sock, {"type": "ping"})
            resp = self._recv_json(sock)
            sock.close()
            if resp and resp.get("type") == "pong":
                return True, resp.get("hostname", ip)
            return True, ip
        except Exception as e:
            return False, str(e)

    # ── Data gathering & merging ───────────────────────

    def _gather_local_data(self) -> dict:
        conn = get_connection()
        try:
            events = [dict(r) for r in conn.execute("SELECT * FROM events").fetchall()]
            transactions = [dict(r) for r in conn.execute("SELECT * FROM transactions").fetchall()]
            todos = [dict(r) for r in conn.execute("SELECT * FROM todos").fetchall()]
        finally:
            conn.close()

        cfg = load_config()

        # Gather notes from configured notes dir (built-in notes)
        notes = []
        notes_dir = Path(cfg.get("notes_dir", str(NOTES_DIR)))
        if notes_dir.exists():
            for md in notes_dir.rglob("*.md"):
                rel = md.relative_to(notes_dir)
                if any(part.startswith(".") for part in rel.parts):
                    continue
                # Always use forward slashes for cross-platform compatibility
                rel_posix = str(PurePosixPath(rel))
                try:
                    mtime = md.stat().st_mtime
                    content = md.read_text(encoding="utf-8")
                    notes.append({"path": rel_posix, "mtime": mtime, "content": content})
                except OSError:
                    pass

        # Gather Obsidian vault files if configured
        vault_notes = []
        vault_existing_paths = set()  # track what exists for deletion manifest
        vault_path = cfg.get("obsidian_vault_path", "")
        if vault_path:
            vault_dir = Path(vault_path)
            if vault_dir.exists():
                for md in vault_dir.rglob("*.md"):
                    rel = md.relative_to(vault_dir)
                    # Skip hidden dirs (.obsidian, .trash, etc.)
                    if any(p.startswith(".") for p in rel.parts):
                        continue
                    # Always use forward slashes for cross-platform compatibility
                    rel_posix = str(PurePosixPath(rel))
                    vault_existing_paths.add(rel_posix)
                    try:
                        mtime = md.stat().st_mtime
                        content = md.read_text(encoding="utf-8")
                        vault_notes.append({"path": rel_posix, "mtime": mtime, "content": content})
                    except OSError:
                        pass

        # Build deletion manifest — files we know were deleted locally
        vault_deletions = self._get_vault_deletions(vault_path)

        return {
            "events": events, "transactions": transactions,
            "todos": todos, "notes": notes, "vault_notes": vault_notes,
            "vault_deletions": vault_deletions,
        }

    def _get_vault_deletions(self, vault_path: str) -> list[dict]:
        """Read the deletion manifest for vault files."""
        if not vault_path:
            return []
        manifest_path = Path(vault_path) / ".localsync_deletions.json"
        if manifest_path.exists():
            try:
                data = json.loads(manifest_path.read_text(encoding="utf-8"))
                return data if isinstance(data, list) else []
            except Exception:
                return []
        return []

    def _record_vault_deletion(self, vault_path: str, rel_posix: str):
        """Record a file deletion in the vault manifest."""
        if not vault_path:
            return
        manifest_path = Path(vault_path) / ".localsync_deletions.json"
        deletions = self._get_vault_deletions(vault_path)
        # Don't duplicate
        existing_paths = {d["path"] for d in deletions}
        if rel_posix not in existing_paths:
            deletions.append({"path": rel_posix, "deleted_at": time.time()})
        # Keep only last 30 days of deletions
        cutoff = time.time() - (30 * 86400)
        deletions = [d for d in deletions if d.get("deleted_at", 0) > cutoff]
        try:
            manifest_path.write_text(json.dumps(deletions, indent=2), encoding="utf-8")
        except OSError as e:
            logger.warning(f"Failed to write deletion manifest: {e}")

    def _merge_remote_data(self, remote: dict) -> int:
        """Merge remote data. Returns count of changes applied."""
        changes = 0
        conn = get_connection()
        try:
            for rev in remote.get("events", []):
                local = conn.execute(
                    "SELECT updated_at FROM events WHERE id=?", (rev["id"],)
                ).fetchone()
                if local is None or rev["updated_at"] > local["updated_at"]:
                    conn.execute(
                        """INSERT INTO events (id, title, description, start_time, end_time,
                           all_day, color, updated_at, deleted)
                           VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                           ON CONFLICT(id) DO UPDATE SET
                           title=excluded.title, description=excluded.description,
                           start_time=excluded.start_time, end_time=excluded.end_time,
                           all_day=excluded.all_day, color=excluded.color,
                           updated_at=excluded.updated_at, deleted=excluded.deleted""",
                        (rev["id"], rev["title"], rev["description"],
                         rev["start_time"], rev["end_time"], rev["all_day"],
                         rev["color"], rev["updated_at"], rev["deleted"]),
                    )
                    changes += 1

            for rtx in remote.get("transactions", []):
                local = conn.execute(
                    "SELECT updated_at FROM transactions WHERE id=?", (rtx["id"],)
                ).fetchone()
                if local is None or rtx["updated_at"] > local["updated_at"]:
                    conn.execute(
                        """INSERT INTO transactions (id, date, amount, type, category,
                           description, updated_at, deleted)
                           VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                           ON CONFLICT(id) DO UPDATE SET
                           date=excluded.date, amount=excluded.amount, type=excluded.type,
                           category=excluded.category, description=excluded.description,
                           updated_at=excluded.updated_at, deleted=excluded.deleted""",
                        (rtx["id"], rtx["date"], rtx["amount"], rtx["type"],
                         rtx["category"], rtx["description"],
                         rtx["updated_at"], rtx["deleted"]),
                    )
                    changes += 1

            # Merge todos
            for rt in remote.get("todos", []):
                local = conn.execute(
                    "SELECT updated_at FROM todos WHERE id=?", (rt["id"],)
                ).fetchone()
                if local is None or rt["updated_at"] > local["updated_at"]:
                    conn.execute(
                        """INSERT INTO todos (id, title, done, priority, due_date,
                           category, notes, created_at, updated_at, deleted)
                           VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                           ON CONFLICT(id) DO UPDATE SET
                           title=excluded.title, done=excluded.done,
                           priority=excluded.priority, due_date=excluded.due_date,
                           category=excluded.category, notes=excluded.notes,
                           updated_at=excluded.updated_at, deleted=excluded.deleted""",
                        (rt["id"], rt["title"], rt["done"], rt["priority"],
                         rt["due_date"], rt["category"], rt["notes"],
                         rt["created_at"], rt["updated_at"], rt["deleted"]),
                    )
                    changes += 1

            conn.commit()
        finally:
            conn.close()

        # Merge notes (built-in notes dir)
        cfg = load_config()
        notes_dir = Path(cfg.get("notes_dir", str(NOTES_DIR)))
        for rnote in remote.get("notes", []):
            # Normalize path — always convert to OS-native from posix
            rel_posix = rnote["path"].replace("\\", "/")
            local_path = notes_dir / Path(rel_posix)
            should_write = False
            if local_path.exists():
                if rnote["mtime"] > local_path.stat().st_mtime:
                    should_write = True
            else:
                should_write = True
            if should_write:
                local_path.parent.mkdir(parents=True, exist_ok=True)
                local_path.write_text(rnote["content"], encoding="utf-8")
                changes += 1

        # Merge Obsidian vault notes
        vault_path = cfg.get("obsidian_vault_path", "")
        if vault_path:
            vault_dir = Path(vault_path)

            # First, apply remote deletions — remove files the peer deleted
            for deletion in remote.get("vault_deletions", []):
                del_posix = deletion["path"].replace("\\", "/")
                del_time = deletion.get("deleted_at", 0)
                local_path = vault_dir / Path(del_posix)
                if local_path.exists():
                    # Only delete if the local file is older than the deletion
                    try:
                        local_mtime = local_path.stat().st_mtime
                        if del_time > local_mtime:
                            local_path.unlink()
                            changes += 1
                            self._log(f"Deleted vault file (remote deletion): {del_posix}")
                            # Also record locally so we don't re-create from other peers
                            self._record_vault_deletion(vault_path, del_posix)
                    except OSError as e:
                        logger.warning(f"Failed to delete {del_posix}: {e}")

            # Build set of remotely-deleted paths for this sync
            remote_deleted = {
                d["path"].replace("\\", "/")
                for d in remote.get("vault_deletions", [])
            }

            # Then, merge vault notes — create/update files
            for rnote in remote.get("vault_notes", []):
                rel_posix = rnote["path"].replace("\\", "/")
                # Skip if this file was deleted locally
                local_deletions = {
                    d["path"] for d in self._get_vault_deletions(vault_path)
                }
                if rel_posix in local_deletions:
                    # Check if remote mtime is newer than our deletion
                    local_del_time = 0
                    for d in self._get_vault_deletions(vault_path):
                        if d["path"] == rel_posix:
                            local_del_time = d.get("deleted_at", 0)
                            break
                    if rnote["mtime"] <= local_del_time:
                        continue  # Our deletion is newer, skip
                    # Remote edit is newer than our deletion — re-create
                    # Remove from deletion manifest
                    self._remove_vault_deletion(vault_path, rel_posix)

                local_path = vault_dir / Path(rel_posix)
                should_write = False
                if local_path.exists():
                    try:
                        if rnote["mtime"] > local_path.stat().st_mtime:
                            should_write = True
                    except OSError:
                        should_write = True
                else:
                    should_write = True
                if should_write:
                    local_path.parent.mkdir(parents=True, exist_ok=True)
                    local_path.write_text(rnote["content"], encoding="utf-8")
                    changes += 1

            # Clean up empty directories left after deletions
            if vault_dir.exists():
                self._cleanup_empty_dirs(vault_dir)

        return changes

    def _remove_vault_deletion(self, vault_path: str, rel_posix: str):
        """Remove a path from the deletion manifest (file was re-created remotely)."""
        if not vault_path:
            return
        manifest_path = Path(vault_path) / ".localsync_deletions.json"
        deletions = self._get_vault_deletions(vault_path)
        deletions = [d for d in deletions if d["path"] != rel_posix]
        try:
            manifest_path.write_text(json.dumps(deletions, indent=2), encoding="utf-8")
        except OSError:
            pass

    @staticmethod
    def _cleanup_empty_dirs(root: Path):
        """Remove empty subdirectories (bottom-up) after file deletions."""
        for dirpath in sorted(root.rglob("*"), reverse=True):
            if dirpath.is_dir() and dirpath != root:
                # Skip hidden dirs
                rel = dirpath.relative_to(root)
                if any(p.startswith(".") for p in rel.parts):
                    continue
                try:
                    if not any(dirpath.iterdir()):
                        dirpath.rmdir()
                except OSError:
                    pass

    # ── Peer management ────────────────────────────────

    def _get_alive_peers(self) -> list[PeerInfo]:
        with self._lock:
            return [p for p in self._peers.values() if not p.is_stale and p.fail_count < 5]

    def _prune_stale_peers(self):
        with self._lock:
            stale = [ip for ip, p in self._peers.items() if p.is_stale]
            for ip in stale:
                # Keep manually-added peers, just mark stale
                if ip in self.cfg.get("known_peers", []):
                    continue
                del self._peers[ip]
                self.peer_lost.emit(ip)
                self._log(f"Peer went stale: {ip}")

    def _emit_peer_list(self):
        with self._lock:
            peers = []
            for ip, p in self._peers.items():
                status = "stale" if p.is_stale else ("failing" if p.fail_count > 0 else "online")
                peers.append({
                    "ip": ip,
                    "hostname": p.hostname,
                    "status": status,
                    "last_seen": p.last_seen,
                    "last_sync": p.last_sync,
                    "fail_count": p.fail_count,
                })
            self.peers_updated.emit(peers)

    def get_peer_list(self) -> list[dict]:
        """Synchronous access to peer list for the settings dialog."""
        with self._lock:
            return [
                {"ip": ip, "hostname": p.hostname,
                 "status": "stale" if p.is_stale else "online",
                 "fail_count": p.fail_count}
                for ip, p in self._peers.items()
            ]

    # ── Network helpers ────────────────────────────────

    @staticmethod
    def _send_json(sock: socket.socket, obj: dict):
        data = json.dumps(obj).encode("utf-8")
        length = struct.pack("!I", len(data))
        sock.sendall(length + data)

    @staticmethod
    def _recv_json(sock: socket.socket) -> dict | None:
        raw_len = b""
        while len(raw_len) < 4:
            chunk = sock.recv(4 - len(raw_len))
            if not chunk:
                return None
            raw_len += chunk
        msg_len = struct.unpack("!I", raw_len)[0]
        if msg_len > 50_000_000:
            return None
        data = b""
        while len(data) < msg_len:
            chunk = sock.recv(min(65536, msg_len - len(data)))
            if not chunk:
                return None
            data += chunk
        return json.loads(data.decode("utf-8"))

    @staticmethod
    def _get_local_ips() -> set[str]:
        ips = {"127.0.0.1"}
        try:
            hostname = socket.gethostname()
            for info in socket.getaddrinfo(hostname, None, socket.AF_INET):
                ips.add(info[4][0])
        except Exception:
            pass
        # Also try connecting to an external address to find our LAN IP
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.connect(("192.168.0.1", 1))
            ips.add(s.getsockname()[0])
            s.close()
        except Exception:
            pass
        return ips

    def _log(self, msg: str):
        ts = time.strftime("%H:%M:%S")
        self.sync_log.emit(f"[{ts}] {msg}")
        logger.info(msg)
