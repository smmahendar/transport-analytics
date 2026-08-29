"""Tests for the canonical DataAsset contract."""

import json
from datetime import UTC, datetime

import pytest
from pydantic import ValidationError

from metadata_framework.core import DataAsset, DataAssetType


def gtfs_zip_data(**overrides: object) -> dict[str, object]:
    """Return valid input for a representative GTFS ZIP asset."""
    data: dict[str, object] = {
        "asset_type": DataAssetType.FILE,
        "platform": "aistor",
        "service": "transport-raw",
        "namespace": "gtfs-static/complete",
        "name": "complete.zip",
        "fqn": "aistor.transport-raw.gtfs-static.complete.complete.zip",
        "observed_at": datetime(2026, 8, 21, 10, 30, tzinfo=UTC),
        "location": (
            "s3a://transport-raw/gtfs-static/complete/"
            "ingestion_date=2026-08-21/complete.zip"
        ),
        "format": "zip",
        "logical_dataset": "gtfs-static.complete",
    }
    data.update(overrides)
    return data


def test_creates_valid_gtfs_zip_data_asset() -> None:
    asset = DataAsset.model_validate(gtfs_zip_data())

    assert asset.asset_type is DataAssetType.FILE
    assert asset.name == "complete.zip"
    assert asset.logical_dataset == "gtfs-static.complete"
    assert asset.location == (
        "s3a://transport-raw/gtfs-static/complete/"
        "ingestion_date=2026-08-21/complete.zip"
    )


def test_data_asset_type_values() -> None:
    assert {asset_type.value for asset_type in DataAssetType} == {
        "api_endpoint",
        "container",
        "dataset",
        "file",
        "object",
        "table",
        "topic",
        "dashboard",
    }


def test_strips_string_whitespace() -> None:
    asset = DataAsset.model_validate(
        gtfs_zip_data(
            asset_type=" file ",
            platform="  aistor  ",
            name=" complete.zip ",
            logical_dataset=" gtfs-static.complete ",
        )
    )

    assert asset.asset_type is DataAssetType.FILE
    assert asset.platform == "aistor"
    assert asset.name == "complete.zip"
    assert asset.logical_dataset == "gtfs-static.complete"


def test_rejects_blank_required_field() -> None:
    with pytest.raises(ValidationError):
        DataAsset.model_validate(gtfs_zip_data(name="   "))


def test_rejects_invalid_asset_type() -> None:
    with pytest.raises(ValidationError):
        DataAsset.model_validate(gtfs_zip_data(asset_type="archive"))


def test_rejects_timezone_naive_observed_at() -> None:
    with pytest.raises(ValidationError):
        DataAsset.model_validate(
            gtfs_zip_data(observed_at=datetime(2026, 8, 21, 10, 30))  # noqa: DTZ001
        )


def test_rejects_unknown_field() -> None:
    with pytest.raises(ValidationError):
        DataAsset.model_validate(gtfs_zip_data(openmetadata_id="unknown"))


def test_properties_defaults_are_independent() -> None:
    first = DataAsset.model_validate(gtfs_zip_data())
    second = DataAsset.model_validate(gtfs_zip_data())

    first.properties["feed"] = "GTFS"

    assert second.properties == {}
    assert first.properties is not second.properties


def test_json_serialisation_and_round_trip_validation() -> None:
    asset = DataAsset.model_validate(
        gtfs_zip_data(properties={"size_bytes": 1234, "compressed": True})
    )

    json_compatible = asset.model_dump(mode="json")
    json.dumps(json_compatible)
    restored = DataAsset.model_validate_json(asset.model_dump_json())

    assert restored == asset
