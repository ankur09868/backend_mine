from django.shortcuts import render
from rest_framework import generics
from .models import Product, Experience
from .serializers import ProductSerializer, ExperienceSerializer
from rest_framework.permissions import IsAdminUser
from helpers.tables import get_db_connection
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import logging

class ProductListAPIView(generics.ListCreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    # permission_classes = (IsAdminUser,)

class ProductDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    # permission_classes = (IsAdminUser,)

class ExperienceListAPIView(generics.ListCreateAPIView):
    queryset = Experience.objects.all()
    serializer_class = ExperienceSerializer

class ExperienceDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Experience.objects.all()
    serializer_class = ExperienceSerializer

logger = logging.getLogger(__name__)

@csrf_exempt
def get_products(request):
    if request.method == "GET":
        connection = get_db_connection()
        cursor = connection.cursor()
        query = """
            SELECT 
                product_product.*, 
                custom_fields_customfield.custom_field,
                custom_fields_customfield.value
            FROM 
                product_product
            JOIN 
                custom_fields_customfield
            ON 
                product_product.id = custom_fields_customfield.object_id
            ORDER BY 
                product_product.id;
        """

        try:
            # Execute the query
            cursor.execute(query)

            column_names = [desc[0] for desc in cursor.description]

            # Fetch all results
            results = cursor.fetchall()

            # Organize results
            products = {}
            for row in results:
                product_id = row[0]  # Assuming the ID is the first column
                if product_id not in products:
                    # Initialize product entry
                    products[product_id] = {
                        "id": row[0],
                        "product_owner": row[1],
                        "product_name": row[2],
                        "product_code": row[3],
                        "product_active": row[4],
                        "manufacturer": row[5],
                        "product_category": row[6],
                        "sales_start_date": row[7],
                        "sales_end_date": row[8],
                        "support_start_date": row[9],
                        "support_end_date": row[10],
                        "unit_price": row[11],
                        "commission_rate": row[12],
                        "tax": row[13],
                        "is_taxable": row[14],
                        "usage_unit": row[15],
                        "qty_ordered": row[16],
                        "reorder_level": row[17],
                        "quantity_in_stock": row[18],
                        "handler": row[19],
                        "quantity_in_demand": row[20],
                        "description": row[21],
                        "tenant_id": row[22],
                        "vendor_name": row[23]
                    }
                # Add custom field as a top-level entry
                custom_field = row[-2]
                value = row[-1]
                products[product_id][custom_field] = value

            # Convert to list for JSON response
            data = list(products.values())
            return JsonResponse(data, safe=False, status=200)

        except Exception as e:
            logger.error(f"An error occurred: {e}")
            return JsonResponse({"error": str(e)}, status=500)

        finally:
            # Close the cursor and connection
            cursor.close()
            connection.close()