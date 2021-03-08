import calendar
import datetime

class Calendar():

    def get_current_month_days(self):
        x=datetime.datetime.today()
        get_current_month=calendar.month_name[1]

        days=[]
        for day in calendar.monthcalendar(int(x.year),int(x.month)):
            for i in day:
                if i!=0:
                    day_name=calendar.day_name[calendar.weekday(int(x.year), int(x.month), int(i))]
                    days.append((i,day_name))
        return days

    def get_current_month_and_year(self):
        x=datetime.datetime.today()
        current_month=calendar.month_name[int(x.month)]
        current_year=x.year
        month_number=int(x.month)
        return [current_month,current_year,month_number]


