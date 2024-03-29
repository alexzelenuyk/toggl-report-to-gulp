#!/usr/bin/env python3.8

import argparse
from toggle_report_to_gulp.report import Report
import locale

locale.setlocale(locale.LC_ALL, 'de_DE')


def main():
    parser = argparse.ArgumentParser(description='Creates report for GULP according to Toggl notes.')
    parser.add_argument('--workspace', help='Workspace name', required=True)
    parser.add_argument('--api-key', help='Api key name, can be found here: https://toggl.com/app/profile',
                        required=True)
    parser.add_argument('--month-number',
                        help='Month number, from 1 to 12',
                        required=True,
                        type=int
                        )
    parser.add_argument('--year',
                        help='Year',
                        required=True,
                        type=int
                        )
    parser.add_argument('--name', help='You first and last name. Will be used in header', required=True, type=str)
    parser.add_argument('--project-number', help='Project number (PEV). Will be used in header', required=True,
                        type=str)
    parser.add_argument('--client-name', help='Client name. Will be used in header', required=True, type=str)
    parser.add_argument('--order-no', help='Order no (Bestellnummer). Will be used in header', required=True, type=str)
    parser.add_argument('--write',
                        help='Write to file or to the output',
                        choices=['true', 'false'],
                        default='true'
                        )
    args = parser.parse_args()

    report = Report(args.api_key, args.name, args.project_number, args.client_name, args.order_no)
    document_name = report.detailed(args.workspace, args.year, args.month_number, args.write == 'true')

    print(f"Finished! Report store in {document_name}")


if __name__ == "__main__":
    main()
