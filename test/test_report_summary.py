from toggle_report_to_gulp.report_summary import ReportSummary
from toggle_report_to_gulp.toggl_client import TogglEntry
import iso8601
from datetime import datetime, timedelta, timezone


class TestReportSummary:

    def test_aggregate_toggl_entries(self):
        result = ReportSummary().aggregate(
            [
                TogglEntry(
                    iso8601.parse_date('2019-01-01T09:00+00:00'),
                    iso8601.parse_date('2019-01-01T12:00+00:00'),
                    'Task 1',
                ),
                TogglEntry(
                    iso8601.parse_date('2019-01-01T13:00+00:00'),
                    iso8601.parse_date('2019-01-01T18:00+00:00'),
                    'Task 1',
                ),
                TogglEntry(
                    iso8601.parse_date('2019-01-02T09:00+00:00'),
                    iso8601.parse_date('2019-01-02T12:00+00:00'),
                    'Task 2',
                ),
                TogglEntry(
                    iso8601.parse_date('2019-01-02T13:00+00:00'),
                    iso8601.parse_date('2019-01-02T18:00+00:00'),
                    'Task 2',
                ),
            ]
        )

        assert result.total_time == '16:00'
        assert result.total_summary == 16.0
        assert len(result.entries) == 2
        assert result.entries[0] == [
                '2019-01-01',
                datetime(2019, 1, 1, 9, 0, tzinfo=timezone(timedelta(0), '+00:00')),
                datetime(2019, 1, 1, 18, 0, tzinfo=timezone(timedelta(0), '+00:00')),
                timedelta(seconds=3600),
                'Task 1',
                timedelta(seconds=28800)
            ]

        assert result.entries[1] == [
                '2019-01-02',
                datetime(2019, 1, 2, 9, 0, tzinfo=timezone(timedelta(0), '+00:00')),
                datetime(2019, 1, 2, 18, 0, tzinfo=timezone(timedelta(0), '+00:00')),
                timedelta(seconds=3600),
                'Task 2',
                timedelta(seconds=28800)
            ]
