def save_to_file(file_path, content):
    """Save the provided content to a file."""
    with open(file_path, "w", encoding="utf-8") as file:
        file.write(content)
