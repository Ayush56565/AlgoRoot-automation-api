import chromadb
from sentence_transformers import SentenceTransformer


embedding_model = SentenceTransformer("all-MiniLM-L6-v2")
session_memory = chromadb.PersistentClient(path="./session_db").get_or_create_collection(name="session_memory")

function_metadata = {
    "open_chrome": "Launch Google Chrome browser",
    "open_calculator": "Open Windows calculator",
    "get_cpu_usage": "Retrieve current CPU usage",
    "get_ram_usage": "Retrieve current RAM usage",
    "list_directory": "List files and directories in a specified path",
    "get_working_directory": "Get the current working directory"
}

SIMILARITY_THRESHOLD = 0.7 

def store_function_metadata():
    """Store function descriptions and their embeddings in ChromaDB."""
    for func, desc in function_metadata.items():
        embedding = embedding_model.encode(desc).tolist()
        session_memory.add(documents=[desc], embeddings=[embedding], ids=[func])

def retrieve_best_function(user_prompt, session_id):
    embedding = embedding_model.encode(user_prompt).tolist()
    results = session_memory.query(query_embeddings=[embedding], n_results=1)

    if results["ids"]:
        function_name = results["ids"][0][0]
        similarity_score = results["distances"][0][0] 
        print(similarity_score)

        if similarity_score <= SIMILARITY_THRESHOLD:
            return function_name 
        else:
            return None 

    return None 


store_function_metadata()
