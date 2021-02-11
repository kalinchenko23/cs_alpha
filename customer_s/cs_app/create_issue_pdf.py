from reportlab.platypus import SimpleDocTemplate
from datetime import date
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import Paragraph, Spacer, Table, Image, ListFlowable

class SawSomething():

    def pdf_built(self,issue):
        report = SimpleDocTemplate("./media/issue/issue.pdf", pageSize="A4")
        style=getSampleStyleSheet()
        today=date.today()

        SAW = [
        Paragraph(f"I want to tell you something {today}" ,style["Title"]),
        Paragraph(issue,style["Normal"]),
        ]

        report.build(SAW)
