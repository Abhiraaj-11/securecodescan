import os
import hashlib
from pathlib import Path

try:
    from git import Repo, GitCommandError
except ImportError:
    Repo = None
    GitCommandError = Exception

IGNORE_DIRS = {
    "node_modules",
    ".git",
    "dist",
    "build",
    "__pycache__",
    ".next",
    ".vscode"
}

INCLUDE_EXTENSIONS = {
    ".py", ".js", ".ts", ".tsx", ".java",
    ".cpp", ".c", ".go", ".rb", ".php",
    ".html", ".css", ".json", ".md",
    ".ipynb"
}


def clone_repository(repo_url, destination_root=None):
    destination_root = destination_root or os.path.abspath(
        os.path.join(os.path.dirname(__file__), "..", "cloned_repos")
    )
    os.makedirs(destination_root, exist_ok=True)

    repo_name = os.path.splitext(os.path.basename(repo_url.rstrip("/")))[0]
    repo_hash = hashlib.sha1(repo_url.encode("utf-8")).hexdigest()[:8]
    target_dir = os.path.join(destination_root, f"{repo_name}-{repo_hash}")

    if os.path.exists(target_dir) and os.path.isdir(target_dir):
        return target_dir

    if Repo is None:
        raise RuntimeError(
            "GitPython is required to clone repositories. Install it from requirements.txt."
        )

    try:
        Repo.clone_from(repo_url, target_dir)
        return target_dir
    except GitCommandError as exc:
        raise RuntimeError(f"Failed to clone repository: {exc}") from exc


def get_python_files(repo_path):
    python_files = []

    for root, dirs, files in os.walk(repo_path):
        dirs[:] = [d for d in dirs if d not in IGNORE_DIRS]

        for file in files:
            if file.endswith(".py"):
                python_files.append(os.path.join(root, file))

    return python_files


def get_all_files(repo_path):
    IGNORE_FILES = {"test", "example", "mock", "demo"}
    all_files = []

    for root, dirs, files in os.walk(repo_path):

        # remove unwanted directories
        dirs[:] = [d for d in dirs if d not in IGNORE_DIRS]

        root_name = os.path.basename(root).lower()

        # skip folder-level test/mock/example dirs only when the directory name matches exactly
        if root_name in IGNORE_FILES:
            continue

        for file in files:
            file_lower = file.lower()

            # skip unwanted files
            if any(x in file_lower for x in IGNORE_FILES):
                continue

            file_path = os.path.join(root, file)

            ext = os.path.splitext(file)[1].lower()

            if ext in INCLUDE_EXTENSIONS:
                all_files.append(file_path)

    print(f"[+] Total files: {len(all_files)}")
    return all_files