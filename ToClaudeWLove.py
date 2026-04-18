import os
import ast
from collections import defaultdict

OUTPUT_FILENAME = "repo_context.md"

def collect_python_files(root_dir, self_filename):
    python_files = []
    for dirpath, _, filenames in os.walk(root_dir):
        for f in filenames:
            if (f.endswith(".py") or f.endswith(".pyw") or f.endswith(".js") or f.endswith(".cs") ) and f != self_filename:
                full_path = os.path.join(dirpath, f)
                python_files.append(full_path)
    return python_files

def build_file_tree(root_dir, files):
    tree = []
    for f in files:
        rel = os.path.relpath(f, root_dir)
        parts = rel.split(os.sep)
        indent = "  " * (len(parts) - 1)
        tree.append(f"{indent}- {parts[-1]}")
    return "\n".join(tree)

def extract_dependencies(files):
    deps = defaultdict(list)
    for f in files:
        try:
            with open(f, "r", encoding="utf-8") as src:
                tree = ast.parse(src.read())
            for node in ast.walk(tree):
                if isinstance(node, ast.Import):
                    for n in node.names:
                        deps[f].append(n.name)
                elif isinstance(node, ast.ImportFrom):
                    if node.module:
                        deps[f].append(node.module)
        except Exception:
            pass
    return deps

def extract_docstrings(files):
    doc_info = {}
    for f in files:
        try:
            with open(f, "r", encoding="utf-8") as src:
                tree = ast.parse(src.read())
            module_doc = ast.get_docstring(tree)
            classes = []
            functions = []

            for node in ast.walk(tree):
                if isinstance(node, ast.ClassDef):
                    classes.append((node.name, ast.get_docstring(node)))
                elif isinstance(node, ast.FunctionDef):
                    functions.append((node.name, ast.get_docstring(node)))

            doc_info[f] = {
                "module": module_doc,
                "classes": classes,
                "functions": functions,
            }
        except Exception:
            doc_info[f] = {}
    return doc_info

def project_summary(files):
    total_lines = 0
    for f in files:
        try:
            with open(f, "r", encoding="utf-8") as src:
                total_lines += len(src.readlines())
        except:
            pass

    return {
        "file_count": len(files),
        "total_lines": total_lines,
    }

def write_context_file(root, files, tree, deps, docs, summary):
    with open(OUTPUT_FILENAME, "w", encoding="utf-8") as out:

        # Header
        out.write("# 📘 Repository Context Document\n\n")
        out.write("This document contains the full context of the repository, formatted for optimal LLM consumption.\n\n")
        out.write("## 📑 Document Structure\n")
        out.write("1. File Tree\n")
        out.write("2. Project Summary\n")
        out.write("3. Dependency Graph\n")
        out.write("4. Docstring Summary\n")
        out.write("5. Full File Contents\n\n")
        out.write("---\n\n")

        # File Tree
        out.write("## 📁 File Tree\n")
        out.write("```\n")
        out.write(tree)
        out.write("\n```\n\n")

        # Project Summary
        out.write("## 📊 Project Summary\n")
        out.write(f"- Total Python files: **{summary['file_count']}**\n")
        out.write(f"- Total lines of code: **{summary['total_lines']}**\n\n")

        # Dependency Graph
        out.write("## 🔗 Dependency Graph\n")
        for f, imports in deps.items():
            rel = os.path.relpath(f, root)
            out.write(f"### {rel}\n")
            if imports:
                for i in imports:
                    out.write(f"- {i}\n")
            else:
                out.write("- (No imports)\n")
            out.write("\n")

        # Docstring Summary
        out.write("## 📝 Docstring Summary\n")
        for f, info in docs.items():
            rel = os.path.relpath(f, root)
            out.write(f"### {rel}\n")

            out.write("**Module docstring:**\n")
            out.write(f"{info.get('module') or '(None)'}\n\n")

            out.write("**Classes:**\n")
            if info.get("classes"):
                for name, doc in info["classes"]:
                    out.write(f"- `{name}`: {doc or '(No docstring)'}\n")
            else:
                out.write("- (None)\n")
            out.write("\n")

            out.write("**Functions:**\n")
            if info.get("functions"):
                for name, doc in info["functions"]:
                    out.write(f"- `{name}`: {doc or '(No docstring)'}\n")
            else:
                out.write("- (None)\n")
            out.write("\n")

        # Full File Contents
        out.write("## 📄 Full File Contents\n")
        for f in files:
            rel = os.path.relpath(f, root)
            out.write(f"\n### `{rel}`\n\n")
            out.write("```python\n")
            try:
                with open(f, "r", encoding="utf-8") as src:
                    out.write(src.read())
            except Exception as e:
                out.write(f"# Error reading file: {e}")
            out.write("\n```\n")

def main():
    root = os.getcwd()
    self_filename = os.path.basename(__file__)
    files = collect_python_files(root, self_filename)
    files.sort()

    tree = build_file_tree(root, files)
    deps = extract_dependencies(files)
    docs = extract_docstrings(files)
    summary = project_summary(files)

    write_context_file(root, files, tree, deps, docs, summary)
    print(f"Context file created: {OUTPUT_FILENAME}")

if __name__ == "__main__":
    main()
