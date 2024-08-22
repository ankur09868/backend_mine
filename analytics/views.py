from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import PromptSerializer
from .middle import name_to_model
from django.db import connection
from openai import OpenAI
import os
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def prompt_to_sql(prompt):
    # First GPT call to extract the table name from the user prompt
    response1 = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "Extract the table name from the user prompt out of one of the following: 'accounts_account' ,'contacts_contact','interaction_calls','leads_lead','interaction_meetings','opportunities_opportunity','interaction_interaction','tasks_tasks','channels_channel','reminder_reminder'','tenant_tenant','campaign_campaign','node_temps_node_temp','vendors_vendors','product_product','documents_document','dynamic_entities_dynamicmodel','loyalty_loyalty','custom_fields_custom_field','tickets_ticket','stage_stage','lead_report','campaign_campaign','campaign_instagramcampaign','campaign_whatsappcampaign','campaign_emailcampaign'"},
            {"role": "user", "content": prompt}
        ],
        max_tokens=50,
        n=1,
        stop=None,
        temperature=0.7,
    )

    table_name = response1.choices[0].message.content.strip()
    print(table_name)

    # First GPT call to determine if the prompt is asking for the stage with the most leads or opportunities
    response2 = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {
                "role": "system",
                "content": (
                    "You are an assistant that determines whether a user prompt is asking for the stage with the most "
                    "number of leads or opportunities. If the prompt is asking for this, respond with 'yes', otherwise respond with 'no'."
                    "If the prompt have only leads or lead respond no only"
                    "If the prompt other than stage with the most return no like 'leads with assigned'and 'opportunity with qualification'"
                ),
            },
            {"role": "user", "content": prompt},
        ],
        max_tokens=50,
        n=1,
        stop=None,
        temperature=0.7,
    )

    is_stage_most_leads_or_opportunities = response2.choices[0].message.content.strip().lower()
    print(is_stage_most_leads_or_opportunities)

    # If the prompt is asking for the stage with the most leads or opportunities
    if 'yes' in is_stage_most_leads_or_opportunities:
        # Determine if the prompt is specifically about leads, opportunities, or both
        if 'lead' in prompt.lower():
            sql_query = (
                "SELECT stage_stage.status, COUNT(leads_lead.stage_id) as lead_count "
                "FROM leads_lead "
                "JOIN stage_stage ON leads_lead.stage_id = stage_stage.id "
                "WHERE stage_stage.model_name = 'lead' "
                "GROUP BY stage_stage.status "
                "ORDER BY lead_count DESC "
                "LIMIT 1;"
            )
        elif 'opportunity' in prompt.lower():
            sql_query = (
                "SELECT stage_stage.status, COUNT(opportunities_opportunity.stage_id) as opportunity_count "
                "FROM opportunities_opportunity "
                "JOIN stage_stage ON opportunities_opportunity.stage_id = stage_stage.id "
                "WHERE stage_stage.model_name = 'opportunity' "
                "GROUP BY stage_stage.status "
                "ORDER BY opportunity_count DESC "
                "LIMIT 1;"
            )
        else:
            # Handle the case where both leads and opportunities are mentioned
            sql_query = (
                "SELECT stage_stage.status, "
                "SUM(CASE WHEN leads_lead.stage_id IS NOT NULL THEN 1 ELSE 0 END) as lead_count, "
                "SUM(CASE WHEN opportunities_opportunity.stage_id IS NOT NULL THEN 1 ELSE 0 END) as opportunity_count "
                "FROM stage_stage "
                "LEFT JOIN leads_lead ON leads_lead.stage_id = stage_stage.id "
                "LEFT JOIN opportunities_opportunity ON opportunities_opportunity.stage_id = stage_stage.id "
                "WHERE stage_stage.model_name IN ('lead', 'opportunity') "
                "GROUP BY stage_stage.status "
                "ORDER BY (lead_count + opportunity_count) DESC "
                "LIMIT 1;"
            )
        
        print(f"Generated SQL query for most leads/opportunities in stage: {sql_query}")
        return sql_query

    # Second check: Handle special cases where only leads or opportunities are mentioned in the prompt
    elif 'lead' in table_name.lower() or 'opportunity' in table_name.lower():
        # Determine the model name based on the table name
        model_name = 'lead' if 'lead' in table_name.lower() else 'opportunity'
        stage_model_structure = name_to_model('stage_stage')
        table_model_structure = name_to_model(table_name)

        # Third GPT call to generate the SQL query specifically for leads_lead or opportunity
        response_sql = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {
                    "role": "system",
                    "content": (
                        f"RESPOND ONLY WITH THE SQL QUERY without padding or anything. "
                        f"Prompt have total number of count{prompt}then count"
                        f"Generate a PostgreSQL query for the '{table_name}' table. The query should join with the 'stage_stage' table "
                        f"to get the status of {model_name}s. The prompt is: {prompt}\n\n"
                        f"to retrieve the status for {model_name}s. Only include the following fields: all fields from '{table_name}' "
                        f"and the 'status' field from 'stage_stage'. Exclude the 'model_name' field in the result.\n\n"
                        f"Model Structure for {table_name}:\n\n{table_model_structure}\n\n"
                        f"Model Structure for stage_stage:\n\n{stage_model_structure}"
                    ),
                },
                {"role": "user", "content": prompt}
            ],
            max_tokens=1024,
            n=1,
            stop=None,
            temperature=0.7,
        )

        sql_query = response_sql.choices[0].message.content.strip()
        print(f"Generated SQL query for {table_name}: {sql_query}")
        return sql_query


    # Fourth GPT call to get the model structure based on the table name
    model_structure = name_to_model(table_name)

    # Fifth GPT call to generate the SQL query based on user prompt and model structure
    response3 = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": f"RESPOND ONLY WITH THE SQL QUERY without padding or anything.You are a postgresql expert and reply with ONLY THE SQL QUERY.Convert the following natural language request to a PostgreSQL query for {table_name}:\n\n{prompt}\n\nModel Structure:\n\n{model_structure}"},
            {"role": "user", "content": prompt}
        ],
        max_tokens=1024,
        n=1,
        stop=None,
        temperature=0.7,
    )

    sql_query = response3.choices[0].message.content.strip()
    print(sql_query)
    return sql_query

class ExecuteQueryView(APIView):
    serializer_class = PromptSerializer

    def post(self, request, format=None):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            prompt = serializer.validated_data.get('prompt')

            try:
                sql_query = prompt_to_sql(prompt)

                with connection.cursor() as cursor:
                    cursor.execute(sql_query)
                    columns = [col[0] for col in cursor.description]
                    results = [
                        dict(zip(columns, row))
                        for row in cursor.fetchall()
                    ]
                    return Response(results, status=status.HTTP_200_OK)

            except ValueError as e:
                return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

            except Exception as e:
                return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
