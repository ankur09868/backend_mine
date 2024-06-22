from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import PromptSerializer
from django.db import connection

def prompt_to_sql(prompt):
    if 'all accounts' in prompt.lower():
        return 'SELECT * FROM accounts_account;'
    elif 'contact'in prompt.lower():
        return 'SELECT * FROM contacts_contact;'
    elif 'calls'in prompt.lower():
        return 'SELECT * FROM calls_calls;'
    elif 'leads'in prompt.lower():
        return 'SELECT * FROM leads_lead;'
    elif 'all interactions' in prompt.lower():
        return 'SELECT * FROM interaction_interaction;'
    elif 'report' in prompt.lower():
        return 'SELECT * FROM reports_report;'
    elif 'opportunities' in prompt.lower():
        return 'SELECT * FROM opportunities_opportunity;'
    elif 'ticket' in prompt.lower():
        return 'SELECT * FROM tickets_ticket;'
    else:
        raise ValueError('Prompt could not be translated to SQL query.')

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
