from django.shortcuts import render ,redirect
from django.contrib import messages
import os
from django.db.models import Sum
from django.http import JsonResponse
from .send_aer import SendAER,SendNumbers
from customer_s import settings
from .forms import (UserRegisterForm, UserUpdateForm, AppointmentForm, Work_ProgressForm,ProfileForm,NumbersForm,
    AerForm, ACFTForm,PT_Form)
from django.contrib.auth.decorators import login_required
from .models import  User, ACFT, Appointment, Work_Progress, PT,Profile
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
# Create your views here.
from django.urls import reverse
from reportlab.pdfgen.canvas import Canvas
from django.core.mail import EmailMessage
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView
)
from .convert_acft_to_points import *
from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType

x=SendAER()

num=SendNumbers()

y=ScoreCalculator()

class SectionListView(LoginRequiredMixin, ListView):
    model = Appointment
    template_name='users/schedule_list.html'
    context_object_name= 'schedule'

    def get_queryset(self):
            queryset = Appointment.objects.all()
            user = self.request.user
            queryset = queryset.filter(
                    created_by=user
                )
            return queryset


    def get_context_data(self, **kwargs):
        context = super(ListView, self).get_context_data(**kwargs)
        user = self.request.user
        context['user']=user
        total_numbers=Work_Progress.objects.all()
        total_numbers_for_current_user=total_numbers.filter(created_by=user)
        if total_numbers_for_current_user!= None:
            customers=sum([i.customers for i in total_numbers_for_current_user])
            context['customers']=customers

            pay_inq=sum([i.pay_inq for i in total_numbers_for_current_user])
            context['pay_inq']=pay_inq

            tl=sum([i.tl for i in total_numbers_for_current_user])
            context['tl']=tl

            cycles=sum([i.cycles for i in total_numbers_for_current_user])
            context['cycles']=cycles

            rejects=sum([i.rejects for i in total_numbers_for_current_user])
            context['rejects']=rejects

            recycles=sum([i.recycles for i in total_numbers_for_current_user])
            context['recycles']=recycles

            rsearch=sum([i.rsearch for i in total_numbers_for_current_user])
            context['rsearch']=rsearch

            management_n=sum([i.management_notices for i in total_numbers_for_current_user])
            context['management_n']=management_n

        users=[i.last_name for i in User.objects.all()]
        context['users']=users
        categories=[('Customers',context['customers']),('Pay inqueries',context['pay_inq']),('TLs',context['tl']),('Cycles',context['cycles']),('Rejects',context['rejects']),('Recycles',context['recycles']),
        ('Management notices',context['management_n']),('Research',context['rsearch'])]
        context['categories']=categories
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
        context['valid_users']=valid_users
        for i in users:
            if total_numbers.filter(created_by=User.objects.get(last_name=i)):
                valid_users.append(i)

                resp=total_numbers.filter(created_by=User.objects.get(last_name=i)).aggregate(Sum('customers'))
                total_n['Customers'].append((i,resp['customers__sum']))

                resp=total_numbers.filter(created_by=User.objects.get(last_name=i)).aggregate(Sum('pay_inq'))
                total_n['Pay inqueries'].append((i,resp['pay_inq__sum']))

                resp=total_numbers.filter(created_by=User.objects.get(last_name=i)).aggregate(Sum('tl'))
                total_n['TLs'].append((i,resp['tl__sum']))

                resp=total_numbers.filter(created_by=User.objects.get(last_name=i)).aggregate(Sum('cycles'))
                total_n['Cycles'].append((i,resp['cycles__sum']))

                resp=total_numbers.filter(created_by=User.objects.get(last_name=i)).aggregate(Sum('rejects'))
                total_n['Rejects'].append((i,resp['rejects__sum']))

                resp=total_numbers.filter(created_by=User.objects.get(last_name=i)).aggregate(Sum('recycles'))
                total_n['Recycles'].append((i,resp['recycles__sum']))

                resp=total_numbers.filter(created_by=User.objects.get(last_name=i)).aggregate(Sum('management_notices'))
                total_n['Management notices'].append((i,resp['management_notices__sum']))

                resp=total_numbers.filter(created_by=User.objects.get(last_name=i)).aggregate(Sum('rsearch'))
                total_n['Research'].append((i,resp['rsearch__sum']))
        context['total_n']=total_n

        event=ACFT.objects.all()
        event=event.filter(owner=user)
        if event!= None:
            for i in event:
                pushups_score=y.pushups(i.pushups)
                run_score=y.run(i.run)
                deadlift_score=y.dead_lift(i.dead_lift)
                sprint_drug_score=y.sdc(i.sprint_drag)
                leg_tuck_score=y.leg_t(i.leg_tucks)
                ball_score=y.ball(i.ball)
                final=pushups_score+run_score+deadlift_score+sprint_drug_score+leg_tuck_score+ball_score
                context['final_individual_score'] = final
        final_score=[]
        context['final_score']=final_score
        for i in users:
            event=event.filter(owner=User.objects.get(last_name=i))
            if event!= None:
                for i in event:
                    pushups_score=y.pushups(i.pushups)
                    run_score=y.run(i.run)
                    deadlift_score=y.dead_lift(i.dead_lift)
                    sprint_drug_score=y.sdc(i.sprint_drag)
                    leg_tuck_score=y.leg_t(i.leg_tucks)
                    ball_score=y.ball(i.ball)
                    final=pushups_score+run_score+deadlift_score+sprint_drug_score+leg_tuck_score+ball_score
                    final_score.append((i,final))

        profile=Profile.objects.all()
        profile_for_current_user=profile.filter(user=user)
        if profile_for_current_user!= None:
            for i in profile_for_current_user:
                context['rank']=i.rank
                context['height']=i.height
                context['weight']=i.weight
        users_with_profile=[]
        context['users_with_profile']=users_with_profile
        height_weight={}
        height_weight['height']=[]
        height_weight['weight']=[]
        context['height_weight']=height_weight
        for i in users:
            if profile.filter(user=User.objects.get(last_name=i)):
                users_with_profile.append(i)
                height_weight['height'].append((i," ".join([i.height for i in profile.filter(user=User.objects.get(last_name=i))])))
                height_weight['weight'].append((i," ".join([i.weight for i in profile.filter(user=User.objects.get(last_name=i))])))



        return context

