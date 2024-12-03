import shelve
from hashlib import sha256


def generate_cache_key(*args) -> str:
    """Generate a unique cache key based on input arguments."""
    cache_input = ":".join(map(str, args))
    return sha256(cache_input.encode("utf-8")).hexdigest()


def fetch_with_cache(key: str, fetch_func, *args, **kwargs):
    """
    Fetch data and cache it. If the data is already cached, return it directly.

    Args:
        key (str): Cache key for the operation.
        fetch_func (callable): Function to fetch the data if not cached.
        *args, **kwargs: Arguments for the fetch function.

    Returns:
        Cached or fetched data.
    """
    with shelve.open("github_cache") as cache:
        if key in cache:
            return cache[key]
        else:
            data = fetch_func(*args, **kwargs)
            cache[key] = data
            return data
