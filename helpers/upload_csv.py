import os, json
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from .tables import get_db_connection, table_mappings
from openai import OpenAI

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=OPENAI_API_KEY)

def get_tableFields(table_name):
    query = f"SELECT * FROM {table_name} LIMIT 0"  # Use LIMIT 0 to avoid fetching actual data
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(query)
        
        column_names = [desc[0] for desc in cursor.description]
    finally:
        cursor.close()
        conn.close()
    
    return column_names


def mappingFunc(list1, list2):
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are a helpful assistant who answers STRICTLY to what is asked, based on the info provided. DO NOT ADD DATA FROM THE INTERNET. YOU KNOW NOTHING ELSE EXCEPT THE DATA BEING PROVIDED TO YOU. Keep your answers concise and only the required information"},
            {"role": "user", "content": f"map these two lists with each other. List1: {list1}, List2: {list2} Return only the mapped dictionary in json."}
        ]
    )
    return response.choices[0].message.content

@csrf_exempt
def upload_file(request, df):
    if request.method == 'POST':
        try:
            print("entering upload file")
            print("df: ", df[:1])
            
            model_name = request.POST.get('model_name')
            xls_file = request.FILES.get('file')
            tenant_id = request.headers.get('X-Tenant-Id')
            
            print("rcvd model_name: ", model_name)
            
            if not (xls_file.name.endswith('.xls') or xls_file.name.endswith('.xlsx') or xls_file.name.endswith('.csv')):
                return JsonResponse({"error": "File is not in XLS/XLSX format"}, status=400)

            if model_name:
                table_name = table_mappings.get(model_name)
                field_names = get_tableFields(table_name)
                column_names = df.columns.tolist()
                
                try:
                    field_mapping = mappingFunc(column_names, field_names)
                except Exception as e:
                    return JsonResponse({"error": f"Error mapping fields: {e}"}, status=500)
                print("openai response: " ,field_mapping)
                start = field_mapping.find('{')
                end = field_mapping.find('}')
                field_mapping=  field_mapping[start:end + 1]

                field_mapping_json = json.loads(field_mapping)
                print(field_mapping_json.values())
                df_new = df.rename(columns=field_mapping_json)

            else:
                file_name = os.path.splitext(xls_file.name)[0]
                table_name = file_name.lower().replace(' ', '_')  # Ensure table name is lowercase and replace spaces with underscores

            headers = df_new.columns.tolist()
            print("headers:", df_new)
            data = df_new.values.tolist()
            print("data: ", data[0])

            column_definitions = ', '.join(f'"{header}" VARCHAR(255)' for header in headers)
            
            create_table_query = f"""
                CREATE TABLE IF NOT EXISTS "{table_name}" (
                    id SERIAL PRIMARY KEY,
                    {column_definitions},
                    "tenant_id" VARCHAR(255)
                );
            """

            conn = get_db_connection()
            cur = conn.cursor()
            
            try:
                cur.execute(create_table_query)
                conn.commit()
                print("table created/found")

                for row in data:
                    values = list(row) + [tenant_id]
                    insert_query = f"""
                        INSERT INTO "{table_name}" ({', '.join(f'"{header}"' for header in headers)}, "tenant_id") 
                        VALUES ({', '.join('%s' for _ in range(len(headers)))}, %s);
                    """

                    print("Final Values: ", values)
                    print("row: " ,row)
                    cur.execute(insert_query, values)
                    print("Row created")
                    conn.commit()

                return JsonResponse({"message": "XLS file uploaded and data inserted successfully", "table_name": table_name}, status=200)

            except Exception as e:
                conn.rollback()
                return JsonResponse({"error": f"Error inserting data: {e}"}, status=500)

            finally:
                cur.close()
                conn.close()

        except Exception as e:
            return JsonResponse({"error": f"Unexpected error: {e}"}, status=500)

    return JsonResponse({"error": "Invalid request method"}, status=405)
