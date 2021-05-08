import requests
import json
import calendar
import iso8601
from collections import namedtuple
from requests.auth import HTTPBasicAuth


TogglEntry = namedtuple('ReportEntry', 'start end description')


class TogglClient:

    BASE_URL = 'https://www.toggl.com'

    def __init__(self, api_key):
        self.api_key = api_key

    def get_workspace_id(self, pattern: str):
        workspaces_request = requests.get(
            self.url('/api/v8/workspaces'),
            auth=HTTPBasicAuth(self.api_key, 'api_token'),
        )

        if not workspaces_request.ok:
            raise BaseException(
                f"Failed to get workspaces list from api, error code: {workspaces_request.status_code}"
            )

        ws = None

        for ws in json.loads(workspaces_request.content.decode("utf8")):
            if pattern.lower() in ws.get("name"):
                return ws

        if not ws:
            raise BaseException(f"Failed to find workspace by provided name: {pattern}")

        return ws

    def get_detailed_report(self, workspace_id: int, year: int, month: int):
        report_entries = []
        page = 1

        while True:
            response = self.__get_detailed_per_page(workspace_id, year, month, page)
            report_entries += response.get('data')
            page += 1

            if response.get('total_count') == len(report_entries):
                break

        return list(map(
            lambda e: TogglEntry(
                    iso8601.parse_date(e['start']),
                    iso8601.parse_date(e['end']),
                    e['description'],
                    ),
            report_entries
        ))

    def __get_detailed_per_page(self, workspace_id: int, year: int, month: int, page: int):
        day_range = calendar.monthrange(year, month)
        params = {
            "page": page,
            "workspace_id": workspace_id,
            "since": f"{year}-{month}-1",
            "until": f"{year}-{month}-{day_range[1]}",
            "user_agent": "https://github.com/alexzelenuyk/toggl-report-to-gulp",
        }

        details = requests.get(
            self.url("/reports/api/v2/details"),
            auth=HTTPBasicAuth(self.api_key, "api_token"),
            params=params,
        )

        if not details.ok:
            raise BaseException(
                f"Failed to get workspaces list from api, error code: {details.status_code}"
            )

        return json.loads(details.content.decode("utf8"))

    def url(self, api: str):
        return f"{TogglClient.BASE_URL}{api}"
