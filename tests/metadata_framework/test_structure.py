"""Structural tests for the initial metadata framework scaffold."""

from pathlib import Path

import metadata_framework
from metadata_framework import __version__, cli

REPOSITORY_ROOT = Path(__file__).resolve().parents[2]


def test_package_imports() -> None:
    assert metadata_framework is not None


def test_version() -> None:
    assert __version__ == "0.1.0"


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
