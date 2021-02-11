from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.shortcuts import render ,redirect
from .calendar_for_schedule import Calendar
from users.models import Schedule, Work_Progress, PT
from .forms import SawSome
from .create_issue_pdf import SawSomething
from django.core.mail import EmailMessage
from django.contrib import messages
from django.urls import reverse
from .uniform_selector import uniform
import datetime
# Create your views here.

x=Calendar()
y=SawSomething()
today=str(datetime.date.today())
@login_required(login_url='/login')
def home(request):
    today_split_day=int(str(datetime.date.today()).split("-")[2])
    today_split_month=int(str(datetime.date.today()).split("-")[1])

    #Creates an objects for template
    dat=Schedule.objects.all()
    work_progress=Work_Progress.objects.all()
    d=[(int(str(i.date).split("-")[1]),int(str(i.date).split("-")[2]),i.name,i.created_by.last_name) for i in dat]
    work_p=[(int(str(i.date).split("-")[1]),int(str(i.date).split("-")[2]),i.created_by.last_name,i.customers,i.pay_inq,i.cycles) for i in work_progress]
    dates=[i.date for i in work_progress]
    event=""
    weekend_indexes=[5,6,12,13,19,20,26,27,33,34]
    week_days=[]
    for i in x.get_current_month_days():
        if i!=0 and x.get_current_month_days().index(i) not in weekend_indexes:
            week_days.append(i)



    context={'days':x.get_current_month_days(),
            'uniform':uniform,
            'today_split_month':today_split_month,
            'today_split_day':today_split_day,
            'd':d,
            'work_progress':work_progress,
            'week_days':week_days,
            'dates':dates,
            'today':today,
            'work_p':work_p,
            'dat':dat,
            'month_and_year':x.get_current_month_and_year()}
    return render(request, 'cs_app/index.html',context)

@login_required(login_url='/login')
def pt_schedule(request):
    today_split_day=int(str(datetime.date.today()).split("-")[2])
    today_split_month=int(str(datetime.date.today()).split("-")[1])
    pt=PT.objects.all()
    d=[(int(str(i.date).split("-")[1]),int(str(i.date).split("-")[2]),i.name_of_event, i.instructor) for i in pt]
    event=""

    context={'days':x.get_current_month_days(),
            'uniform':uniform,
            'today_split_month':today_split_month,
            'today_split_day':today_split_day,
            'd':d,
            'pt':pt,
            'month_and_year':x.get_current_month_and_year()}
    return render(request, 'cs_app/pt_schedule.html',context)











@login_required(login_url='/login')
def saw_something(request):
    form=SawSome()

    if request.method == 'POST':

        form = SawSome(request.POST)
        if form.is_valid():
            issue=form.cleaned_data["issue"]

            y.pdf_built(issue)
            email = EmailMessage(
                'Document',
                'Please see a document attached.',
                'kalinchenko.max@gmail.com',
                ['kalinchenko.97@mail.ru'])
            email.attach_file('/Users/maximkalinchenko/Desktop/customer_service/customer_s/media/issue/issue.pdf')
            email.send()

            messages.success(request, f"The issue was addressed.")
            return redirect("/")


    context={
       "form":form}
    return render(request,"cs_app/see_something_say_something.html",context)

