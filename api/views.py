from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import PromptSerializer
from .middle import name_to_model
from django.db import connection
from openai import OpenAI
client = OpenAI(api_key="sk-proj-XsFPegZDKVJjoJ4OjxwhT3BlbkFJUiZB2h5ZEuVN7DFPbv0Y")



def prompt_to_sql(prompt):
     # First GPT call to extract the table name from the user prompt
    response1 = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "Extract the table name from the user prompt out of one of the following: 'accounts_account' ,'contacts_contact','calls_call','leads_lead','meetings_meeting','opportunities_opportunity','interaction_interaction','tasks_tasks','channels_channel','reminder_reminder'','tenant_tenant','campaign_campaign','node_temps_node_temp','vendors_vendor','product_product','documents_document','dynamic_entities_dynamic_entitie','loyalty_loyalty','custom_fields_custom_field','tickets_ticket''stage_stage''reports_report'"},
            {"role": "user", "content": prompt}
        ],
        max_tokens=50,
        n=1,
        stop=None,
        temperature=0.7,
    )

    table_name = response1.choices[0].message.content.strip()

    # Second GPT call to get the model structure based on the table name
    model_structure = name_to_model(table_name)

    # Third GPT call to generate the SQL query based on user prompt and model structure
    response2 = client.chat.completions.create(
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

    sql_query = response2.choices[0].message.content.strip()
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
