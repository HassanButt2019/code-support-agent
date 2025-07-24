import os
import subprocess

def clone_github_repo(repo_url: str, clone_dir: str = "data/"):
    repo_name = repo_url.rstrip("/").split("/")[-1]
    dest = os.path.join(clone_dir, repo_name)
    if os.path.exists(dest):
        print(f"🔁 Repo already exists: {dest}")
        return dest
    subprocess.run(["git", "clone", "--depth", "1", repo_url, dest])
    print(f"✅ Cloned repo to: {dest}")
    return dest


def build_github_link(file_path, lines, github_repo_url):
    """
    Builds a GitHub URL to a specific file and line range.

    Args:
        file_path (str): The local file path (e.g., 'data/portfolio_backend/app/main.py')
        lines (str): Line range in 'start-end' format (e.g., '12-24')
        github_repo_url (str): The base URL of the GitHub repo (e.g., 'https://github.com/username/repo')

    Returns:
        str: Full GitHub link to the file and line range
    """
    start_line, end_line = lines.split("-")
    repo_base = github_repo_url.rstrip("/") + "/blob/main/"
    # remove 'data/portfolio_backend/' or 'data/<repo_name>/' prefix
    if "data/" in file_path:
        file_clean = "/".join(file_path.split("/")[2:])  # skip 'data' and repo folder
    else:
        file_clean = file_path
    return f"{repo_base}{file_clean}#L{start_line}-L{end_line}"

