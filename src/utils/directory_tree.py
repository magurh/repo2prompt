from src.utils.github import fetch_repo_content


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
                (".py", ".ipynb", ".html", ".css", ".js", ".jsx", ".rst", ".md")
            ):
                file_paths.append((indent, item["path"]))
    return tree_str, file_paths
