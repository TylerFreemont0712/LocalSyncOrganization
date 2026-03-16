"""LAN sync engine — peer discovery + data exchange over TCP.

Architecture:
- Uses UDP broadcast for peer discovery on the LAN.
- Uses TCP for actual data transfer (JSON messages).
- Runs in a background QThread so the UI never freezes.
- Conflict resolution: last-write-wins based on updated_at timestamps.

The sync engine handles:
1. SQLite records (calendar events, transactions) — row-level sync
2. Note files — file-level sync using mtime comparison
"""

import json
import logging
import os
import socket
import struct
import threading
import time
from pathlib import Path

from PyQt6.QtCore import QThread, pyqtSignal

from src.config import load_config, NOTES_DIR
from src.data.database import get_connection
from src.utils.timestamps import now_utc

logger = logging.getLogger(__name__)

DISCOVERY_PORT = 42070
SYNC_MAGIC = b"LSYNC1"


class SyncEngine(QThread):
    """Background sync thread. Emits status signals for the UI."""

    status_changed = pyqtSignal(str)
    sync_completed = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self.cfg = load_config()
        self.sync_port = self.cfg.get("sync_port", 42069)
        self.interval = self.cfg.get("sync_interval_seconds", 300)
        self._running = True
        self._peers: set[str] = set()

    def run(self):
        """Main sync loop."""
        # Start discovery listener in a daemon thread
        disc_thread = threading.Thread(target=self._discovery_listener, daemon=True)
        disc_thread.start()

        # Start sync server in a daemon thread
        server_thread = threading.Thread(target=self._sync_server, daemon=True)
        server_thread.start()

        while self._running:
            try:
                self._broadcast_presence()
                time.sleep(2)  # Wait for discovery responses
                if self._peers:
                    self.status_changed.emit("syncing...")
                    for peer_ip in list(self._peers):
                        try:
                            self._sync_with_peer(peer_ip)
                        except Exception as e:
                            logger.warning(f"Sync with {peer_ip} failed: {e}")
                    self.status_changed.emit("idle")
                    self.sync_completed.emit()
                else:
                    self.status_changed.emit("no peers found")
            except Exception as e:
                logger.error(f"Sync loop error: {e}")
                self.status_changed.emit(f"error: {e}")

            # Sleep in small intervals so we can stop quickly
            for _ in range(self.interval):
                if not self._running:
                    break
                time.sleep(1)

    def stop(self):
        self._running = False

    # --- Discovery ---

    def _broadcast_presence(self):
        """Broadcast our presence on the LAN via UDP."""
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
            sock.settimeout(1)
            msg = SYNC_MAGIC + struct.pack("!H", self.sync_port)
            sock.sendto(msg, ("<broadcast>", DISCOVERY_PORT))
            sock.close()
        except Exception as e:
            logger.debug(f"Broadcast failed: {e}")

    def _discovery_listener(self):
        """Listen for peer broadcasts."""
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            sock.bind(("", DISCOVERY_PORT))
            sock.settimeout(5)
        except Exception as e:
            logger.error(f"Discovery listener bind failed: {e}")
            return

        my_ips = self._get_local_ips()
        while self._running:
            try:
                data, addr = sock.recvfrom(1024)
                if data[:6] == SYNC_MAGIC and addr[0] not in my_ips:
                    peer_port = struct.unpack("!H", data[6:8])[0]
                    self._peers.add(addr[0])
                    logger.info(f"Discovered peer: {addr[0]}:{peer_port}")
            except socket.timeout:
                continue
            except Exception as e:
                logger.debug(f"Discovery error: {e}")

    # --- Sync Server (receive incoming syncs) ---

    def _sync_server(self):
        """TCP server that accepts incoming sync requests."""
        try:
            server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            server.bind(("0.0.0.0", self.sync_port))
            server.listen(2)
            server.settimeout(5)
        except Exception as e:
            logger.error(f"Sync server bind failed: {e}")
            return

        while self._running:
            try:
                conn, addr = server.accept()
                threading.Thread(
                    target=self._handle_sync_connection,
                    args=(conn, addr),
                    daemon=True,
                ).start()
            except socket.timeout:
                continue
            except Exception as e:
                logger.debug(f"Server error: {e}")

    def _handle_sync_connection(self, conn: socket.socket, addr):
        """Handle an incoming sync connection."""
        try:
            data = self._recv_json(conn)
            if data and data.get("type") == "sync_request":
                # Send our data
                our_data = self._gather_local_data()
                self._send_json(conn, {"type": "sync_response", "data": our_data})
                # Receive and merge their data
                their_data = data.get("data", {})
                self._merge_remote_data(their_data)
                self.sync_completed.emit()
        except Exception as e:
            logger.warning(f"Sync handler error from {addr}: {e}")
        finally:
            conn.close()

    # --- Sync Client (initiate sync) ---

    def _sync_with_peer(self, peer_ip: str):
        """Initiate sync with a peer."""
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(10)
        try:
            sock.connect((peer_ip, self.sync_port))
            our_data = self._gather_local_data()
            self._send_json(sock, {"type": "sync_request", "data": our_data})

            response = self._recv_json(sock)
            if response and response.get("type") == "sync_response":
                self._merge_remote_data(response.get("data", {}))
        finally:
            sock.close()

    # --- Data Gathering & Merging ---

    def _gather_local_data(self) -> dict:
        """Collect all local data for sync."""
        conn = get_connection()
        try:
            events = [dict(r) for r in conn.execute("SELECT * FROM events").fetchall()]
            transactions = [dict(r) for r in conn.execute("SELECT * FROM transactions").fetchall()]
        finally:
            conn.close()

        # Gather notes metadata
        notes = []
        notes_dir = Path(load_config().get("notes_dir", str(NOTES_DIR)))
        if notes_dir.exists():
            for md in notes_dir.rglob("*.md"):
                rel = str(md.relative_to(notes_dir))
                mtime = md.stat().st_mtime
                content = md.read_text(encoding="utf-8")
                notes.append({"path": rel, "mtime": mtime, "content": content})

        return {"events": events, "transactions": transactions, "notes": notes}

    def _merge_remote_data(self, remote: dict):
        """Merge remote data using last-write-wins on updated_at."""
        conn = get_connection()
        try:
            # Merge events
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

            # Merge transactions
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

            conn.commit()
        finally:
            conn.close()

        # Merge notes (file-level, mtime-based)
        notes_dir = Path(load_config().get("notes_dir", str(NOTES_DIR)))
        for rnote in remote.get("notes", []):
            local_path = notes_dir / rnote["path"]
            if local_path.exists():
                local_mtime = local_path.stat().st_mtime
                if rnote["mtime"] > local_mtime:
                    local_path.write_text(rnote["content"], encoding="utf-8")
            else:
                local_path.parent.mkdir(parents=True, exist_ok=True)
                local_path.write_text(rnote["content"], encoding="utf-8")

    # --- Network helpers ---

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
        if msg_len > 50_000_000:  # 50MB safety limit
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
        return ips
