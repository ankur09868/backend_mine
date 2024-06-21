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
from simplecrm import get_user as getuser
from tenant import views as tenview
from campaign import views as campview
from interaction.active_account import get_most_active_accounts
from node_temps import views as nviews
from interaction.views import extract_cltv
from simplecrm import recent_request as rr
from interaction.active_account import get_most_active_accounts
from interaction.active_account import get_most_active_contacts
from interaction.active_account import get_lead_summation
from vendors import views as vendview
from product import views as prodview
from documents import views as docview
from dynamic_entities import views as dyv
# from loyalty import views as lv
from simplecrm import views as simviews
from simplecrm import tracking as track
from custom_fields import views as cfviews
from simplecrm import tractcount as trac
from tickets import views as tickview
from stage import views as sviews


urlpatterns = [
    #path('admin/', admin.site.urls),
    path('register/', Reg.register, name='register'),  # Endpoint for user registration
    path('login/', Reg.LoginView.as_view(), name='login'), 
    path(r'accounts/', aviews.AccountListCreateAPIView.as_view(), name='account-list'),
    path('accounts/<int:pk>/', aviews.AccountDetailAPIView.as_view(), name='account-detail'),
    path("active_accounts/",get_most_active_accounts, name="most-active-entites"),
    path(r'leads/', lviews.LeadListCreateAPIView.as_view(), name='lead-list'),
    path('leads/<int:pk>/',lviews.LeadDetailAPIView.as_view(), name='lead-detail'),
    path(r'opportunities/', oviews.OpportunityListAPIView.as_view(), name='opportunity-list'),
    path('opportunities/<int:pk>/', oviews.OpportunityDetailAPIView.as_view(), name='opportunity-detail'),
    path('contacts/', cviews.ContactListCreateAPIView.as_view(), name='contact-list-create'),
    path('contacts/<int:pk>/', cviews.ContactDetailAPIView.as_view(), name='contact-detail'),
    path('contacts/', cviews.ContactDetailAPIView.as_view(), name='contact-detail'),
    path('meetings/', mviews.MeetingListCreateAPIView.as_view(), name='meeting-list-create'),
    path('meetings/<int:pk>/', mviews.MeetingDetailAPIView.as_view(), name='meeting-detail'),
    path('calls/', caviews.callsListAPIView.as_view(), name='calls'), 
    path('calls/<int:pk>/', caviews.callsDetailAPIView.as_view(), name='calls-detail'),
    path('interaction/', inviews.InteractionListAPIView.as_view(), name='interaction'),  
    path('interaction/<int:pk>/',inviews.InteractionDetailAPIView.as_view(), name='interaction-detail'),
    path('tasks/', tviews.TaskListCreateAPIView.as_view(), name='task-list'),
    path('tasks/<int:pk>/', tviews.TaskRetrieveUpdateDestroyAPIView.as_view(), name='task-detail'), 
    path('reminders/', rviews.ReminderListAPIView.as_view(), name='reminder-list'),
    path('reminder/<int:pk>/', rviews.ReminderDetailAPIView.as_view(), name='reminder-detail'), 
    path('uploadexcel/', ingex.ImportLeadData, name='excel'),
    path('excel-column/', getxcol.get_excel_columns, name='column_excel'),
    path('get-user/<str:username>/', getuser.get_user_by_username, name='get_user'),
    path('get-all-user/', getuser.get_all_users, name='get_all_user'),
    path('createTenant/', tenview.tenant_list, name='tenant'),
    path('logout/', Reg.LogoutView.as_view(), name='logout'),
    path('campaign/', campview.CampaignViewSet.as_view(), name='campaigns'),
    path('campaign/<int:pk>/', campview.CampaignDetailAPIView.as_view(), name='campaigns'),
    path(r'node-templates/', nviews.NodeTemplateListCreateAPIView.as_view(), name='node-template-list-create'),
    path('node-templates/<int:pk>/', nviews.NodeTemplateDetailAPIView.as_view(), name='node-template-detail'),
    path('extract_cltv/<int:entity_type_id>/', extract_cltv, name='extract_cltv'),
    path ('report/<str:report_id>/', oviews.get_report_by_id, name='get_report_by_id'),
    path('recent_request/<str:model_name>/',rr.recent_request, name='recent_request'),
    path("active_accounts/",get_most_active_accounts, name="most-active-entites"),
    path("active_contacts/",get_most_active_contacts, name="most-active-entites"),
    path("leads_sum/",get_lead_summation, name="most-active-entites"),
    path('products/', prodview.ProductListAPIView.as_view(), name='products-list'),
    path('product/<int:pk>/', prodview.ProductDetailAPIView.as_view(), name='product-detail'),
    path('vendors', vendview.VendorsListAPIView.as_view(), name='vendors-list'),
    path('vendor/<int:pk>', vendview.VendorDetailAPIView.as_view(), name='vendor-detail'),
    path('documents/', docview.DocumentListAPIView.as_view(), name='vendors-list'),
    path('documents/<int:pk>/', docview.DocumentDetailAPIView.as_view(), name='vendor-detail'),
    path('return-documents/<int:entity_type>/<int:entity_id>/', docview.RetrieveDocumentsView.as_view(), name='retrieve-documents'),
    path('return-documents/<int:entity_type>/', docview.RetrieveDocumentsView.as_view(), name='retrieve-documents'),    
    path('create-dynamic-model/', dyv.CreateDynamicModelView.as_view(), name='create_dynamic_model'),
    path('dynamic-models/', dyv.DynamicModelListView.as_view(), name='dynamic_model_list'),
    path('dynamic-model-data/<str:model_name>/', dyv.DynamicModelDataView.as_view(), name='dynamic_model_data'),
    path('delete-dynamic-model/<str:model_name>/', dyv.DeleteDynamicModelView.as_view(), name='delete_dynamic_model'),
    path('return-interaction/<int:entity_type>/<int:entity_id>/', inviews.RetrieveInteractionsView.as_view(), name='retrieve-interaction'),
    path('return-interaction/<int:entity_type>/', inviews.RetrieveInteractionsView.as_view(), name='retrieve-interaction'),    
    path('deduplicate/', simviews.deduplicate_view, name='deduplicate'),
    path('create-custom-field/', cfviews.create_custom_field, name='create_custom_field'),
    path('user/<int:user_id>/tasks/', tviews.UserTasksListAPIView.as_view(), name='user-tasks-list'),
    path('track_open/<int:contact_id>/', track.TrackOpenView.as_view(), name='track_open'),
    path('track_open_count/', trac.TrackOpenCountView.as_view(), name='track_open_count'),
    path('tickets/', tickview.TicketListAPIView.as_view(), name='ticket-list'),
    path('tickets/<int:pk>/', tickview.TicketDetailAPIView.as_view(), name='ticket-detail'),
    path('stage/list/<str:model_name>/', sviews.stage_list, name='stage-list'),#stage
    path('stage/create/', sviews.stage_create, name='stage-create'),
    path('stage/update/<int:stage_id>/', sviews.stage_update, name='stage-update'),
    path('stage/delete/<int:stage_id>/', sviews.stage_delete, name='stage-delete'),
    path('opportunity/<int:opportunity_id>/stage/', oviews.opportunity_stage, name='opportunity_stage'),
    path('lead/<int:lead_id>/stage/', lviews.lead_stage, name='lead_stage'), 
    path('lead/stage/', lviews.all_stages, name='all_lead_stage'), 
    path('opportunity/stage/', oviews.all_stages, name='all_opportunity_stage'), 
    
]

