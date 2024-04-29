"""simplecrm URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
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
from django.urls import path
from django.urls.conf import include

from accounts import views as aviews 
from leads import views as lviews
from opportunities import views as oviews
from contacts import views as cviews
from meetings import views as mviews
from calls import views as caviews
from interaction import views as inviews
from tasks import views as tviews
from reminder import views as rviews
from simplecrm import Register_login as Reg
from simplecrm import ingestexcel as ingex
from simplecrm import get_column_name as getxcol

urlpatterns = [
    #path('admin/', admin.site.urls),
    path('register/', Reg.register, name='register'),  # Endpoint for user registration
    path('login/', Reg.LoginView.as_view(), name='login'), 
    path(r'accounts/', aviews.AccountListCreateAPIView.as_view(), name='account-list'),
    path('accounts/<int:pk>/', aviews.AccountDetailAPIView.as_view(), name='account-detail'),
    path(r'leads/', lviews.LeadListCreateAPIView.as_view(), name='lead-list'),
    path('leads/<int:pk>/',lviews.LeadDetailAPIView.as_view(), name='lead-detail'),
    path(r'opportunities/', oviews.OpportunityListAPIView.as_view(), name='opportunity-list'),
    path('contacts/', cviews.ContactListCreateAPIView.as_view(), name='contact-list-create'),
    path('contacts/<int:pk>/', cviews.ContactDetailAPIView.as_view(), name='contact-detail'),
    path('meetings/', mviews.MeetingListAPIView.as_view(), name='meeting-list'),
    path('calls/', caviews.callsListAPIView.as_view(), name='calls'), 
    path('interaction/', inviews.InteractionListAPIView.as_view(), name='interaction'),  
    path('tasks/', tviews.TaskListCreateAPIView.as_view(), name='task-list'),
    path('tasks/<int:pk>/', tviews.TaskRetrieveUpdateDestroyAPIView.as_view(), name='task-detail'), 
    path('reminders/', rviews.ReminderListAPIView.as_view(), name='reminder-list'),
    path('uploadexcel/', ingex.ImportLeadData, name='excel'),
    path('excel-column/', getxcol.get_excel_columns, name='column_excel'),


]