class Work_Progress_createView(LoginRequiredMixin, CreateView):
    model = Work_Progress
    form_class=Work_ProgressForm
    template_name='users/work_progres_create.html'

    def get_success_url(self):
        return reverse('schedule-list')

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        return super().form_valid(form)

class Profile_createView(LoginRequiredMixin, CreateView):
    model = Profile
    form_class=ProfileForm
    template_name='users/profile_info_create.html'

    def get_success_url(self):
        return reverse('schedule-list')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)



class Appointment_createView(LoginRequiredMixin, CreateView):
    model = Appointment
    form_class=AppointmentForm
    template_name='users/shedule_upload.html'

    def get_success_url(self):
        return reverse('schedule-list')

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        return super().form_valid(form)

@login_required(login_url='/login')
def deleate_schedule(request,pk):
    if request.method=="POST":
        appointement=Appointment.objects.get(pk=pk)
        appointement.delete()
    return redirect("schedule-list")

class AppointmentUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Appointment
    form_class=AppointmentForm

    template_name='users/update_schedule.html'

    def get_success_url(self):
        return reverse('schedule-list')

    def test_func(self):
        appointement = self.get_object()
        if self.request.user == appointement.created_by:
            return True
        return False


class ACFTCreateView(LoginRequiredMixin, CreateView):
    model = ACFT
    form_class=ACFTForm

    template_name='users/ACFT.html'

    def get_success_url(self):
        return reverse('schedule-list')

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)



class ACFTCupdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = ACFT
    form_class=ACFTForm

    template_name='users/ACFT.html'

    def get_success_url(self):
        return reverse('schedule-list')

    def test_func(self):
        score = self.get_object(pk)
        if self.request.user == score.owner:
            return True
        return False

    def get_success_url(self):
        return reverse('schedule-list')

