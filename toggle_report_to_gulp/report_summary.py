from collections import namedtuple
from typing import List
from toggle_report_to_gulp.toggl_client import TogglEntry
from functools import reduce
from toggle_report_to_gulp.utils import seconds_to_hours_minutes, seconds_to_hours_decimal, iso8601_to_date

DayGroupedEntry = namedtuple('DayGroupedEntry', 'start end pause description total')


Summary = namedtuple('Summary', 'entries total_time total_summary')


class ReportSummary:

    def aggregate(self, entries: List[TogglEntry]):
        days = {d: list() for d in [iso8601_to_date(e.start) for e in entries]}

        for entry in entries:
            date = iso8601_to_date(entry.start)
            days.get(date).append(entry)

        rows = []
        for day, entries in days.items():
            merged = self.__merge_entries_for_day(entries)
            rows.append([day, *merged])

        total = reduce(lambda a, b: a + b, map(lambda a: a[5].seconds, rows))

        return Summary(
            rows,
            seconds_to_hours_minutes(total),
            seconds_to_hours_decimal(total)
        )

    def __merge_entries_for_day(self, entries: List[TogglEntry]):
        def earlier(a):
            return a.start
        entries = sorted(entries, key=earlier)

        start = entries[0].start
        end = entries[len(entries) - 1].end
        total = end - start
        work = reduce(lambda a, b: a + b, map(lambda e: e.end - e.start, entries))
        pause = total - work
        descriptions = set(map(lambda e: e.description, entries))

        return DayGroupedEntry(start, end, pause, '; '.join(descriptions), work)
