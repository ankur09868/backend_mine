from stage.models import Stage

DEFAULT_LEAD_STAGES = [
    {'stage': 'assigned'},
    {'stage': 'in process'},
    {'stage': 'converted'},
    {'stage': 'recycled'},
    {'stage': 'dead'}
]

DEFAULT_OPPORTUNITY_STAGES = [
    {'stage': 'QUALIFICATION'},
    {'stage': 'NEEDS ANALYSIS'},
    {'stage': 'VALUE PROPOSITION'},
    {'stage': 'ID.DECISION MAKERS'},
    {'stage': 'PERCEPTION ANALYSIS'},
    {'stage': 'PROPOSAL/PRICE QUOTE'},
    {'stage': 'NEGOTIATION/REVIEW'},
    {'stage': 'CLOSED WON'},
    {'stage': 'CLOSED LOST'}
]

def get_or_create_default_stages(tenant, model_name):
    default_stages = []

    if model_name == 'lead':
        default_stages = DEFAULT_LEAD_STAGES
    elif model_name == 'opportunity':
        default_stages = DEFAULT_OPPORTUNITY_STAGES
    else:
        return  # Handle other models if needed

    stages = Stage.objects.filter(tenant=tenant, model_name=model_name)
    existing_stage_names = set(stages.values_list('status', flat=True))

    for stage in default_stages:
        if stage['stage'] not in existing_stage_names:
            Stage.objects.create(status=stage['stage'], model_name=model_name, tenant=tenant)

    # Retrieve all stages after creation
    stages = Stage.objects.filter(tenant=tenant, model_name=model_name)
    return stages
