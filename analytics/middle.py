def name_to_model(modelName):
    if 'accounts_account'in modelName.lower():
        return """
            Name = models.CharField("Name of Account", max_length=64)
            email = models.EmailField()
            phone = models.CharField(max_length=20)
            industry = models.CharField("Industry Type", max_length=255, blank=True, null=True)
            website = models.URLField("Website", blank=True, null=True)
            description = models.TextField(blank=True, null=True)
            assigned_to = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='account_assigned_to', blank=True, null=True, on_delete=models.CASCADE)
            created_by = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='account_created_by', on_delete=models.CASCADE, blank=True, null=True)
            createdOn = models.DateTimeField("Created on", auto_now_add=True)
            is_active = models.BooleanField(default=False)
            company = models.CharField(max_length=100, default='Unknown')
            tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE )
            account_type = models.CharField(max_length=10, choices=ACCOUNT_TYPE_CHOICES, null=True)
            stage = models.CharField(max_length=20, choices=STAGE_CHOICES, blank=True, null=True)
            custom_fields = models.ForeignKey(CustomField, on_delete=models.CASCADE, null=True, blank=True, related_name='account_custom_fields')
        """
    elif 'contacts_contact'in modelName.lower():
        return """
    first_name = models.CharField("First name", max_length=255)
    last_name = models.CharField("Last name", max_length=255)
    account = models.ForeignKey(Account, related_name='lead_account_contacts', on_delete=models.CASCADE, blank=True, null=True)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    address = models.TextField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    createdBy = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='contact_created_by', on_delete=models.CASCADE)
    createdOn = models.DateTimeField("Created on", auto_now_add=True)
    isActive = models.BooleanField(default=False)
    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE)
    """
    elif 'calls_call'in modelName.lower():
        return """
    call_to = models.ForeignKey(Contact, on_delete=models.SET_NULL, related_name='call_to_meetings', blank=True, null=True, verbose_name='Contact Name')
    related_to = models.CharField(max_length=255, blank=True, null=True, verbose_name='Related To')
    call_type = models.CharField(max_length=255, blank=True, null=True, verbose_name='Call Type')
    outgoing_status = models.CharField(max_length=255, blank=True, null=True, verbose_name='Outgoing Status')
    start_time = models.DateTimeField(verbose_name='Start Time', blank=True, null=True)
    call_duration = models.DurationField(verbose_name='Call Duration', blank=True, null=True)
    location = models.CharField(max_length=255, blank=True, null=True, verbose_name='Location')
    voice_recording = models.CharField(max_length=255, blank=True, null=True, verbose_name='Voice Recording')
    to_time = models.DateTimeField(verbose_name='To', blank=True, null=True)
    createdBy = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='created_calls', on_delete=models.CASCADE, blank=True, null=True)
    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE)"""
    elif 'reports_report'in modelName.lower():
        return """ 
    created_at = models.DateTimeField(auto_now_add=True)
    leads_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    revenue = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    total_leads = models.IntegerField(default=0)"""
    elif 'documents_document'in modelName.lower():
        return """
    name = models.CharField('Document Name',max_length=600)
    document_type = models.CharField('Document Type',max_length=600)
    description = models.TextField('Description', blank=True)
    file_url = models.CharField('File URL', default='', max_length=600)
    # GenericForeignKey to associate with any entity
    entity_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, blank=True, null=True)
    entity_id = models.PositiveIntegerField(blank=True, null=True)
    entity = GenericForeignKey('entity_type', 'entity_id')
    uploaded_at = models.DateTimeField('Uploaded At', auto_now_add=True)
    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE)"""
    elif 'meetings_meeting'in modelName.lower():
        return """
    title = models.CharField(max_length=64, blank=True, null=True, verbose_name='Title')
    location = models.CharField(max_length=255, blank=True, null=True, verbose_name='Location')
    from_time = models.DateTimeField(verbose_name='From')
    to_time = models.DateTimeField(verbose_name='To')
    related_to = models.CharField(max_length=255, blank=True, null=True, verbose_name='Related To')
    contact_name = models.ForeignKey(Contact, related_name='meeting_contacts', blank=True, null=True, verbose_name='Contact Name', on_delete=models.CASCADE )
    host = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, related_name='meeting_hosts', blank=True, null=True, verbose_name='Host')
    participants = models.ForeignKey(Contact, related_name='meeting_participants', blank=True, on_delete=models.CASCADE)
    description = models.TextField(blank=True, null=True, verbose_name='Description')
    account = models.ForeignKey('accounts.Account', related_name='meetings', on_delete=models.CASCADE, blank=True, null=True)
    assigned_to = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, related_name='meeting_assigned_users',blank=True, null=True)
    createdBy = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='meeting_created_by', on_delete=models.CASCADE,blank=True, null=True)
    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE)"""
    elif 'leads_lead'in modelName.lower():
        return """LEAD_SOURCE = (
    ('call', 'Call'),
    ('email', 'Email'),
    ('existing customer', 'Existing Customer'),
    ('partner', 'Partner'),
    ('public relations', 'Public Relations'),
    ('compaign', 'Campaign'),
    ('other', 'Other'),
)

LEAD_STATUS = (
    ('assigned', 'Assigned'),
    ('in process', 'In Process'),
    ('converted', 'Converted'),
    ('recycled', 'Recycled'),
    ('dead', 'Dead')
)
PRIORITY_CHOICES = (
    ('High', 'High'),
    ('Medium', 'Medium'),
    ('Low', 'Low')
)
class leads_lead(models.Model):
    title = models.CharField("Treatment Pronouns for the customer", max_length=64, blank=True, null=True)
    first_name = models.CharField(("First name"), max_length=255)
    last_name = models.CharField(("Last name"), max_length=255)
    email = models.EmailField()
    phone = models.CharField(max_length=20, null=True, blank=True)
    account = models.ForeignKey(Account, related_name='Leads', on_delete=models.CASCADE, blank=True, null=True)
    stage = models.ForeignKey(Stage, on_delete=models.SET_NULL, null=True, blank=True)
    source = models.CharField("Source of Lead", max_length=255, blank=True, null=True, choices=LEAD_SOURCE)
    address = models.CharField("Address", max_length=255, blank=True, null=True)
    website = models.CharField("Website", max_length=255, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    assigned_to = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='lead_assigned_users')    
    account_name = models.CharField(max_length=255, null=True, blank=True)
    opportunity_amount = models.DecimalField("Opportunity Amount", decimal_places=2, max_digits=12,blank=True, null=True)
    createdBy = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='lead_created_by', on_delete=models.CASCADE)
    createdOn = models.DateTimeField("Created on", auto_now_add=True)
    isActive = models.BooleanField(default=False)
    enquery_type = models.CharField(max_length=255, blank=True, null=True)
    money = models.DecimalField("Money", decimal_places=2, max_digits=12, blank=True, null=True)
    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE)
    priority = models.CharField("Lead Priority", max_length=6, blank= True, null= True, choices=PRIORITY_CHOICES )"""
    elif 'opportunities_opportunity'in modelName.lower():
        return """
    STAGES = (
    ('QUALIFICATION', 'QUALIFICATION'),
    ('NEEDS ANALYSIS', 'NEEDS ANALYSIS'),
    ('VALUE PROPOSITION', 'VALUE PROPOSITION'),
    ('ID.DECISION MAKERS', 'ID.DECISION MAKERS'),
    ('PERCEPTION ANALYSIS', 'PERCEPTION ANALYSIS'),
    ('PROPOSAL/PRICE QUOTE', 'PROPOSAL/PRICE QUOTE'),
    ('NEGOTIATION/REVIEW', 'NEGOTIATION/REVIEW'),
    ('CLOSED WON', 'CLOSED WON'),
    ('CLOSED LOST', 'CLOSED LOST'),
)

SOURCES = (
    ('NONE', 'NONE'),
    ('CALL', 'CALL'),
    ('EMAIL', ' EMAIL'),
    ('EXISTING CUSTOMER', 'EXISTING CUSTOMER'),
    ('PARTNER', 'PARTNER'),
    ('PUBLIC RELATIONS', 'PUBLIC RELATIONS'),
    ('CAMPAIGN', 'CAMPAIGN'),
    ('WEBSITE', 'WEBSITE'),
    ('OTHER', 'OTHER'),
)



TYPECHOICES = (
    ('CUSTOMER', 'CUSTOMER'),
    ('INVESTOR', 'INVESTOR'),
    ('PARTNER', 'PARTNER'),
    ('RESELLER', 'RESELLER'),
)

INDCHOICES = (
    ('ADVERTISING', 'ADVERTISING'),
    ('AGRICULTURE', 'AGRICULTURE'),
    ('APPAREL & ACCESSORIES', 'APPAREL & ACCESSORIES'),
    ('AUTOMOTIVE', 'AUTOMOTIVE'),
    ('BANKING', 'BANKING'),
    ('BIOTECHNOLOGY', 'BIOTECHNOLOGY'),
    ('BUILDING MATERIALS & EQUIPMENT', 'BUILDING MATERIALS & EQUIPMENT'),
    ('CHEMICAL', 'CHEMICAL'),
    ('COMPUTER', 'COMPUTER'),
    ('EDUCATION', 'EDUCATION'),
    ('ELECTRONICS', 'ELECTRONICS'),
    ('ENERGY', 'ENERGY'),
    ('ENTERTAINMENT & LEISURE', 'ENTERTAINMENT & LEISURE'),
    ('FINANCE', 'FINANCE'),
    ('FOOD & BEVERAGE', 'FOOD & BEVERAGE'),
    ('GROCERY', 'GROCERY'),
    ('HEALTHCARE', 'HEALTHCARE'),
    ('INSURANCE', 'INSURANCE'),
    ('LEGAL', 'LEGAL'),
    ('MANUFACTURING', 'MANUFACTURING'),
    ('PUBLISHING', 'PUBLISHING'),
    ('REAL ESTATE', 'REAL ESTATE'),
    ('SERVICE', 'SERVICE'),
    ('SOFTWARE', 'SOFTWARE'),
    ('SPORTS', 'SPORTS'),
    ('TECHNOLOGY', 'TECHNOLOGY'),
    ('TELECOMMUNICATIONS', 'TELECOMMUNICATIONS'),
    ('TELEVISION', 'TELEVISION'),
    ('TRANSPORTATION', 'TRANSPORTATION'),
    ('VENTURE CAPITAL', 'VENTURE CAPITAL'),
)

class opportunities_opportunity(models.Model):
    name = models.CharField(max_length=64)
    account = models.ForeignKey(Account, related_name='opportunities', on_delete=models.CASCADE, blank=True, null=True)
    stage = models.CharField( max_length=64, choices=STAGES)
    stage = models.ForeignKey(Stage, on_delete=models.SET_NULL, null=True, blank=True)
    amount = models.DecimalField("Opportunity Amount", decimal_places=2, max_digits=12, blank=True, null=True)
    lead_source = models.CharField("Source of Lead", max_length=255, choices=SOURCES, blank=True, null=True)
    probability = models.IntegerField(default=0, blank=True, null=True)
    contacts = models.ForeignKey(Contact, related_name='opportunity', on_delete=models.CASCADE, blank=True, null=True)
    closedBy = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True)
    closedOn = models.DateTimeField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    createdBy = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='opportunity_created_by', on_delete=models.CASCADE)
    createdOn = models.DateTimeField("Created on", auto_now_add=True)
    isActive = models.BooleanField(default=False)
    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE)"""
    elif 'interaction_interaction'in modelName.lower():
        return """
        INTERACTION_TYPES = (
        ('Call', 'Call'),
        ('Email', 'Email'),
        ('Meeting', 'Meeting'),
        ('Note', 'Note'),
       
    )

    entity_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    entity_id = models.PositiveIntegerField()
    entity = GenericForeignKey('entity_type', 'entity_id')
    
    interaction_type = models.CharField(max_length=50, choices=INTERACTION_TYPES)
    interaction_datetime = models.DateTimeField()
    notes = models.TextField(blank=True, null=True)
    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE)"""
    elif 'tasks_tasks'in modelName.lower():
        return """ 
        STATUS_CHOICES = (
        ('not_started', 'Not Started'),
        ('deferred', 'Deferred'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
        ('waiting_for_input', 'Waiting for Input'),
    )

    PRIORITY_CHOICES = (
        ('high', 'High'),
        ('normal', 'Normal'),
        ('low', 'Low'),
    )

    subject = models.CharField(max_length=255)
    due_date = models.DateField()
    createdBy = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='task_created_by', on_delete=models.CASCADE)
    contact = models.ForeignKey(Contact, related_name='contact_tasks', on_delete=models.CASCADE, blank=True, null=True)
    account = models.ForeignKey(Account, related_name='account_tasks', on_delete=models.CASCADE, blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='not_started')
    priority = models.CharField(max_length=10, choices=PRIORITY_CHOICES, default='normal')
    reminder = models.BooleanField(default=False)
    description = models.TextField()
    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE)
    assigned_to = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='task_assigned_to', on_delete=models.CASCADE, blank=True, null=True)"""
    elif 'tenant_tenant'in modelName.lower():
        return """
    id = models.CharField(primary_key=True, max_length=50)
    organization=models.CharField(max_length=100)
    db_user = models.CharField(max_length=100)
    db_user_password = models.CharField(max_length=100)"""
    elif 'campaign_campaign'in modelName.lower():
        return """
    campaign_owner = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='campaign_created_by', on_delete=models.CASCADE,blank=True, null=True)
    campaign_name = models.CharField(max_length=255)
    start_date = models.DateField()
    end_date = models.DateField()
    expected_revenue = models.DecimalField(max_digits=10, decimal_places=2)
    actual_cost = models.DecimalField(max_digits=10, decimal_places=2)
    numbers_sent = models.IntegerField()
    type = models.CharField(max_length=50, choices=[('None', 'None'), ('Email', 'Email'), ('SMS', 'SMS')])
    status = models.CharField(max_length=50, choices=[('None', 'None'), ('Active', 'Active'), ('Completed', 'Completed'), ('Cancelled', 'Cancelled')])
    budgeted_cost = models.DecimalField(max_digits=10, decimal_places=2)
    expected_response = models.DecimalField(max_digits=5, decimal_places=2)
    description = models.TextField()
    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE,default=3)"""
    elif 'tickets_ticket'in modelName.lower():
        return """ 
        CASE_STATUS_CHOICES = [
        ('open', 'Open'),
        ('closed', 'Closed'),
        ('pending', 'Pending'),
    ]

    PRIORITY_CHOICES = [
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
    ]
    TYPE_CHOICES = [
        ('issue', 'Issue'),
        ('request', 'Request'),
        ('bug', 'Bug'),
    ]
    CASE_ORIGIN_CHOICES = [
        ('phone', 'Phone'),
        ('email', 'Email'),
        ('web', 'Web'),
        ('social_media', 'Social Media'),
    ]

    casenumber = models.CharField(max_length=100, unique=True)
    subject = models.CharField(max_length=200)
    description = models.TextField()
    webemail = models.EmailField(max_length=254)
    case_reason = models.CharField(max_length=200) 
    status = models.CharField(max_length=20, choices=CASE_STATUS_CHOICES)
    date = models.DateField()
    owner = models.CharField(max_length=100)
    contact = models.ForeignKey(Contact, related_name='Ticket', on_delete=models.CASCADE, blank=True, null=True)
    account = models.ForeignKey(Account, related_name='Ticket', on_delete=models.CASCADE, blank=True, null=True)
    priority = models.CharField(max_length=20, choices=PRIORITY_CHOICES)
    type = models.CharField(max_length=20, choices=TYPE_CHOICES) 
    case_origin = models.CharField(max_length=20, choices=CASE_ORIGIN_CHOICES)
    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE)
"""
    elif 'product_product' in modelName.lower():
        return"""
    product_owner = models.CharField(max_length=100)
    product_name = models.CharField(max_length=100)
    product_code = models.CharField(max_length=50, unique=True)
    vendor_name = models.CharField(max_length=100, null=True)
    product_active = models.BooleanField(default=True)
    manufacturer = models.CharField(max_length=100)
    product_category = models.CharField(max_length=100)
    sales_start_date = models.DateField(null=True, blank=True)
    sales_end_date = models.DateField(null=True, blank=True)
    support_start_date = models.DateField(null=True, blank=True)
    support_end_date = models.DateField(null=True, blank=True)
    unit_price = models.CharField(max_length=200, null=True, blank=True)
    commission_rate = models.DecimalField(max_digits=5, decimal_places=2)
    tax = models.DecimalField(max_digits=5, decimal_places=2)
    is_taxable = models.BooleanField(default=False)
    usage_unit = models.CharField(max_length=50)
    qty_ordered = models.PositiveIntegerField(default=0)
    reorder_level = models.PositiveIntegerField(default=0)
    quantity_in_stock = models.PositiveIntegerField(default=0)
    handler = models.CharField(max_length=100)
    quantity_in_demand = models.PositiveIntegerField(default=0)
    description = models.TextField(blank=True)
    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE)
"""
    elif 'stage_stage'in modelName.lower():
        return"""
    status = models.CharField(max_length=64)
    model_name = models.CharField(max_length=20, choices=MODEL_CHOICES)
    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE)
"""
    elif 'loyalty_loyalty' in modelName.lower():
        return"""
    LOYALTY_PROGRAMS = (
        ('Promo Code', 'Promo Code'),
        ('Loyalty Cards', 'Loyalty Cards'),
        ('Fidelity Cards', 'Fidelity Cards'),
        ('Promotional Program', 'Promotional Program'),
        ('Coupons', 'Coupons'),
        ('2+1 Free', '2+1 Free'),
        ('Next Order Coupons' , 'Next Order Coupons')
    )
    CURRENCY_CHOICES = (
    ('USD', 'US Dollar'),
    ('EUR', 'Euro'),
    ('GBP', 'British Pound'),
    ('JPY', 'Japanese Yen'),
    ('INR', 'Indian Rupee'),
)

    entity_id = models.PositiveIntegerField()
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    entity = GenericForeignKey('content_type' , 'entity_id')
    
    loyalty_program = models.CharField(max_length=50, choices=LOYALTY_PROGRAMS)
    contacts = models.ForeignKey(Contact, on_delete=models.CASCADE)
    currency = models.CharField(max_length=3, choices=CURRENCY_CHOICES, default='INR')
    points_unit = models.IntegerField(default=0),
    start_date = models.DateField(),
    end_date = models.DateField(),
    company = models.CharField(max_length=50),
    website = models.URLField(blank=True, null=True)
"""
    else:
        raise ValueError('Prompt could not be translated to SQL query.')