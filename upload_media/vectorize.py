from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import os, psycopg2, pymupdf, json
from openai import OpenAI
import numpy as np
# Initialize OpenAI client
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Load and split file into chunks
def split_file(pdf_file):
    document = pymupdf.open(stream=pdf_file, filetype="pdf")
    docs = []
    for page_num in range(len(document)):
        page = document.load_page(page_num)
        text = page.get_text()
        docs.append(text)
    return docs

def get_embeddings(chunks):
    embeddings = []
    for chunk in chunks:
        response = client.embeddings.create(input=chunk, model="text-embedding-3-small")
        embeddings.append(response.data[0].embedding)
    return embeddings

def get_db_connection():
    return psycopg2.connect(
            dbname="postgres",
            user="nurenai",
            password="Biz1nurenWar*",
            host="nurenaistore.postgres.database.azure.com",
            port="5432"
        )

def vectorize(request):
    try:
        if request.method == 'POST':
            pdf_file = request.FILES['file'].read()  # Ensure you're using request.FILES to get the uploaded file
        else:
            return JsonResponse({"status": 405, "message": "Request method is not POST"}, status=405)

        chunks = split_file(pdf_file)
        embeddings = get_embeddings(chunks)

        conn = get_db_connection()
        cur = conn.cursor()
        
        cur.execute('''
        CREATE TABLE IF NOT EXISTS text_embeddings (
            id SERIAL PRIMARY KEY,
            chunk TEXT,
            embedding vector(1536)
        )
        ''')
        conn.commit()

        # Insert embeddings into the table
        for i, chunk in enumerate(chunks):
            embedding_array = np.array(embeddings[i])
            cur.execute(
                "INSERT INTO text_embeddings (chunk, embedding) VALUES (%s, %s::vector)",
                (chunk, embedding_array.tolist())
            )
        conn.commit()

        return JsonResponse({"status": 200, "message": "Text vectorized successfully"})

    except Exception as e:
        print(f"An error occurred: {e}")
        return JsonResponse({"status": 500, "message": f"An error occurred: {e}"}, status=500)

    finally:
        if 'cur' in locals():
            cur.close()
        if 'conn' in locals():
            conn.close()


# Function to get embedding for a query string using OpenAI
def get_query_embedding(query):
    response = client.embeddings.create(
        input=query,
        model="text-embedding-ada-002"
    )
    embedding = response.data[0].embedding
    print(type(embedding))
    return embedding

# Function to store chunk and its embedding into PostgreSQL
def store_chunk_embedding(chunk, embedding):
    try:
        # Database connection details
        with get_db_connection() as conn:
            with conn.cursor() as cur:
                # Insert the chunk and its embedding into the table
                cur.execute(
                    "INSERT INTO text_embeddings (chunk, embedding) VALUES (%s, %s::vector(1536))",
                    (chunk, embedding)
                )
                conn.commit()
    except psycopg2.Error as e:
        print(f"Error: {e}")
    return []

# Function to perform cosine similarity search using pgvector
def perform_cosine_similarity_search(query_embedding):
    try:
        # Database connection details
        with get_db_connection() as conn:
            with conn.cursor() as cur:
                # Convert query embedding to string format for SQL
                query_embedding_str = '[' + ','.join(map(str, query_embedding)) + ']'
                
                # Perform the cosine similarity search
                cur.execute(
                    f"""
                    SELECT
                        te.id,
                        te.chunk AS most_similar_chunk,
                        (te.embedding::vector) <-> %s AS similarity_score
                    FROM
                        text_embeddings te
                    ORDER BY (te.embedding::vector) <-> %s DESC
                    LIMIT 10;

                    """,
                    (query_embedding_str, query_embedding_str)
                )
                results = cur.fetchall()
                return results
    except psycopg2.Error as e:
        print(f"Error: {e}")
    return []

# Main function to process and search similar queries
def process_and_search_similar_queries(query):
    # Get the embedding for the query
    query_embedding = get_query_embedding(query)
    
    # Convert query embedding to numpy array of type float64
    query_embedding_array = np.array(query_embedding, dtype=np.float64)
    
    # Perform cosine similarity search
    similar_queries = perform_cosine_similarity_search(query_embedding_array)
    
    return similar_queries


def make_openai_call(combined_query, query_string):

    # Combine the template with the query
    # prompt = prompt_template.format(combined_query=combined_query, query_string=query_string)

    # print("PROMPT: " ,prompt)

    # Make the OpenAI API request
    # client = openai.OpenAI(api_key = API_KEY)

    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": "you shall answer the queries asked based on the following text provided: {}".format(combined_query)},
            {"role": "assistant", "content": "Sure, I'd be happy to answer any queries you have based on the provided text"},
            {"role": "user", "content": "{}".format(query_string)}
        ]
    )

    # Extract and return the response text
    return response.choices[0].message.content



@csrf_exempt
def query(request):
    req_body = json.loads(request.body)
    query_string = req_body.get("query", "")
    
    if not query_string:
        return JsonResponse({"status": 400, "message": "Query is required."})
    
    similar_queries = process_and_search_similar_queries(query_string)
    combined_query =""

    for item in similar_queries:
        combined_query += item[1] + " "
        # print(f"ID: {item[0]}, Chunk: {item[1]}, Similarity: {item[2]:.4f}")
        
    # print("COMB QUERY: " ,combined_query)
    # prompt = "based on the {}, answer the query: {} suitably in minimum words.".format(combined_query, query_string)

    # Make the OpenAI call
    openai_response = make_openai_call(combined_query, query_string)
    return JsonResponse({"status": 200, "message": openai_response})
    # print(f"OpenAI Response: {openai_response}")

