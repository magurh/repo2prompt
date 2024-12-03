import requests
import base64
from urllib.parse import urlparse

from src.utils.cache import (
    fetch_with_cache,
    generate_cache_key,
)


def parse_github_url(url: str) -> tuple[str, str]:
    """Parse the GitHub URL to extract owner and repository name."""
    parsed_url = urlparse(url)
    path_segments = parsed_url.path.strip("/").split("/")
    if len(path_segments) >= 2:
        return path_segments[0], path_segments[1]
    else:
        raise ValueError("Invalid GitHub URL provided!")


def fetch_repo_content(
    owner: str, repo: str, path: str = "", token: str = None
) -> dict:
    """Fetch the content of the GitHub repository."""
    base_url = f"https://api.github.com/repos/{owner}/{repo}/contents/{path}"
    headers = {"Accept": "application/vnd.github.v3+json"}
    if token:
        headers["Authorization"] = f"Bearer {token}"
    response = requests.get(base_url, headers=headers)
    response.raise_for_status()  # Raise an error for non-200 responses
    return response.json()


def fetch_repo_tree(
    owner: str, repo: str, token: str = None, branch: str = "main"
) -> dict:
    """Fetch the full repository tree recursively with caching."""
    cache_key = generate_cache_key("repo_tree", owner, repo, branch)
    return fetch_with_cache(
        cache_key,
        _fetch_repo_tree_from_api,
        owner,
        repo,
        token,
        branch,
    )


def _fetch_repo_tree_from_api(
    owner: str, repo: str, token: str = None, branch: str = "main"
) -> dict:
    """Fetch the full repository tree recursively from GitHub API."""
    url = f"https://api.github.com/repos/{owner}/{repo}/git/trees/{branch}?recursive=1"
    headers = {"Accept": "application/vnd.github.v3+json"}
    if token:
        headers["Authorization"] = f"Bearer {token}"
    response = requests.get(url, headers=headers)
    response.raise_for_status()  # Raise an error for non-200 responses
    return response.json()["tree"]


def get_file_content(file_info: dict) -> str:
    """
    Retrieve and decode the content of files with caching.

    Parameters:
        file_info (dict): File metadata from the GitHub API.

    Returns:
        str: Decoded file content.
    """
    try:
        if file_info.get("encoding") == "base64":
            # Use SHA as the cache key if available; fallback to file path if missing
            cache_key = generate_cache_key(
                "file_content", file_info.get("sha", file_info.get("path", "unknown"))
            )
            return fetch_with_cache(
                cache_key, _decode_base64_content, file_info["content"]
            )
        elif "content" in file_info:
            # Handle non-base64 files (e.g., plain text or other formats)
            return file_info["content"]
        else:
            raise ValueError("Unsupported file encoding or missing content.")
    except Exception as e:
        print(
            f"Error decoding content for file: {file_info.get('path', 'unknown')} - {e}"
        )
        return ""


def _decode_base64_content(content: str) -> str:
    """
    Decode Base64 content.

    Parameters:
        content (str): Base64-encoded string.

    Returns:
        str: Decoded string.
    """
    try:
        return base64.b64decode(content).decode("utf-8")
    except Exception as e:
        raise ValueError(f"Failed to decode Base64 content: {e}")
