import csv, pandas as pd, os
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from .tables import get_db_connection

@csrf_exempt
def upload_csv(request, df):
    if request.method == 'POST':
        print("entering upload xls")
        print("df: " ,df[:1])
        model_name = request.POST.get('model_name')
        csv_file = request.FILES.get('file')
        tenant_id = request.headers.get('X-Tenant-Id')
        if not csv_file or not csv_file.name.endswith('.csv'):
            return JsonResponse({"error": "File is not in CSV format"}, status=400)
        # table_name = request.POST.get('table_name', None)
        
        if not model_name:
            file_name = os.path.splitext(csv_file.name)[0]
            table_name = file_name.lower().replace(' ', '_')  # Ensure table name is lowercase and replace spaces with underscores
        else:
            table_name = model_name
        # Try reading the CSV file with different encodings
        try:
            try:
                csv_data = csv.reader(csv_file.read().decode('utf-8').splitlines())
            except UnicodeDecodeError:
                csv_file.seek(0)  # Reset file pointer to the beginning
                csv_data = csv.reader(csv_file.read().decode('latin1').splitlines())
        except Exception as e:
            return JsonResponse({"error": f"Failed to read CSV file: {e}"}, status=500)
        
        # Extract headers from the CSV file
        headers = next(csv_data, None)
        if headers is None:
            return JsonResponse({"error": "CSV file is empty"}, status=400)
        
        # Generate column names and their types (assuming VARCHAR(255) for simplicity)
        column_definitions = ', '.join(f'"{header}" VARCHAR(255)' for header in headers)

        # Create the table dynamically
        create_table_query = f"""
            CREATE TABLE IF NOT EXISTS "{table_name}" (
                id SERIAL PRIMARY KEY,
                {column_definitions}
            );
        """
        # Connect to the PostgreSQL database
        conn = get_db_connection()
        cur = conn.cursor()

        try:
            # Create the table
            cur.execute(create_table_query)
            conn.commit()

            # Insert data into the table
            for row in csv_data:
                # Prepare the INSERT query dynamically based on headers
                insert_query = f"""
                    INSERT INTO "{table_name}" ({', '.join(f'"{header}"' for header in headers)}, tenant_id) 
                    VALUES ({', '.join('%s' for _ in range(len(headers)))},{tenant_id})
                """
                cur.execute(insert_query, row)
                print("row  created")
            conn.commit()

            return JsonResponse({"message": "CSV file uploaded and data inserted successfully", "table_name": table_name}, status=200)
        
        except Exception as e:
            conn.rollback()
            return JsonResponse({"error": f"Error during database operation: {e}"}, status=500)
        
        finally:
            cur.close()
            conn.close()

    return JsonResponse({"error": "Invalid request method"}, status=405)


@csrf_exempt
def upload_xls(request, df):
    if request.method == 'POST':
        print("entering upload xls")
        print("df: " ,df[:1])
        model_name = request.POST.get('model_name')
        xls_file = request.FILES.get('file')
        tenant_id = request.headers.get('X-Tenant-Id')
        print("rcvd model_name: " ,model_name)
        if not (xls_file.name.endswith('.xls') or xls_file.name.endswith('.xlsx')):
            return JsonResponse({"error": "File is not in XLS/XLSX format"}, status=400)
        
        if not model_name:
            file_name = os.path.splitext(xls_file.name)[0]
            table_name = file_name.lower().replace(' ', '_')  # Ensure table name is lowercase and replace spaces with underscores
        else:
            table_name = model_name
        
        # Read XLS file
        # Extract headers and data
        headers = df.columns.tolist()
        print("headers:" ,headers)
        data = df.values.tolist()
        print("data: " ,data[0])
        
        column_definitions = ', '.join(f'"{header}" VARCHAR(255)' for header in headers)
        
        create_table_query = f"""
            CREATE TABLE IF NOT EXISTS "{table_name}" (
                id SERIAL PRIMARY KEY,
                {column_definitions}
            );
        """
        # Connect to the PostgreSQL database
        conn = get_db_connection()
        cur = conn.cursor()
        print("table created/found")
        try:
            # Create the table
            cur.execute(create_table_query)
            conn.commit()

            # Insert data into the table
            for row in data:
                # Assuming `tenant_id` is part of the `row` or provided separately
                insert_query = f"""
                    INSERT INTO "{table_name}" ({', '.join(f'"{header}"' for header in headers)}, "tenant_id") 
                    VALUES ({', '.join('%s' for _ in range(len(headers)))}, %s);
                """
                print("row: ", row)
                cur.execute(insert_query, row + [tenant_id])
                print("row created")
                conn.commit()

            return JsonResponse({"message": "XLS file uploaded and data inserted successfully", "table_name": table_name}, status=200)
        
        except Exception as e:
            return JsonResponse({"error": f"Error: {e}"}, status=500)
        
        finally:
            cur.close()
            conn.close()

    return JsonResponse({"error": "Invalid request method"}, status=405)