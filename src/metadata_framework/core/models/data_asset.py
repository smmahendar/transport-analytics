"""Technology-neutral data asset contract."""

from enum import Enum
from typing import Annotated, Any

from pydantic import AwareDatetime, BaseModel, ConfigDict, Field, field_validator


class DataAssetType(str, Enum):
    """Canonical categories of data assets."""

    API_ENDPOINT = "api_endpoint"
    CONTAINER = "container"
    DATASET = "dataset"
    FILE = "file"
    OBJECT = "object"
    TABLE = "table"
    TOPIC = "topic"
    DASHBOARD = "dashboard"


RequiredString = Annotated[str, Field(min_length=1)]


class DataAsset(BaseModel):
    """Internal, technology-neutral representation of a data asset."""

    model_config = ConfigDict(extra="forbid", str_strip_whitespace=True)

    asset_type: DataAssetType
    platform: RequiredString
    service: RequiredString
    namespace: RequiredString
    name: RequiredString
    fqn: RequiredString
    observed_at: AwareDatetime
    location: str | None = None
    format: str | None = None
    logical_dataset: str | None = None
    properties: dict[str, Any] = Field(default_factory=dict)
    fingerprint: str | None = None

    @field_validator("asset_type", mode="before")
    @classmethod
    def strip_asset_type_whitespace(cls, value: Any) -> Any:
        """Apply the string trimming policy before enum validation."""
        return value.strip() if isinstance(value, str) else value
