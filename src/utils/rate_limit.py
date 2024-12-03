import requests

from src.config import config


def fetch_rate_limit(token: str = config.github_token) -> None:
    """Fetch the current GitHub API rate limit."""
    url = "https://api.github.com/rate_limit"
    headers = {"Accept": "application/vnd.github.v3+json"}
    if token:
        headers["Authorization"] = f"Bearer {token}"
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    return response.json()


# Example usage
rate_limit = fetch_rate_limit(token=config.github_token)
print(rate_limit)

if __name__ == "__main__":
    fetch_rate_limit()
