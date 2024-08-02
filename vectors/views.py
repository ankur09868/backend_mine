import numpy as np
import os
import psycopg2
from django.http import HttpResponse
from psycopg2.extensions import register_adapter, AsIs, adapt
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from openai import OpenAI
from psycopg2 import sql
import time
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
import json
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import  QuerySerializer
from dataclasses import dataclass
from django.core.files.storage import default_storage
from langchain_community.document_loaders import PyPDFLoader
from pypdf.errors import PdfStreamError



# Set your OpenAI API key
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Database connection string
DB_CONNECTION_STRING = 'postgresql://nurenai:Biz1nurenWar*@nurenaistore.postgres.database.azure.com:5432/nurenpostgres'

# Define the dimension of embeddings
N_DIM = 1536

# Adapter function to convert NumPy array to PostgreSQL vector
def adapt_numpy_array(query_embedding):
    return AsIs("'[{}]'::vector".format(",".join(map(str, query_embedding))))

# Register the adapter for NumPy arrays
register_adapter(np.ndarray, adapt_numpy_array)


@dataclass
class TextChunk:
    page_content: str
    metadata: dict

def pdf_to_txt(pdf_path, txt_path):
    try:
        loader = PyPDFLoader(pdf_path)
        documents = loader.load()
        with open(txt_path, 'w', encoding='utf-8') as f:
            for i, page in enumerate(documents):
                f.write(f"\n{page}\n\n")
        print(f"Processed {pdf_path} \nsaved content to {txt_path}")
    except PdfStreamError as e:
        print(f"Failed to process {pdf_path} due to PDF stream error: {e}")
    except Exception as e:
        print(f"Failed to process {pdf_path}: {e}")

def extract_metadata_and_split_text(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        lines = file.readlines()

    chunks = []
    metadata = None
    content = ""

    for line in lines:
        if "metadata=" in line:  # Assuming metadata lines contain 'metadata='
            if content:
                chunks.append(TextChunk(page_content=content.strip(), metadata=metadata))
                content = ""
            metadata_start = line.find("metadata=") + len("metadata=")

            metadata = eval(line[metadata_start:].strip())
        else:
            content += line
    

    if content:
        chunks.append(TextChunk(page_content=content.strip(), metadata=metadata))
    

    textsplitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=0)
    split_chunks = []
    for chunk in chunks:
        split_documents = textsplitter.split_text(chunk.page_content)
        for i, doc in enumerate(split_documents):
            split_chunks.append(TextChunk(page_content=doc, metadata=metadata))
    return split_chunks

def generate_embeddings(text_chunks):
    embeddings = OpenAIEmbeddings()
    return [embeddings.embed_query(chunk.page_content) for chunk in text_chunks]

def insert_embeddings(embeddings, text_chunks,txt_file_path):
    with psycopg2.connect(DB_CONNECTION_STRING) as conn:
        with conn.cursor() as cursor:
            cursor.execute(
                """                
                CREATE TABLE IF NOT EXISTS text_embeddings_anky (
                    id SERIAL PRIMARY KEY,
                    document TEXT,
                    source TEXT,
                    embedding vector(%s)
                )
                """, [N_DIM]
            )
            for chunk, embedding in zip(text_chunks, embeddings):
                # Ensure metadata is not None
                if chunk.metadata is not None:
                    source_with_metadata = f"File-Path: { txt_file_path } / Page-No: { chunk.metadata['page'] }"
                else:
                    source_with_metadata = f"File-Path:{txt_file_path}"

                cursor.execute(
                    "INSERT INTO text_embeddings_anky (document, source, embedding) VALUES (%s, %s, %s)",
                    (chunk.page_content, source_with_metadata, adapt(embedding))
                )
            cursor.execute(
                """
                CREATE INDEX IF NOT EXISTS text_embeddings_anky_embedding_idx
                ON text_embeddings_anky USING ivfflat (embedding vector_cosine_ops) with (lists=500)
                
                """
            )
            conn.commit()

# Function to get embedding for a query string using OpenAI
def get_embedding(text, model="text-embedding-ada-002"):
    text = text.replace("\n", " ")
    return client.embeddings.create(input=[text], model=model).data[0].embedding

def find_similar_embeddings(query_embedding, threshold=0.5): 
    conn = psycopg2.connect(DB_CONNECTION_STRING)
    cursor = conn.cursor()
            
    try:
        query = sql.SQL(f"""
            SELECT id, document, source, (embedding <=> %s::vector) AS distance
            FROM text_embeddings_anky
            WHERE (embedding <=> %s::vector) < %s
            ORDER BY distance 
            LIMIT 15;
        """)
        
        cursor.execute(query, (query_embedding, query_embedding, threshold))
   
        results = cursor.fetchall()
        return results
    finally:
        cursor.close()
        conn.close()

    
