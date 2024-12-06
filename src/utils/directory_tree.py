from src.config import config
from src.utils.github import fetch_repo_content


def build_tree_from_tree(tree_data) -> tuple[str, list]:
    """Build directory structure and collect file paths using the GitHub tree API response."""
    tree_str = ""
    file_paths = []

    for item in tree_data:
        if ".github" in item["path"].split("/"):
            continue  # Skip .github directory

        # Check if it's a file or directory
        if item["type"] == "tree":  # GitHub API uses 'tree' for directories
            tree_str += f"[{item['path']}/]\n"
        elif item["type"] == "blob":  # GitHub API uses 'blob' for files
            tree_str += f"{item['path']}\n"
            if item["path"].endswith(
                config.supported_files
            ):
                file_paths.append(item["path"])

    return tree_str, file_paths


def build_directory_tree(
    owner: str,
    repo: str,
    path: str = "",
    token: str = None,
    indent: int = 0,
    file_paths: list = [],
) -> tuple[str, list]:
    """Build a string representation of the directory tree and collect file paths."""
    items = fetch_repo_content(owner, repo, path, token)
    tree_str = ""
    for item in items:
        if ".github" in item["path"].split("/"):
            continue
        if item["type"] == "dir":
            tree_str += "    " * indent + f"[{item['name']}/]\n"
            tree_str += build_directory_tree(
                owner, repo, item["path"], token, indent + 1, file_paths
            )[0]
        else:
            tree_str += "    " * indent + f"{item['name']}\n"
            if item["name"].endswith(
               config.supported_files
            ):
                file_paths.append((indent, item["path"]))
    return tree_str, file_paths
