import iso8601
from src.gulp_pdf import GulpPdf, ReportEntry
from src.toggl_client import TogglClient
import calendar


class Report:

    def __init__(self, api_key: str, name: str, project_number: str, client_name: str, order_no: str):
        self.api_key = api_key
        self.name = name
        self.project_number = project_number
        self.client_name = client_name
        self.order_no = order_no

    def detailed(self, workspace: str, month_number: int):
        client = TogglClient(self.api_key)

        workspace = client.get_workspace_id(workspace)
        reports_entries = client.get_detailed_report(workspace.get('id'), month_number)

        gulp_report = GulpPdf(self.name, self.project_number, self.client_name, self.order_no)
        document_name = gulp_report.generate(
            calendar.month_name[month_number],
            list(map(
                lambda e: ReportEntry(
                    iso8601.parse_date(e['start']),
                    iso8601.parse_date(e['end']),
                    e['description'],
                ),
                reports_entries
            ))
        )

        return document_name
