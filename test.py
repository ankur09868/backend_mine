from django.db import connection
from helpers.tables import get_db_connection

connection = get_db_connection()
with connection.cursor() as cursor:
    cursor.execute("SELECT * FROM node_temps_flow")
    rows = cursor.fetchone()

for row in rows:
    print(row)

