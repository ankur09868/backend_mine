import psycopg2
from psycopg2.extras import RealDictCursor

def get_db_connection():
    return psycopg2.connect(
            dbname="postgres",
            user="nurenai",
            password="Biz1nurenWar*",
            host="nurenaistore.postgres.database.azure.com",
            port="5432"
        )


def fetch_table(table_name: str):
    try: 
        conn = get_db_connection()
        cur=conn.cursor(cursor_factory=RealDictCursor)

        cur.execute(f"SELECT * FROM {table_name}")
            
            # Fetch all rows from the executed query
        data = cur.fetchall()
            
            # Close the cursor and connection
        cur.close()
        conn.close()


        def format_row(row) -> str:
            ans="{" + "\n"
            ans+=",".join(f' "{key}": "{value}"' for key, value in row.items())
            ans+="\n" + "}"
            return ans

        # Iterate through each row and format
        formatted_rows = [format_row(row) for row in data]

        return formatted_rows
    
    except Exception as e:
        print(f"Error fetching data: {e}")
        return []

def get_tables_schema():
    query = """
        SELECT
            table_schema,
            table_name,
            column_name,
            ordinal_position,
            column_default,
            is_nullable,
            data_type,
            character_maximum_length,
            numeric_precision,
            numeric_scale,
            udt_name
        FROM
            information_schema.columns
        WHERE
            table_schema NOT IN ('information_schema', 'pg_catalog')
        ORDER BY
            table_schema,
            table_name,
            ordinal_position;
        """
    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute(query)
        table_struct = cursor.fetchall()

        table_schema = {}
        for row in table_struct:
            
            table_name =row[1]
            column_name = row[2]
            
            if table_name not in table_schema:
                table_schema[table_name] = []
            table_schema[table_name].append(column_name)

        result = [{table_name: columns} for table_name, columns in table_schema.items()]

        return result
    except Exception as error:
        print(f"Error fetching table schemas: {error}")
    finally:
        if conn:
            cursor.close()
            conn.close()


