"""Structural tests for the initial metadata framework scaffold."""

import sys
from pathlib import Path


REPOSITORY_ROOT = Path(__file__).resolve().parents[2]
SOURCE_ROOT = REPOSITORY_ROOT / "src"
sys.path.insert(0, str(SOURCE_ROOT))

import metadata_framework  # noqa: E402
from metadata_framework import cli  # noqa: E402


def test_package_imports() -> None:
    assert metadata_framework is not None


def test_version() -> None:
    assert metadata_framework.__version__ == "0.1.0"


def test_cli_main_exists() -> None:
    assert callable(cli.main)


def test_required_configuration_directories_exist() -> None:
    metadata_config = REPOSITORY_ROOT / "config" / "metadata"
    required_directories = (
        metadata_config / "environments",
        metadata_config / "sources",
        metadata_config / "mappings",
        metadata_config / "lineage",
    )

    assert all(directory.is_dir() for directory in required_directories)
