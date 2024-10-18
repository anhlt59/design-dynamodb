from datetime import UTC, datetime

from uuid_utils import UUID, uuid7


def current_utc_timestamp() -> int:
    return round(datetime.now(UTC).timestamp())


def timestamp_to_hex(timestamp: float | int) -> str:
    """Convert timestamp (in seconds) to Hexadecimal string"""
    return uuid7(int(timestamp)).hex[:8]


def uuid7_to_timestamp(uuid: str) -> int:
    """Convert uuid7 string to timestamp"""
    return UUID(uuid).timestamp
