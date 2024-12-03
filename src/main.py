from src.config import config
from src.utils.directory_tree import build_directory_tree
from src.utils.file_handling import save_to_file
from src.utils.github import (
    fetch_repo_content,
    get_file_content,
    parse_github_url,
)


def retrieve_github_repo_info(url: str, token: str = None) -> str:
    """Retrieve and format repository information."""
    owner, repo = parse_github_url(url)

    try:
        readme_info = fetch_repo_content(owner, repo, "README.md", token)
        readme_content = get_file_content(readme_info)
        formatted_string = f"README.md:\n```\n{readme_content}\n```\n\n"
    except Exception:
        formatted_string = "README.md: Not found or error fetching README\n\n"

    directory_tree, file_paths = build_directory_tree(owner, repo, token=token)

    formatted_string += f"Directory Structure:\n{directory_tree}\n"

    for indent, path in file_paths:
        file_info = fetch_repo_content(owner, repo, path, token)
        file_content = get_file_content(file_info)
        formatted_string += (
            "\n"
            + "    " * indent
            + f"{path}:\n"
            + "    " * indent
            + "```\n"
            + file_content
            + "\n"
            + "    " * indent
            + "```\n"
        )

    return formatted_string


def main() -> None:
    formatted_repo_info = retrieve_github_repo_info(
        config.repo_url, token=config.github_token
    )
    output_file_name = (
        config.data_path / f"{config.repo_url.split('/')[-1]}-formatted-prompt.txt"
    )
    save_to_file(output_file_name, formatted_repo_info)
    print(f"Repository information has been saved to {output_file_name}")


if __name__ == "__main__":
    main()
