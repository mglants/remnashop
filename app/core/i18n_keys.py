from enum import StrEnum

# TODO: Move all keys?


class UtilKey(StrEnum):
    BUTTON = "btn"
    MESSAGE = "msg"
    UNLIMITED = "unlimited"
    SPACE = "space"
    SEPARATOR = "separator"


class ByteUnitKey(StrEnum):
    BYTE = "unit-bytes"
    KILOBYTE = "unit-kilobytes"
    MEGABYTE = "unit-megabytes"
    GIGABYTE = "unit-gigabytes"
    TERABYTE = "unit-terabytes"


class TimeUnitKey(StrEnum):
    SECOND = "unit-seconds"
    MINUTE = "unit-minutes"
    HOUR = "unit-hours"
    DAY = "unit-days"
