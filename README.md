# repo2prompt

Turn a Github Repo's contents into a big prompt for long-context models like Claude 3 Opus.

## Setup

The repository uses `uv` for dependency management. 
Run:

```bash
uv sync --all-extras
```


Introduce the desired Github repository URL into the `.env` file. 
For better rate limit, generate a Github access token, as described in the [github docs](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/managing-your-personal-access-tokens).
Note, however, that Github is still limited to 5,000 API requests per hour even with a token.
For private repositories, make sure that the token has the appropriate permissions.

Run the `main` script using:

```bash
uv run python -m src.main
```

The output is saved to a `.txt` file with name `[repo]-formatted-prompt.txt`, in the `data` folder. 
To check the number of remaining API calls run:

```bash
uv run python -m src.utils.rate_limit
```


##  Description

This repository is forked from andrewgcodes repo2prompt, and includes various improvements:

* Cleaner structure, formatting, and direct script running.
* Using GitHub `tree` API for recursive directory retrieval.
* Using caching system for previously fetched data.
* Allow calls to specific subfolders of a repository.


