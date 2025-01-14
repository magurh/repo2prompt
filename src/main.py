from tqdm import tqdm
from src.config import config
from src.utils.directory_tree import (
    build_tree_from_tree,
)
from src.utils.file_handling import save_to_file
from src.utils.github import (
    fetch_repo_content,
    fetch_repo_tree,
    get_file_content,
    parse_github_url,
)


def retrieve_github_repo_info(url: str, token: str = None, folder_path: str = "") -> tuple[str, int]:
    """Retrieve and format repository information with API call tracking."""
    owner, repo = parse_github_url(url)
    api_calls = 0  # Initialize API call counter
    formatted_string = ""

    # Fetch README.md
    try:
        api_calls += 1
        readme_info = fetch_repo_content(owner, repo, "README.md", token)
        readme_content = get_file_content(readme_info)
        formatted_string += f"README.md:\n```\n{readme_content}\n```\n\n"
    except Exception:
        pass

    # Fetch entire repo tree
    api_calls += 1
    tree_data = fetch_repo_tree(owner, repo, token)

    # Filter tree data to include only the specified folder
    if folder_path:
        tree_data = [
            item for item in tree_data if item["path"].startswith(folder_path)
        ]

    directory_tree, file_paths = build_tree_from_tree(tree_data)

    formatted_string += f"Directory Structure:\n{directory_tree}\n"

    # Fetch content for included files
    with tqdm(total=len(file_paths), desc="Fetching file contents", unit="file") as pbar:
        for path in file_paths:
            api_calls += 1
            try:
                file_info = fetch_repo_content(owner, repo, path, token)
                file_content = get_file_content(file_info)
                formatted_string += f"{path}:\n```\n{file_content}\n```\n\n"
            except Exception as e:
                formatted_string += f"{path}: Error fetching file content ({e})\n\n"
            
            # Update progress bar
            pbar.update(1) 

    return formatted_string, api_calls



def _fetch_readme_content(owner: str, repo: str, token: str = None) -> str:
    """Fetch README.md content."""
    readme_info = fetch_repo_content(owner, repo, "README.md", token)
    return get_file_content(readme_info)


def _fetch_file_content(owner: str, repo: str, path: str, token: str = None) -> str:
    """Fetch file content."""
    file_info = fetch_repo_content(owner, repo, path, token)
    return get_file_content(file_info)


def main() -> None:
    """Main entry point for the script."""
    formatted_repo_info, api_calls = retrieve_github_repo_info(
        config.repo_url, token=config.github_token, folder_path=config.folder_path,
    )
    output_file_name = (
        config.data_path / f"{config.repo_url.split('/')[-1]}-formatted-prompt.txt"
    )
    save_to_file(output_file_name, formatted_repo_info)
    print(f"Repository information has been saved to {output_file_name}")
    print(f"Total API calls made: {api_calls}")


if __name__ == "__main__":
    main()
