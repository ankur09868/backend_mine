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
from rest_framework.routers import DefaultRouter


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
from reports import views as rpviews
from api import views as apiviews
from whatsapp_chat import views as whatsappview
from drafts import views as draftview
from wallet import views as wallview
from query.query_dispatch import dispatch
from upload_media import upload_dispatch as u_dispatch
from communication import insta_msg as imsg 
router = DefaultRouter()
router.register(r'instagram-campaigns', campview.InstagramCampaignViewSet)
router.register(r'whatsapp-campaigns',campview.WhatsAppCampaignViewSet)
router.register(r'email-campaigns', campview.EmailCampaignViewSet)
router.register(r'call-campaigns', caviews.CallCampaignViewSet)


urlpatterns = [
    #path('admin/', admin.site.urls),
    # User Registration
    path('register/', Reg.register, name='register'),  # Endpoint for user registration

    # User Authentication
    path('login/', Reg.LoginView.as_view(), name='login'),  # User login
    path('logout/', Reg.LogoutView.as_view(), name='logout'),  # User logout

    # Account Management
    path('accounts/', aviews.AccountListCreateAPIView.as_view(), name='account-list'),  # List and create accounts
    path('accounts/<int:pk>/', aviews.AccountDetailAPIView.as_view(), name='account-detail'),  # Retrieve, update, delete account by ID

    # Active Accounts
    path("active_accounts/", get_most_active_accounts, name="most-active-entities"),  # Get most active accounts

    # Lead Management
    path('leads/', lviews.LeadListCreateAPIView.as_view(), name='lead-list'),  # List and create leads
    path('leads/<int:pk>/', lviews.LeadDetailAPIView.as_view(), name='lead-detail'),  # Retrieve, update, delete lead by ID

    # Opportunity Management
    path('opportunities/', oviews.OpportunityListAPIView.as_view(), name='opportunity-list'),  # List and create opportunities
    path('opportunities/<int:pk>/', oviews.OpportunityDetailAPIView.as_view(), name='opportunity-detail'),  # Retrieve, update, delete opportunity by ID

    # Contact Management
    path('contacts/', cviews.ContactListCreateAPIView.as_view(), name='contact-list-create'),  # List and create contacts
    path('contacts/<int:pk>/', cviews.ContactDetailAPIView.as_view(), name='contact-detail'),  # Retrieve, update, delete contact by ID

    # Meeting Management
    path('meetings/', mviews.MeetingListCreateAPIView.as_view(), name='meeting-list-create'),  # List and create meetings
    path('meetings/<int:pk>/', mviews.MeetingDetailAPIView.as_view(), name='meeting-detail'),  # Retrieve, update, delete meeting by ID

    # Call Management
    path('calls/', caviews.callsListAPIView.as_view(), name='calls'),  # List calls
    path('calls/<int:pk>/', caviews.callsDetailAPIView.as_view(), name='calls-detail'),  # Retrieve, update, delete call by ID

    # Interaction Management
    path('interaction/', inviews.InteractionListAPIView.as_view(), name='interaction'),  # List interactions
    path('interaction/<int:pk>/', inviews.InteractionDetailAPIView.as_view(), name='interaction-detail'),  # Retrieve, update, delete interaction by ID

    # Task Management
    path('tasks/', tviews.TaskListCreateAPIView.as_view(), name='task-list'),  # List and create tasks
    path('tasks/<int:pk>/', tviews.TaskRetrieveUpdateDestroyAPIView.as_view(), name='task-detail'),  # Retrieve, update, delete task by ID

    # Reminder Management
    path('reminders/', rviews.ReminderListAPIView.as_view(), name='reminder-list'),  # List reminders
    path('reminder/<int:pk>/', rviews.ReminderDetailAPIView.as_view(), name='reminder-detail'),  # Retrieve, update, delete reminder by ID

    # Excel Data Upload
    path('uploadexcel/', ingex.ImportLeadData, name='excel'),  # Upload leads from Excel file
    path('excel-column/', getxcol.get_excel_columns, name='column_excel'),  # Get columns from Excel file

    # User Management
    path('get-user/<str:username>/', getuser.get_user_by_username, name='get_user'),  # Get user by username
    path('get-all-user/', getuser.get_all_users, name='get_all_user'),  # Get all users

    # Tenant Management
    path('createTenant/', tenview.tenant_list, name='tenant'),  # Create a new tenant
    path('getTenantDetail/<str:tenant_id>/', tenview.tenant_detail, name='tenant_details'),  # Create a new tenant

    # Campaign Management
    path('campaign/', campview.CampaignViewSet.as_view(), name='campaigns'),  # List and create campaigns
    path('campaign/<int:pk>/', campview.CampaignDetailAPIView.as_view(), name='campaigns'),  # Retrieve, update, delete campaign by ID
    path('campaign/stats/', campview.CampaignStatsAPIView.as_view(), name='campaign-stats'),  # Get campaign statistics

    # Node Template Management
    path('node-templates/', nviews.NodeTemplateListCreateAPIView.as_view(), name='node-template-list-create'),  # List and create node templates
    path('node-templates/<int:pk>/', nviews.NodeTemplateDetailAPIView.as_view(), name='node-template-detail'),  # Retrieve, update, delete node template by ID

    # CLTV Extraction
    path('extract_cltv/<int:entity_type_id>/', extract_cltv, name='extract_cltv'),  # Extract CLTV for given entity type

    # Report Management
    path('report/<str:report_id>/', oviews.get_report_by_id, name='get_report_by_id'),  # Get report by ID
    path('generate-report/', rpviews.generate_and_get_report_view, name='generate_report'),  # Generate and retrieve report
    path('retrieve-reports/', rpviews.retrieve_all_reports_view, name='retrieve_reports'),  # Retrieve all reports
    path('today/', rpviews.retrieve_today_report_view, name='retrieve_today_report'),  # Retrieve today's report
    path('yesterday/', rpviews.retrieve_yesterday_report_view, name='retrieve_yesterday_report'),  # Retrieve yesterday's report

    # Query Execution
    path('execute-query/', apiviews.ExecuteQueryView.as_view(), name='execute_query'),  # Execute custom query

    # WhatsApp Conversation Management
    path('whatsapp_convo_post/<str:contact_id>/', whatsappview.save_conversations, name='save_whatsapp_convo'),  # Save WhatsApp conversations
    path('whatsapp_convo_get/<str:contact_id>/', whatsappview.view_conversation, name='get_whatsapp_convo'),  # Get WhatsApp conversations
    path('unique_insta_profiles/', whatsappview.get_unique_instagram_contact_ids, name='get_all_insta'),  # Get unique Instagram contact IDs

    # Draft Management
    path('drafts/', draftview.DraftListCreateAPIView.as_view(), name='draft-list-create'),  # List and create drafts
    path('drafts/<int:id>/', draftview.DraftDetailAPIView.as_view(), name='draft-detail'),  # Retrieve, update, delete draft by ID

    # Contact by Account
    path('contacts_of_account/<int:account_id>/', cviews.ContactByAccountAPIView.as_view(), name='contacts-by-account'),  # Get contacts for specific account

    # Wallet Management
    path('wallet/recharge/', wallview.recharge_wallet, name='recharge_wallet'),  # Recharge wallet
    path('wallet/deduct/', wallview.deduct_from_wallet, name='deduct_from_wallet'),  # Deduct from wallet
    path('wallet/balance/', wallview.get_wallet_balance, name='get_wallet_balance'),  # Get wallet balance
    path('wallet/transactions/', wallview.get_last_n_transactions, name='get_wallet_balance'),  # Get last transactions

    # Generic Query
    path('query/', dispatch, name='query'),  # Generic query endpoint

    # File Upload
    path('upload/', u_dispatch.dispatcher, name='upload_dispatch'),  # Upload dispatcher

    # Message Saving
    path('save-messages/', imsg.save_messages, name='save-messages'),  # Save messages
    path('save-email-messages/', imsg.save_email_messages, name='save-email-messages'),  # Save email messages
    path('store-selected-emails/', simviews.store_selected_emails, name='store_selected_emails'),  # Store selected emails
    path('fetch-all-emails/', simviews.fetch_all_emails, name='fetch_all_emails'),  # Fetch all emails

    # Include Router URLs
    path('', include(router.urls)),  # Include individual campaign routing

]

