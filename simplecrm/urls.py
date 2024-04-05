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

from accounts import views as aviews 
from leads import views as lviews
from opportunities import views as oviews
from contacts import views as cviews
from meetings import views as mviews
from calls import views as caviews

urlpatterns = [
    path('admin/', admin.site.urls),
    path(r'accounts/', aviews.AccountListAPIView.as_view(), name='account-list'),
    path('accounts/<int:pk>/', aviews.AccountListAPIView.as_view(), name='account-detail'),
    path(r'leads/', lviews.LeadListAPIView.as_view(), name='lead-list'),
    path(r'opportunities/', oviews.OpportunityListAPIView.as_view(), name='opportunity-list'),
    path(r'contacts/', cviews.ContactListAPIView.as_view(), name='contact-list'),
    path('meetings/', mviews.MeetingListAPIView.as_view(), name='meeting-list'),
    path('calls/', caviews.callsListAPIView.as_view(), name='calls'),   
]
