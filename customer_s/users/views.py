from django.shortcuts import render ,redirect
from django.contrib import messages
import os
from django.http import JsonResponse
from .send_aer import SendAER
from customer_s import settings
from .forms import (UserRegisterForm, UserUpdateForm, ScheduleForm, Work_ProgressForm,
    AerForm, RankForm, ACFTForm,PT_Form)
from django.contrib.auth.decorators import login_required
from .models import Profile, User, ACFT, Schedule, Work_Progress, PT
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
y=ScoreCalculator()

class ScheduleListView(LoginRequiredMixin, ListView):
    model = Schedule
    template_name='users/schedule_list.html'
    context_object_name= 'schedule'

    def get_queryset(self):
            queryset = Schedule.objects.all()
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
        if total_numbers!= None:
            customers=sum([i.customers for i in total_numbers_for_current_user])
            context['customers']=customers

            pay_inq=sum([i.pay_inq for i in total_numbers_for_current_user])
            context['pay_inq']=pay_inq

            cycles=len([i.pay_inq for i in total_numbers_for_current_user])
            context['cycles']=cycles

            rejects=len([i.rejects for i in total_numbers_for_current_user])
            context['rejects']=rejects

            recycles=len([i.rejects for i in total_numbers_for_current_user])
            context['recycles']=recycles

        oliver=User.objects.get(last_name='Oliver')
        kalinchenko=User.objects.get(last_name='Kalinchenko')
        skipwith=User.objects.get(last_name='Skipwith')

        customers_oliver=sum([i.customers for i in total_numbers.filter(created_by=oliver)])
        context['customers_oliver']=customers_oliver
        customers_kalinchenko=sum([i.customers for i in total_numbers.filter(created_by=kalinchenko)])
        context['customers_kalinchenko']=customers_kalinchenko
        customers_skipwith=sum([i.customers for i in total_numbers.filter(created_by=skipwith)])
        context['customers_skipwith']=customers_skipwith

        pay_inq_oliver=sum([i.pay_inq for i in total_numbers.filter(created_by=oliver)])
        context['pay_inq_oliver']=pay_inq_oliver
        pay_inq_skipwith=sum([i.pay_inq for i in total_numbers.filter(created_by=skipwith)])
        context['pay_inq_skipwith']=pay_inq_oliver
        pay_inq_kalinchenko=sum([i.pay_inq for i in total_numbers.filter(created_by=kalinchenko)])
        context['pay_inq_kalinchenko']=pay_inq_kalinchenko


        cycles_oliver=len([i.pay_inq for i in total_numbers.filter(created_by=oliver)])
        context['cycles_oliver']=cycles_oliver
        cycles_skipwith=len([i.pay_inq for i in total_numbers.filter(created_by=skipwith)])
        context['cycles_skipwith']=cycles_skipwith
        cycles_kalinchenko=len([i.pay_inq for i in total_numbers.filter(created_by=kalinchenko)])
        context['cycles_kalinchenko']=cycles_kalinchenko

        rejects_oliver=len([i.rejects for i in total_numbers.filter(created_by=oliver)])
        context['rejects_oliver']=rejects_oliver
        rejects_skipwith=len([i.rejects for i in total_numbers.filter(created_by=skipwith)])
        context['rejects_skipwith']=rejects_skipwith
        rejects_kalinchenko=len([i.rejects for i in total_numbers.filter(created_by=kalinchenko)])
        context['rejects_kalinchenko']=rejects_kalinchenko

        recycles_oliver=len([i.rejects for i in total_numbers.filter(created_by=oliver)])
        context['recycles_oliver']=recycles_oliver
        recycles_skipwith=len([i.rejects for i in total_numbers.filter(created_by=skipwith)])
        context['recycles_skipwith']=recycles_skipwith
        recycles_kalinchenko=len([i.rejects for i in total_numbers.filter(created_by=kalinchenko)])
        context['recycles_kalinchenko']=recycles_kalinchenko


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
                context['final_score'] = final

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


class Schedule_createView(LoginRequiredMixin, CreateView):
    model = Schedule
    form_class=ScheduleForm
    template_name='users/shedule_upload.html'

    def get_success_url(self):
        return reverse('schedule-list')

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        return super().form_valid(form)

@login_required(login_url='/login')
def deleate_schedule(request,pk):
    if request.method=="POST":
        appointement=Schedule.objects.get(pk=pk)
        appointement.delete()
    return redirect("schedule-list")

class ScheduleUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Schedule
    form_class=ScheduleForm

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
def aer(request):
    form=AerForm()

    if request.method == 'POST':

        form = AerForm(request.POST)
        if form.is_valid():
            user=request.user.get_full_name()
            rank=request.user.profile.rank
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
                ['kalinchenko.97@mail.ru'])
            email.attach_file('/Users/maximkalinchenko/Desktop/customer_service/customer_s/media/aer/aer.pdf')
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
