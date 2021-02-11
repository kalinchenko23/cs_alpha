from reportlab.platypus import SimpleDocTemplate
from datetime import date
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import Paragraph, Spacer, Table, Image, ListFlowable

class SendAER():

    def pdf_built(self,q1,q2,q3,q4,q5,q6,q7,q8,q9,q10,q11,q12,q13,q14,user,rank):
        report = SimpleDocTemplate("./media/aer/aer.pdf", pageSize="A4")
        style=getSampleStyleSheet()
        today=date.today()

        AER = [
        Paragraph(f"AER {today}" ,style["Title"]),
        Paragraph(f"created by {rank} {user}"),
        Paragraph("What suppose to happen:",style["h2"]),
        Paragraph(q1,style["Normal"]),
        Paragraph("What did happen:",style["h2"]),
        Paragraph(q2,style["Normal"]),
        Paragraph("Sustainements:",style["h2"]),
        ListFlowable(
                [Paragraph(s) for s in [
                    q3,
                    q4,
                    q5,
                    q6,
                    q7
                ]],
                leftIndent=48,

            ),
        Paragraph("Improvements:",style["h2"]),
        ListFlowable(
                [Paragraph(s) for s in [
                    q8,
                    q9,
                    q10,
                    q11,
                    q12
                ]],
                leftIndent=48,

            ),
        Paragraph("Alibis:",style["h2"]),
        ListFlowable(
                [Paragraph(s) for s in [
                    q13,
                    q14
                ]],
                leftIndent=48,

            ),
        ]

        report.build(AER)
