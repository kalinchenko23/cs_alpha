from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.shortcuts import render ,redirect
from .calendar_for_schedule import Calendar
from users.models import Appointment, Work_Progress, PT
from .forms import SawSome
from .create_issue_pdf import SawSomething
from django.core.mail import EmailMessage
from django.contrib import messages
from django.urls import reverse
from .uniform_selector import uniform
import datetime
import itertools
# Create your views here.

x=Calendar()
y=SawSomething()
today=str(datetime.date.today())
@login_required(login_url='/login')
def home(request):
    today_split_day=int(str(datetime.date.today()).split("-")[2])
    today_split_month=int(str(datetime.date.today()).split("-")[1])

    #Creates an objects for template
    appointment=Appointment.objects.all()
    appointments=[(int(i.date.day),int(i.date.month),i.name,i.created_by.last_name) for i in appointment]
    colors=['purple','#A52A2A','#FFA500','#FF69B4','#FFD700','#1E90FF']

    p='purple'
    work_progress=Work_Progress.objects.all()
    if len(work_progress)>len(colors):
        work_p=[(int(i.date.day),int(i.date.month),i.created_by.last_name,i.customers,i.pay_inq,i.cycles,color) for i,color in itertools.zip_longest(work_progress,colors)]
    else:
        work_p=[(int(i.date.day),int(i.date.month),i.created_by.last_name,i.customers,i.pay_inq,i.cycles,i.tl,color) for i,color in zip(work_progress,colors)]

    dates=[i.date for i in work_progress]
    weekend_indexes=[5,6,12,13,19,20,26,27,33,34]
    week_days=[]
    for i in x.get_current_month_days():
        if i!=0 and x.get_current_month_days().index(i) not in weekend_indexes:
            week_days.append(i)



    context={'days':x.get_current_month_days(),
            'uniform':uniform,
            'today_split_month':today_split_month,
            'today_split_day':today_split_day,
            'appointments':appointments,
            'work_progress':work_progress,
            'week_days':week_days,
            'dates':dates,
            'today':today,
            'work_p':work_p,
            'p':p,
            'month_and_year':x.get_current_month_and_year()}
    return render(request, 'cs_app/index.html',context)

@login_required(login_url='/login')
def pt_schedule(request):
    today_split_day=int(str(datetime.date.today()).split("-")[2])
    today_split_month=int(str(datetime.date.today()).split("-")[1])
    pt=PT.objects.all()
    pt_plan=[(int(i.date.day),int(i.date.month),i.name_of_event, i.instructor) for i in pt]
    event=""

    context={'days':x.get_current_month_days(),
            'uniform':uniform,
            'today_split_month':today_split_month,
            'today_split_day':today_split_day,
            'pt_plan':pt_plan,
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
                ['maksym.kalinchenko.mil@mail.mil'])
            email.attach_file('/home/kalinchenkomax/cs_alpha/customer_s/media/issue/issue.pdf')
            email.send()

            messages.success(request, f"The issue was addressed.")
            return redirect("/")


    context={
       "form":form}
    return render(request,"cs_app/see_something_say_something.html",context)