@login_required(login_url='/login')
def pt(request):
    if request.method == 'POST':
        form = PT_Form(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, f"PT schedule has been submitted")
        return redirect("/profile")
    else:
        form=PT_Form()
    context={'form':form}
    return render(request,'users/PT.html',context)

@login_required(login_url='/login')
def numbers(request):
    form=NumbersForm()
    if request.method == 'POST':
        form = NumbersForm(request.POST)
        if form.is_valid():
            date=form.cleaned_data["date"]
            num.file_built(date)
            email = EmailMessage(
                'Document',
                'Please see a document attached.',
                'kalinchenko.max@gmail.com',
                ['maksym.kalinchenko.mil@mail.mil'])
            email.attach_file('/home/kalinchenkomax/cs_alpha/customer_s/media/numbers/daily_numbers.xlsx')
            email.send()

            messages.success(request, f"The report was successfully sent")
            return redirect("/profile")
    context={
       "form":form}
    return render(request,"users/numbers_form.html",context)

@login_required(login_url='/login')
def aer(request):
    form=AerForm()
    if request.method == 'POST':
        form = AerForm(request.POST)
        if form.is_valid():
            user=request.user.last_name
            rank=Profile.objects.get(user=User.objects.get(last_name=user)).rank
            q1=form.cleaned_data["q1"]
            q2=form.cleaned_data["q2"]
            q3=form.cleaned_data["q3"]
            q4=form.cleaned_data["q4"]
            q5=form.cleaned_data["q5"]
            q6=form.cleaned_data["q6"]
            q7=form.cleaned_data["q7"]
            q8=form.cleaned_data["q8"]
            q9=form.cleaned_data["q9"]
            q10=form.cleaned_data["q10"]
            q11=form.cleaned_data["q11"]
            q12=form.cleaned_data["q12"]
            q13=form.cleaned_data["q13"]
            q14=form.cleaned_data["q14"]
            x.pdf_built(q1,q2,q3,q4,q5,q6,q7,q8,q9,q10,q11,q12,q13,q14,user,rank)
            email = EmailMessage(
                'Document',
                'Please see a document attached.',
                'kalinchenko.max@gmail.com',
                ['maksym.kalinchenko.mil@mail.mil'])
            email.attach_file('/home/kalinchenkomax/cs_alpha/customer_s/media/aer/aer.pdf')
            email.send()

            messages.success(request, f"The AER was successfully sent")
            return redirect("/profile")


    context={
       "form":form}
    return render(request,"users/aer_form.html",context)





def register(request):
    if request.method=="POST":
        form=UserRegisterForm(request.POST)
        rank=RankForm(request.POST)
        if form.is_valid() and rank.is_valid():
            user=form.save()
            user.profile.rank=rank.cleaned_data.get('rank')
            user.profile.save()
            username=form.cleaned_data.get('username')
            messages.success(request, f"Your account has been created! Please log in.")
            return redirect("/login")
    else:
        form=UserRegisterForm()
        rank=RankForm()
    return render(request, 'users/register.html',{"form":form,"rank":rank})



@login_required(login_url='/login')
def resultsACFT(request):

    user = request.user
    event=ACFT.objects.all()
    event=event.filter(owner=user)
    for i in event:
        pushups_score=y.pushups(i.pushups)
        run_score=y.run(i.run)
        deadlift_score=y.dead_lift(i.dead_lift)
        sprint_drug_score=y.sdc(i.sprint_drag)
        leg_tuck_score=y.leg_t(i.leg_tucks)
        ball_score=y.ball(i.ball)
        final=pushups_score+run_score+deadlift_score+sprint_drug_score+leg_tuck_score+ball_score
    data=[{"pushups":pushups_score},{"ball":ball_score},{"sprint drag":sprint_drug_score},{"leg tucks":leg_tuck_score},
            {"run":run_score},{"dead lift":deadlift_score}]
    return JsonResponse(data, safe=False)
