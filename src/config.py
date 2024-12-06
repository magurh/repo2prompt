import os
from dataclasses import dataclass
from pathlib import Path
from urllib.parse import urlparse

from dotenv import load_dotenv

load_dotenv()

# Modify as needed
SUPPORTED_FILES = (".py", ".ipynb", ".html", ".css", ".js", ".jsx", ".rst", ".md", ".go", ".yaml")

@dataclass(frozen=True, kw_only=True)
class Config:
    github_token: str
    data_path: Path
    repo_url: str
    folder_path: str
    supported_files: tuple[str]


def load_env_var(var_name: str) -> str:
    env_var = os.getenv(var_name, default="")
    if not env_var:
        msg = f"'{var_name}' not found in env"
        raise ValueError(msg)
    return env_var


def create_path(folder_name: str) -> Path:
    path = Path(__file__).parent.resolve().parent / f"{folder_name}"
    path.mkdir(exist_ok=True)
    return path


def extract_folder_from_url(repo_url: str) -> str:
    """
    Extract the folder path from a GitHub URL if it includes a specific folder.
    Example: https://github.com/owner/repo/tree/main/folder -> folder
    """
    parsed_url = urlparse(repo_url)
    path_parts = parsed_url.path.strip("/").split("/")

    if "tree" in path_parts:
        tree_index = path_parts.index("tree")
        # Skip 'tree' and branch name
        return "/".join(path_parts[tree_index + 2 :])  
    return ""  

REPO_URL = load_env_var("GITHUB_REPO_URL")

config = Config(
    github_token=load_env_var("GITHUB_TOKEN"),
    data_path=create_path("data"),
    repo_url=REPO_URL,
    folder_path=extract_folder_from_url(REPO_URL),
    supported_files=SUPPORTED_FILES,
)
