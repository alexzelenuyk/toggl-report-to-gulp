from fpdf import FPDF
from collections import namedtuple
from typing import List
from src.utils import split_string
from functools import reduce
import datetime


ReportEntry = namedtuple('ReportEntry', 'start end description')


class GulpPdf:

    FONT = "Arial"
    DEFAULT_HEADER_FONT_SIZE = 18
    DEFAULT_FONT_SIZE = 12
    REPORT_NAME_TEMPLATE = 'Leistungsnachweis_{}.pdf'
    REPORT_HEAD = ['Datum', 'Zeit', 'Leistungsbeschreibung', 'Gesamt']
    SPACING = 2

    def __init__(self, first_name: str, project_number: str, client_name: str, order_no: str):
        self.name = first_name
        self.project_number = project_number
        self.client_name = client_name
        self.order_no = order_no

    def generate(self, month: str, details: List[ReportEntry]):
        document = GulpPdf.REPORT_NAME_TEMPLATE . format(month)
        pdf = self.__document()
        details = list(details)

        pdf = self.__head(pdf, month)
        pdf = self.__table(pdf, details)
        pdf = self.__summary(pdf, details)
        pdf = self.__footer(pdf)

        pdf.output(document)

        return document

    def __head(self, pdf: FPDF, month: str):
        pdf.set_font(GulpPdf.FONT, "B", GulpPdf.DEFAULT_HEADER_FONT_SIZE)
        pdf.write(16, "Leistungsnachweis\n")
        pdf.set_font(GulpPdf.FONT, "B", GulpPdf.DEFAULT_FONT_SIZE)

        data = [
            ["Monat:", f"{month.capitalize()} {datetime.datetime.now().year}"],
            ["Auftraggeber Kunde:", self.client_name],
            ["Bestellnummer:", self.order_no],
            ["Leistungserbringer", self.name],
            ["Projektvertragsnummer:", self.project_number]
        ]

        height = self.pdf_height(pdf)

        for row in data:
            pdf.cell(pdf.w * 0.3, height, txt=row[0], border=0)
            pdf.cell(pdf.w * 0.2, height, txt=row[1], border="B")
            pdf.ln(height)

        pdf.write(16, "\n")

        return pdf

    def __table(self, pdf: FPDF, details: List[ReportEntry]):
        pdf.set_font(GulpPdf.FONT, size=GulpPdf.DEFAULT_FONT_SIZE)

        default_height = self.pdf_height(pdf)

        rows = list(self.__map_entries_to_row(details))
        rows.append(GulpPdf.REPORT_HEAD)

        for row in reversed(rows):
            splits = split_string(row[2], 50)
            height = default_height * len(splits)

            pdf.cell(pdf.w * 0.12, height, txt=row[0], border=1)
            pdf.cell(pdf.w * 0.15, height, txt=row[1], border=1)
            desc_w = pdf.w * 0.5
            if len(splits) > 1:
                current_x = pdf.get_x()
                current_y = pdf.get_y()
                pdf.multi_cell(desc_w, default_height, txt=row[2], border=1)
                pdf.set_xy(current_x + desc_w, current_y)
            else:
                pdf.cell(desc_w, height, txt=row[2], border=1)
            pdf.cell(pdf.w * 0.1, height, txt=row[3], border=1)

            pdf.ln(height)

        return pdf

    def __summary(self, pdf: FPDF, details: List[ReportEntry]):
        h = self.pdf_height(pdf)
        total = self.__count_total(details)
        hours = total / 3600
        minutes = int((total % 3600) / 60)
        display_minutes = minutes if minutes < 9 else f"0{minutes}"
        rows = [
            ["Summe Stunden und Minuten", f"{int(hours)}:{display_minutes}"],
            ["Summe Stunden und Minuten dezimal", f"{round(hours, 2)}"],
        ]

        for row in rows:
            pdf.cell(pdf.w * 0.27, h, txt="", border=0)
            pdf.cell(pdf.w * 0.5, h, txt=row[0], border=0, align="R")
            pdf.cell(pdf.w * 0.1, h, txt=row[1], border=1)
            pdf.ln(h)

        return pdf

    def __footer(self, pdf: FPDF):
        h = self.pdf_height(pdf)

        pdf.ln(h * 2)
        pdf.cell(pdf.w * 0.1, h, txt="Leistung erbracht:", border=0)
        pdf.ln(h * 2)

        w = pdf.w * 0.15
        pdf.cell(w, h, txt="Ort", border="T", align="L")
        pdf.cell(w, h, txt="Datum", border="T", align="R")
        pdf.cell(w, h, txt="", border=0)
        pdf.cell(w, h, txt="Ort", border="T", align="L")
        pdf.cell(w, h, txt="Datum", border="T", align="R")

        pdf.ln(h * 2)

        pdf.cell(w * 2, h, txt="Unterschrift Leistungserbringer", border="T")
        pdf.cell(w, h, txt="", border=0)
        pdf.cell(w * 2, h, txt="Unterschrift Auftraggeber", border="T")
        pdf.ln(h)

        return pdf

    def __count_total(self, details: List[ReportEntry]):
        deltas = map(
            lambda e: (e.end - e.start).seconds,
            details
        )

        return reduce(lambda a, b: a + b, deltas)

    def __map_entries_to_row(self, details: List[ReportEntry]):
        return map(
            lambda e: [
                e.start.strftime('%Y-%m-%d'),
                f"{e.start.strftime('%H:%M')} - {e.end.strftime('%H:%M')}",
                e.description,
                (e.end - e.start).__str__()
            ],
            details
        )

    def pdf_height(self, pdf: FPDF):
        return pdf.font_size * GulpPdf.SPACING

    def __document(self):
        pdf = FPDF()
        pdf.add_page()

        return pdf
