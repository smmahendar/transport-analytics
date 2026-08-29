"""Command-line entry point for the metadata framework."""

from metadata_framework import __version__


def main() -> None:
    """Print the metadata framework name and version."""
    print(f"Transport Analytics Metadata Framework {__version__}")


if __name__ == "__main__":
    main()
