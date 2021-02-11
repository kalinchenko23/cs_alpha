import calendar
import datetime

class Calendar():

    def get_current_month_days(self):
        x=str(datetime.datetime.today()).split("-")
        get_current_month=calendar.month_name[1]

        sum_of_days=[]
        for i in calendar.monthcalendar(int(x[0]),int(x[1])):
            sum_of_days+=i


        return sum_of_days

    def get_current_month_and_year(self):
        x=str(datetime.datetime.today()).split("-")
        current_month=calendar.month_name[int(x[1])]
        current_year=x[0]
        month_number=int(x[1])
        return [current_month,current_year,month_number]



