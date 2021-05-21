from toggle_report_to_gulp.gulp_pdf import GulpPdf
from toggle_report_to_gulp.toggl_client import TogglClient
from toggle_report_to_gulp.report_summary import ReportSummary
import calendar


class Report:

    def __init__(self, api_key: str, name: str, project_number: str, client_name: str, order_no: str):
        self.api_key = api_key
        self.name = name
        self.project_number = project_number
        self.client_name = client_name
        self.order_no = order_no

    def detailed(self, workspace: str, year: int, month_number: int, write: bool = True):
        client = TogglClient(self.api_key)

        workspace = client.get_workspace_id(workspace)
        toggl_entries = client.get_detailed_report(workspace.get('id'), year, month_number)

        summary = ReportSummary()
        summary = summary.aggregate(toggl_entries)

        gulp_report = GulpPdf(self.name, self.project_number, self.client_name, self.order_no)
        document_name = gulp_report.generate(
            str(year),
            calendar.month_name[month_number],
            summary,
            write
        )

        return document_name
