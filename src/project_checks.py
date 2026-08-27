from pathlib import Path


def required_directories_exist(base_path: str = ".") -> bool:
    required = ["src", "tests", "docs", "config"]
    base = Path(base_path)

    return all((base / directory).is_dir() for directory in required)
