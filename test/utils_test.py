from toggle_report_to_gulp.utils import split_string, seconds_to_hours_minutes, seconds_to_hours_decimal, iso8601_to_date
import datetime


class TestUtils:

    def test_split_string(self):
        splits = split_string('a b c', 3)

        assert len(splits) == 2
        assert splits[0] == 'a b'
        assert splits[1] == 'c'

    def test_seconds_to_hours_minutes_adds_0_before_minutes(self):
        result = seconds_to_hours_minutes(3600 + 60 + 1)

        assert result == '1:01'

    def test_seconds_to_hours_minutes_(self):
        result = seconds_to_hours_minutes(3600)

        assert result == '1:00'

    def test_seconds_to_hours_decimal(self):
        result = seconds_to_hours_decimal(3650)

        assert result == 1.01

    def test_iso8601_to_date(self):
        result = iso8601_to_date(datetime.datetime(2019, 1, 1))

        assert result == '2019-01-01'
