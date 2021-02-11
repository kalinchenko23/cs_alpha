"""customer_s URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import path,include
from users import views as user_views
from django.conf import settings
from django.conf.urls.static import static
from users.views import  (ACFTCreateView, ACFTCupdateView, Schedule_createView, ScheduleListView,
ScheduleUpdateView , Work_Progress_createView, pt)
from django.urls import re_path


urlpatterns = [
    path('admin/', admin.site.urls),
    re_path(r'aer/$', user_views.aer),


    re_path(r'schedule_create/$',Schedule_createView.as_view(), name='schedule-create'),
    re_path(r'work_progres_create/$',Work_Progress_createView.as_view(), name='work_progres_create'),
    re_path(r'acft_create/$',ACFTCreateView.as_view(), name='acft-create'),
    re_path(r'acft_update/$',ACFTCupdateView.as_view(), name='acft-update'),
    re_path(r'pt_update/$',pt, name='pt-update'),
    re_path(r'profile/$', ScheduleListView.as_view(), name='schedule-list'),
    path('resultsdata/',user_views.resultsACFT, name="acft_results"),


    path('profile/<int:pk>/', user_views.deleate_schedule, name='deleate_schedule'),
    path('profile/<int:pk>/schedule_update', ScheduleUpdateView.as_view(), name='schedule_update'),
    path('register/',user_views.register, name="register"),
    path('login/',auth_views.LoginView.as_view(template_name='users/login.html'), name="login"),
    path('logout/',auth_views.LogoutView.as_view(template_name='users/logout.html'), name="logout"),
    path('',include('cs_app.urls')),

]
if settings.DEBUG:

    urlpatterns+=static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)