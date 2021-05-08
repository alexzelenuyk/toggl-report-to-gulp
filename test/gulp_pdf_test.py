from snapshottest import TestCase
from toggle_report_to_gulp.report_summary import Summary
from toggle_report_to_gulp.gulp_pdf import GulpPdf
from datetime import datetime
from freezegun import freeze_time


class TestGulpPdf(TestCase):

    @freeze_time("2019-01-01")
    def test_match_snapshot(self):
        gulp_pdf = GulpPdf(
            'Max Mustermann',
            'Project X',
            'Muster GmbH',
            '123456'
        )

        summary = Summary(
            [[
                '2019-01-01',
                datetime(2019, 1, 1, 9, 0, 0, 0),
                datetime(2019, 1, 1, 13, 0, 0, 0),
                '01:00:00',
                'Task 1; Task 2',
                '03:00:00'
            ]],
            '3:00',
            3.0
        )
        pdf = gulp_pdf.generate(2019, 'May', summary, write=False)

        self.assertMatchSnapshot(pdf.__str__())
