from reportlab.platypus import SimpleDocTemplate
from datetime import date
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import Paragraph, Spacer, Table, Image, ListFlowable
from .models import Work_Progress,Profile,User
import pandas as pd


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

class SendNumbers():

    def file_built(self,date):
        users=[i.last_name for i in User.objects.all()]
        total_numbers=Work_Progress.objects.all()
        total_n={}
        total_n['Customers']=[]
        total_n['Pay inqueries']=[]
        total_n['TLs']=[]
        total_n['Cycles']=[]
        total_n['Rejects']=[]
        total_n['Recycles']=[]
        total_n['Management notices']=[]
        total_n['Research']=[]
        valid_users=[]
        for i in users:
            if total_numbers.filter(date=date,created_by=User.objects.get(last_name=i)):
                valid_users.append(i)

                resp=total_numbers.filter(date=date,created_by=User.objects.get(last_name=i))
                for i in resp:
                    total_n['Customers'].append(i.customers)
                    total_n['Pay inqueries'].append(i.pay_inq)
                    total_n['TLs'].append(i.tl)
                    total_n['Cycles'].append(i.cycles)
                    total_n['Rejects'].append(i.rejects)
                    total_n['Recycles'].append(i.recycles)
                    total_n['Management notices'].append(i.management_notices)
                    total_n['Research'].append(i.rsearch)
        numbers=pd.DataFrame.from_dict(total_n)
        numbers.set_index([valid_users],inplace=True)
        numbers.to_excel('/home/kalinchenkomax/cs_alpha/customer_s/media/numbers/daily_numbers.xlsx')











