import requests
import base64
from urllib.parse import urlparse

def parse_github_url(url):
    """Parse the GitHub URL to extract owner and repository name."""
    parsed_url = urlparse(url)
    path_segments = parsed_url.path.strip("/").split("/")
    if len(path_segments) >= 2:
        return path_segments[0], path_segments[1]
    else:
        raise ValueError("Invalid GitHub URL provided!")

def fetch_repo_content(owner, repo, path='', token=None):
    """Fetch the content of the GitHub repository."""
    base_url = f"https://api.github.com/repos/{owner}/{repo}/contents/{path}"
    headers = {"Accept": "application/vnd.github.v3+json"}
    if token:
        headers["Authorization"] = f"Bearer {token}"
    response = requests.get(base_url, headers=headers)
    response.raise_for_status()  # Raise an error for non-200 responses
    return response.json()

def get_file_content(file_info):
    """Retrieve and decode the content of files."""
    if file_info['encoding'] == 'base64':
        return base64.b64decode(file_info['content']).decode('utf-8')
    return file_info['content']

def retrieve_github_repo_info(url, token=None):
    """Retrieve and format repository information."""
    owner, repo = parse_github_url(url)

    try:
        readme_info = fetch_repo_content(owner, repo, 'README.md', token)
        readme_content = get_file_content(readme_info)
        formatted_string = f"README.md:\n```\n{readme_content}\n```\n\n"
    except Exception:
        formatted_string = "README.md: Not found or error fetching README\n\n"

    from utils.directory_tree import build_directory_tree
    directory_tree, file_paths = build_directory_tree(owner, repo, token=token)

    formatted_string += f"Directory Structure:\n{directory_tree}\n"

    for indent, path in file_paths:
        file_info = fetch_repo_content(owner, repo, path, token)
        file_content = get_file_content(file_info)
        formatted_string += '\n' + '    ' * indent + f"{path}:\n" + '    ' * indent + '```\n' + file_content + '\n' + '    ' * indent + '```\n'

    return formatted_string
