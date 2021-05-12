from fpdf import FPDF
from typing import List
from toggle_report_to_gulp.utils import split_string
from toggle_report_to_gulp.report_summary import DayGroupedEntry, Summary


class GulpPdf:

    FONT = "Arial"
    DEFAULT_HEADER_FONT_SIZE = 14
    DEFAULT_FONT_SIZE = 8
    REPORT_NAME_TEMPLATE = 'Leistungsnachweis_{}.pdf'
    REPORT_HEAD = ['Datum', 'Start', 'Ende', 'Pause', 'Leistungsbeschreibung', 'Gesamt']
    SPACING = 1.5

    def __init__(self, first_name: str, project_number: str, client_name: str, order_no: str):
        self.name = first_name
        self.project_number = project_number
        self.client_name = client_name
        self.order_no = order_no

    def generate(self, year: str, month: str, summary: Summary, write=True):
        document = GulpPdf.REPORT_NAME_TEMPLATE . format(month)
        pdf = self.__document()

        pdf = self.__head(pdf, year, month)
        pdf = self.__table(pdf, summary.entries)
        pdf = self.__summary(pdf, summary.total_time, summary.total_summary)
        pdf = self.__footer(pdf)

        dest = 'F' if write else 'S'

        result = pdf.output(document, dest)

        return document if write else result.encode('latin-1')

    def __head(self, pdf: FPDF, year: str, month: str):
        pdf.set_font(GulpPdf.FONT, "B", GulpPdf.DEFAULT_HEADER_FONT_SIZE)
        pdf.write(GulpPdf.DEFAULT_HEADER_FONT_SIZE, "Leistungsnachweis\n")
        pdf.set_font(GulpPdf.FONT, "B", GulpPdf.DEFAULT_FONT_SIZE)

        data = [
            ["Monat:", f"{month.capitalize()} {year}"],
            ["Auftraggeber Kunde:", self.client_name],
            ["Bestellnummer:", self.order_no],
            ["Leistungserbringer", self.name],
            ["Projektvertragsnummer:", self.project_number]
        ]

        height = self.__pdf_height(pdf)

        for row in data:
            pdf.cell(pdf.w * 0.3, height, txt=row[0], border=0)
            pdf.cell(pdf.w * 0.2, height, txt=row[1], border="B")
            pdf.ln(height)

        pdf.write(8, "\n")

        return pdf

    def __table(self, pdf: FPDF, details: List[DayGroupedEntry]):
        pdf.set_font(GulpPdf.FONT, size=GulpPdf.DEFAULT_FONT_SIZE)
        self.__row(pdf, GulpPdf.REPORT_HEAD)

        for row in reversed(list(details)):
            row[1] = row[1].strftime('%H:%M:%S')
            row[2] = row[2].strftime('%H:%M:%S')
            self.__row(pdf, row)

        return pdf

    def __row(self, pdf: FPDF, row: DayGroupedEntry):
        default_height = self.__pdf_height(pdf)

        splits = split_string(row[4], 90)
        height = default_height * len(splits)

        pdf.cell(pdf.w * 0.08, height, txt=row[0], border=1)
        pdf.cell(pdf.w * 0.07, height, txt=row[1].__str__(), border=1)
        pdf.cell(pdf.w * 0.07, height, txt=row[2].__str__(), border=1)
        pdf.cell(pdf.w * 0.06, height, txt=row[3].__str__(), border=1)
        desc_w = pdf.w * 0.57
        if len(splits) > 1:
            current_x = pdf.get_x()
            current_y = pdf.get_y()
            pdf.multi_cell(desc_w, default_height, txt=row[4], border=1)
            pdf.set_xy(current_x + desc_w, current_y)
        else:
            pdf.cell(desc_w, height, txt=row[4], border=1)
        pdf.cell(pdf.w * 0.06, height, txt=row[5].__str__(), border=1)

        pdf.ln(height)

    def __summary(self, pdf: FPDF, total_time: str, total_decimal: float):
        h = self.__pdf_height(pdf)

        rows = [
            ["Summe Stunden und Minuten", total_time],
            ["Summe Stunden und Minuten dezimal", total_decimal],
        ]

        for row in rows:
            pdf.cell(pdf.w * 0.2, h, txt="", border=0)
            pdf.cell(pdf.w * 0.65, h, txt=row[0], border=0, align="R")
            pdf.cell(pdf.w * 0.06, h, txt=row[1].__str__(), border=1)
            pdf.ln(h)

        return pdf

    def __footer(self, pdf: FPDF):
        h = self.__pdf_height(pdf)

        pdf.cell(pdf.w * 0.1, h, txt="Leistung erbracht:", border=0)
        pdf.ln(h * 3)

        w = pdf.w * 0.15
        pdf.cell(w, h, txt="Ort", border="T", align="L")
        pdf.cell(w, h, txt="Datum", border="T", align="R")
        pdf.cell(w, h, txt="", border=0)
        pdf.cell(w, h, txt="Ort", border="T", align="L")
        pdf.cell(w, h, txt="Datum", border="T", align="R")

        pdf.ln(h * 3)

        pdf.cell(w * 2, h, txt="Unterschrift Leistungserbringer", border="T")
        pdf.cell(w, h, txt="", border=0)
        pdf.cell(w * 2, h, txt="Unterschrift Auftraggeber", border="T")
        pdf.ln(h)

        return pdf

    def __pdf_height(self, pdf: FPDF):
        return pdf.font_size * GulpPdf.SPACING

    def __document(self):
        pdf = FPDF()
        pdf.add_page()
        pdf.set_auto_page_break(False)

        return pdf
