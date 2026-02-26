# -*- coding: utf-8 -*-


try:
    import tomllib
except ImportError:
    try:
        import toml as tomllib
    except ImportError:
        raise ImportError("tomllib or tomli is required for python 3.9. Install: unicecream[toml]")

from pathlib import Path


DEFAULT_CONFIG = {
    "select": ["IC001", "IC002", "IC003"],
    "ignore": [],
    "exclude": [".venv", "__pycache__", "build", "dist"],
}


def load_config():
    pyproject = Path("pyproject.toml")

    if not pyproject.exists():
        return DEFAULT_CONFIG

    try:
        with open(pyproject, "rb") as f:
            data = tomllib.load(f)

        config = data.get("tool", {}).get("unicecream", {})

        return {
            "select": config.get("select", DEFAULT_CONFIG["select"]),
            "ignore": config.get("ignore", DEFAULT_CONFIG["ignore"]),
            "exclude": config.get("exclude", DEFAULT_CONFIG["exclude"]),
        }

    except Exception:
        return DEFAULT_CONFIG
