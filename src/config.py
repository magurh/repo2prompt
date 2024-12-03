import os
from dataclasses import dataclass
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()


@dataclass(frozen=True, kw_only=True)
class Config:
    github_token: str
    data_path: Path
    repo_url: str


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


config = Config(
    github_token=load_env_var("GITHUB_TOKEN"),
    data_path=create_path("data"),
    repo_url=load_env_var("GITHUB_REPO_URL"),
)
