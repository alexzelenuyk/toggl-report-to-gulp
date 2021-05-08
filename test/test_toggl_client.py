from toggle_report_to_gulp.toggl_client import TogglClient
import responses
from datetime import datetime, timedelta, timezone


class TestTogglClient:

    @responses.activate
    def test_get_workspace(self):
        expected = {'name': 'expected_name'}
        responses.add(
            responses.GET,
            'https://www.toggl.com/api/v8/workspaces',
            json=[expected],
            status=200
        )

        workspace = TogglClient('123').get_workspace_id('test')

        assert workspace == expected

    @responses.activate
    def test_iterate_requests_until_all_read(self):
        entry1 = {'start': '2019-01-02T09:00+00:00', 'end': '2019-01-02T12:00+00:00', 'description': 'Task 1'}
        entry2 = {'start': '2019-01-02T13:00+00:00', 'end': '2019-01-02T18:00+00:00', 'description': 'Task 2'}
        responses.add(
            responses.GET,
            'https://www.toggl.com/reports/api/v2/details',
            json={'total_count': 2, 'data': [entry1]},
            status=200
        )

        responses.add(
            responses.GET,
            'https://www.toggl.com/reports/api/v2/details',
            json={'total_count': 2, 'data': [entry2]},
            status=200
        )

        reports = TogglClient('123').get_detailed_report(1, 2019, 1)

        assert len(reports) == 2
        assert reports[0].description == 'Task 1'
        assert reports[0].start == datetime(2019, 1, 2, 9, 0, tzinfo=timezone(timedelta(0), '+00:00'))
        assert reports[0].end == datetime(2019, 1, 2, 12, 0, tzinfo=timezone(timedelta(0), '+00:00'))
