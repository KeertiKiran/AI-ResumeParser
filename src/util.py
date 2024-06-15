import os

def ensure_path(path: str) -> None:
    """Ensures that the path exists, if not, creates it.

    Args:
        path (str): The path to ensure.
    """
    if not os.path.exists(path):
        os.makedirs(path)