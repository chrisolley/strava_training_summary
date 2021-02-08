from datetime import datetime, timezone


def unix_time_from_string(utc_iso_datetime):
    return int(datetime.fromisoformat(utc_iso_datetime).replace(tzinfo=timezone.utc).timestamp())
