from datetime import UTC, datetime

EPOCH_TIME = 1400000000


def current_utc_timestamp() -> int:
    return round(datetime.now(UTC).timestamp())


def current_utc_datetime() -> datetime:
    return datetime.now(UTC)


def timestamp_to_utc_datetime(timestamp: int) -> datetime:
    """Convert timestamp to UTC datetime object.
    1633461600 -> datetime.datetime(2021, 10, 6, 0, 0, tzinfo=datetime.timezone.utc)"""
    return datetime.fromtimestamp(timestamp, UTC)


def datetime_to_utc_timestamp(dt: datetime) -> int:
    """Convert datetime object to timestamp.
    datetime.datetime(2021, 10, 6, 0, 0, tzinfo=datetime.timezone.utc) -> 1633461600"""
    return round(dt.timestamp())


def timestamp_to_hex(timestamp: float) -> str:
    """Convert timestamp to Hexadecimal string"""
    hex_string = hex(int(timestamp - EPOCH_TIME))
    # remove the "0x" prefix
    return hex_string[2:]


def ksuid_to_timestamp(ksuid_str: str) -> int:
    """Convert KSUID string to timestamp"""
    return int(ksuid_str[:8], 16) + EPOCH_TIME
