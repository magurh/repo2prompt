from config import config
from src.utils.github import retrieve_github_repo_info
from src.utils.file_handling import save_to_file


def main() -> None:
    # Retrieve repository information
    formatted_repo_info = retrieve_github_repo_info(
        config.repo_url, token=config.github_token
    )

    # Save the formatted information to a file
    output_file_name = (
        config.data_path / f"{config.repo_url.split('/')[-1]}-formatted-prompt.txt"
    )
    save_to_file(output_file_name, formatted_repo_info)

    print(f"Repository information has been saved to {output_file_name}")


if __name__ == "__main__":
    main()