def make_openai_call(combined_query, query_text):
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are a helpful assistant. You will analyze the provided similar documents and select the four best matches based on the query. Provide the relevant sources ."},
                {"role": "user", "content": f"Here are the similar documents:\n{combined_query}"},
                {"role": "user", "content": f"Based on the provided documents, here is the query: {query_text}. Please select the four documents that best match this query."}
            ]
        )

        content = response.choices[0].message.content
        return content
        
        
    except Exception as e:
        print(f"Error making OpenAI call: {e}")
        return 'Error in OpenAI call'





@method_decorator(csrf_exempt, name='dispatch')
class ProcessFileView(APIView):
    def post(self, request, format=None):
        try:
            # Handle the uploaded file
            uploaded_file = request.FILES.get('file', None)
            if not uploaded_file:
                return Response({"error": "File upload is required"}, status=status.HTTP_400_BAD_REQUEST)

            # Save the uploaded file temporarily
            file_name = uploaded_file.name
            file_path = default_storage.save(file_name, uploaded_file)

            # Process the file
            print("________________________PDF-2-TXT______________________________________________")
            if file_path.endswith('.pdf'):
                txt_file_path = os.path.splitext(file_path)[0] + '.txt'
            else:
                txt_file_path = file_path + '.txt'
            pdf_to_txt(file_path, txt_file_path)
            print("________________________Reading TXT______________________________________________")
            text_chunks = extract_metadata_and_split_text(txt_file_path)
            print(f"Split into {len(text_chunks)} chunks.")
        

            print("________________________Embedding______________________________________________")
            start_time = time.time()
            embeddings = generate_embeddings(text_chunks)
            end_time = time.time()

            total_time = end_time - start_time
            minutes = int(total_time // 60)
            seconds = total_time % 60

            print("Embeddings generated successfully.")
            print(f"Time taken: {minutes} minutes and {seconds:.2f} seconds")
            print("________________________Storing in database______________________________________________")

            insert_embeddings(embeddings, text_chunks, txt_file_path)
            print("Embeddings inserted into the database.")
            print(f"{txt_file_path} embedded and stored into database")
            
             # Delete the temporary files
            default_storage.delete(file_path)
            default_storage.delete(txt_file_path)

            return Response({"status": "success", "message": f"{txt_file_path} embedded and saved to database"}, status=status.HTTP_200_OK)

        except Exception as e:
            print(f"Error processing text file: {e}")
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        

@method_decorator(csrf_exempt, name='dispatch')
class HandleQueryView(APIView):
    serializer_class = QuerySerializer

    def post(self, request, *args, **kwargs):
        try:
            data = json.loads(request.body)
            query_text = data.get('prompt')
            
            if not query_text:
                return Response({"error": "Query text is required"}, status=status.HTTP_400_BAD_REQUEST)
            
            query_embedding = get_embedding(query_text, model="text-embedding-ada-002")
            query_embedding = np.array(query_embedding)
            
            try:
                similar_docs = find_similar_embeddings(query_embedding)
                
                if similar_docs:
                    # Limit to the top 10 similar documents
                    top_docs = similar_docs[:10]
                    print(top_docs)
            
                    # Create a detailed combined_query including the top 10 similar documents
                    combined_query = ""
                    for idx, doc in enumerate(top_docs):
                        combined_query += f"Document {idx+1}: ID: {doc[0]}, Score: {doc[1]}, Source: {doc[2]}\n"
            
                    # Make the OpenAI call
                        openai_response = make_openai_call(combined_query, query_text)
            
                    response = {
                        "query": query_text,
                        "combined_query": combined_query,
                        "openai_response": openai_response
                    }
                    
                    fresponse = (
                        f"query: {response['query']}\n"
                        f"combined_query: {response['combined_query']}\n"
                        f"openai_response: {response['openai_response']}\n"
                    )
                    return HttpResponse(f"Success: {fresponse}", status=200)
                else:
                    return Response({"error": "No similar documents found"}, status=status.HTTP_404_NOT_FOUND)
            
            except Exception as e:
                return HttpResponse({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        except json.JSONDecodeError:
            return HttpResponse({"error": "Invalid JSON"}, status=status.HTTP_400_BAD_REQUEST)
    
    def get(self, request, *args, **kwargs):
        return HttpResponse({"error": "Invalid request method"}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
