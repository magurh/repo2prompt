import requests
import base64
from urllib.parse import urlparse


def parse_github_url(url: str) -> tuple[str, str]:
    """Parse the GitHub URL to extract owner and repository name."""
    parsed_url = urlparse(url)
    path_segments = parsed_url.path.strip("/").split("/")
    if len(path_segments) >= 2:
        return path_segments[0], path_segments[1]
    else:
        raise ValueError("Invalid GitHub URL provided!")


def fetch_repo_content(owner: str, repo: str, path: str = "", token: str = None):
    """Fetch the content of the GitHub repository."""
    base_url = f"https://api.github.com/repos/{owner}/{repo}/contents/{path}"
    headers = {"Accept": "application/vnd.github.v3+json"}
    if token:
        headers["Authorization"] = f"Bearer {token}"
    response = requests.get(base_url, headers=headers)
    response.raise_for_status()  # Raise an error for non-200 responses
    return response.json()


def get_file_content(file_info: dict) -> str:
    """Retrieve and decode the content of files."""
    if file_info["encoding"] == "base64":
        return base64.b64decode(file_info["content"]).decode("utf-8")
    return file_info["content"]
