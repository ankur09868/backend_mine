import csv, pandas as pd, os
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from storage.tables import get_db_connection

@csrf_exempt
def upload_csv(request):
    if request.method == 'POST':
        csv_file = request.FILES.get('file')
        if not csv_file or not csv_file.name.endswith('.csv'):
            return JsonResponse({"error": "File is not in CSV format"}, status=400)
        model_name = request.POST.get('model_name', None)
        
        # Extract file name without extension to use as table name
        file_name = os.path.splitext(csv_file.name)[0]
        table_name = file_name.lower().replace(' ', '_')  # Ensure table name is lowercase and replace spaces with underscores
        
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
                    INSERT INTO "{table_name}" ({', '.join(f'"{header}"' for header in headers)}) 
                    VALUES ({', '.join('%s' for _ in range(len(headers)))})
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
def upload_xls(request):
    if request.method == 'POST':
        xls_file = request.FILES.get('file')
        if not (xls_file.name.endswith('.xls') or xls_file.name.endswith('.xlsx')):
            return JsonResponse({"error": "File is not in XLS/XLSX format"}, status=400)
        
        # Extract file name without extension to use as table name
        file_name = os.path.splitext(xls_file.name)[0]
        table_name = file_name.lower().replace(' ', '_')  # Ensure table name is lowercase and replace spaces with underscores
        
        # Read XLS file
        df = pd.read_excel(xls_file)
        
        # Extract headers and data
        headers = df.columns.tolist()
        data = df.values.tolist()

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
            for row in data:
                # Prepare the INSERT query dynamically based on headers
                insert_query = f"""
                    INSERT INTO "{table_name}" ({', '.join(f'"{header}"' for header in headers)}) 
                    VALUES ({', '.join('%s' for _ in range(len(headers)))})
                """
                cur.execute(insert_query, row)
                print("row created")
            conn.commit()

            return JsonResponse({"message": "XLS file uploaded and data inserted successfully", "table_name": table_name}, status=200)
        
        except Exception as e:
            return JsonResponse({"error": f"Error: {e}"}, status=500)
        
        finally:
            cur.close()
            conn.close()

    return JsonResponse({"error": "Invalid request method"}, status=405)