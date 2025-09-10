import ast
import json
import os
import sys
from pathlib import Path

VERBOSE = ("--verbose" in sys.argv) or ("-v" in sys.argv)
PIN = ("--pin" in sys.argv)

# Map common module names to pip package names
NAME_MAP = {
    "sklearn": "scikit-learn",
    "cv2": "opencv-python",
    "PIL": "Pillow",
    "bs4": "beautifulsoup4",
    "yaml": "PyYAML",
    "skimage": "scikit-image",
    "torch": "torch",
    "torchvision": "torchvision",
    "torchaudio": "torchaudio",
    "xgboost": "xgboost",
    "lightgbm": "lightgbm",
    "catboost": "catboost",
    "statsmodels": "statsmodels",
    "numpy": "numpy",
    "pandas": "pandas",
    "matplotlib": "matplotlib",
    "seaborn": "seaborn",
    "plotly": "plotly",
    "requests": "requests",
    "tqdm": "tqdm",
    "lxml": "lxml",
    "pydantic": "pydantic",
    "fastapi": "fastapi",
    "flask": "flask",
    "uvicorn": "uvicorn",
    "sqlalchemy": "SQLAlchemy",
    "pyarrow": "pyarrow",
    "openpyxl": "openpyxl",
    "xlrd": "xlrd",
    "pytz": "pytz",
    "dateutil": "python-dateutil",
    "jupyter": "jupyter",
    "jupyterlab": "jupyterlab",
    "nbformat": "nbformat",
    "nbconvert": "nbconvert",
    "ipywidgets": "ipywidgets",
}

# Best-effort stdlib set (skip these)
STDLIB = {
    "sys","os","pathlib","json","re","math","itertools","functools","collections","subprocess",
    "typing","datetime","time","random","csv","gzip","pickle","hashlib","logging","argparse",
    "statistics","threading","asyncio","urllib","http","html","xml","sqlite3","shutil","glob",
}

def vprint(*a, **k):
    if VERBOSE:
        print(*a, **k)

def is_stdlib(name: str) -> bool:
    base = name.split(".")[0]
    return base in STDLIB or base.startswith("_")

def to_pkg(name: str) -> str:
    base = name.split(".")[0]
    return NAME_MAP.get(base, base)

def collect_from_py(path: Path) -> set[str]:
    vprint(f"[.py] {path}")
    with open(path, "r", encoding="utf-8", errors="ignore") as f:
        tree = ast.parse(f.read(), filename=str(path))
    mods = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                base = alias.name.split(".")[0]
                if not is_stdlib(base):
                    mods.add(base)
        elif isinstance(node, ast.ImportFrom) and node.module and node.level == 0:
            base = node.module.split(".")[0]
            if not is_stdlib(base):
                mods.add(base)
    return mods

def collect_from_ipynb(path: Path) -> set[str]:
    vprint(f"[.ipynb] {path}")
    with open(path, "r", encoding="utf-8", errors="ignore") as f:
        nb = json.load(f)
    mods = set()
    for cell in nb.get("cells", []):
        if cell.get("cell_type") != "code":
            continue
        source = cell.get("source", [])
        code = "".join(source) if isinstance(source, list) else str(source)
        # Strip cell magics/shell
        lines = []
        for line in code.splitlines():
            if line.strip().startswith(("%", "!", "?")):
                continue
            lines.append(line)
        code = "\n".join(lines)
        if not code.strip():
            continue
        try:
            tree = ast.parse(code)
        except Exception as e:
            vprint(f"  (skip unparsable cell: {e})")
            continue
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    base = alias.name.split(".")[0]
                    if not is_stdlib(base):
                        mods.add(base)
            elif isinstance(node, ast.ImportFrom) and node.module and node.level == 0:
                base = node.module.split(".")[0]
                if not is_stdlib(base):
                    mods.add(base)
    return mods

def main():
    root = Path(".").resolve()
    print(f"Scanning project at: {root}")
    found_modules: set[str] = set()
    scanned = 0

    for dirpath, _, filenames in os.walk(root):
        for fname in filenames:
            p = Path(dirpath) / fname
            try:
                if fname.endswith(".py"):
                    found_modules |= collect_from_py(p)
                    scanned += 1
                elif fname.endswith(".ipynb"):
                    found_modules |= collect_from_ipynb(p)
                    scanned += 1
            except Exception as e:
                print(f"[WARN] Failed parsing {p}: {e}")

    if not scanned:
        print("No .py or .ipynb files found. Are you in the right folder?")
    else:
        print(f"Scanned {scanned} files.")

    packages = sorted({to_pkg(m) for m in found_modules}, key=str.lower)

    # Always write both files so you can see something happened
    raw_path = root / "requirements_raw.txt"
    with open(raw_path, "w", encoding="utf-8") as f:
        f.write("\n".join(packages) + ("\n" if packages else ""))

    out_lines = packages[:]

    if PIN:
        try:
            from importlib.metadata import version, PackageNotFoundError
        except Exception:
            from importlib_metadata import version, PackageNotFoundError  # type: ignore
        pinned = []
        for pkg in packages:
            try:
                pinned.append(f"{pkg}=={version(pkg)}")
            except PackageNotFoundError:
                pinned.append(pkg)
        out_lines = pinned

    req_path = root / "requirements.txt"
    with open(req_path, "w", encoding="utf-8") as f:
        f.write("\n".join(out_lines) + ("\n" if out_lines else ""))

    print(f"Found {len(packages)} packages.")
    print(f"Wrote {raw_path.name} and {req_path.name} ({'pinned' if PIN else 'unpinned'}).")
    print("Open requirements.txt and tweak if needed.")

if __name__ == "__main__":
    main()
