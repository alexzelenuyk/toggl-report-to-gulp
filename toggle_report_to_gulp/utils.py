import iso8601
import datetime


def split_string(string: str, limit: int, sep=' '):
    words = string.split()
    if max(map(len, words)) > limit:
        raise ValueError("limit is too small")
    res, part, others = [], words[0], words[1:]
    for word in others:
        if len(sep)+len(word) > limit-len(part):
            res.append(part)
            part = word
        else:
            part += sep+word
    if part:
        res.append(part)
    return res


def seconds_to_hours_minutes(seconds: int):
    minutes = int((seconds % 3600) / 60)
    display_minutes = f"0{minutes}" if minutes < 9 else minutes
    hours = seconds / 3600

    return f"{int(hours)}:{display_minutes}"


def seconds_to_hours_decimal(seconds: int):
    hours = seconds / 3600
    return round(hours, 2)


def iso8601_to_date(date: datetime):
    return iso8601.parse_date(date.__str__()).strftime('%Y-%m-%d')
