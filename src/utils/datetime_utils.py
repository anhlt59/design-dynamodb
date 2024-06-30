from datetime import UTC, datetime

EPOCH_TIME = 1400000000


def current_utc_timestamp() -> int:
    return round(datetime.now(UTC).timestamp())


def timestamp_to_hex(timestamp: float) -> str:
    """Convert timestamp to Hexadecimal string"""
    hex_string = hex(int(timestamp - EPOCH_TIME))
    # remove the "0x" prefix
    return hex_string[2:]


def ksuid_to_timestamp(ksuid_str: str) -> int:
    """Convert KSUID string to timestamp"""
    return int(ksuid_str[:8], 16) + EPOCH_TIME
