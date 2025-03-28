import chromadb
import uuid
import time
from sentence_transformers import SentenceTransformer

SESSION_EXPIRY_TIME = 1800  

class SessionMemory:
    def __init__(self):
        self.client = chromadb.PersistentClient(path="./session_db")
        self.session_collection = self.client.get_or_create_collection(name="session_history")
        self.embedding_model = SentenceTransformer("all-MiniLM-L6-v2")

    def generate_session_id(self):
        return str(uuid.uuid4())

    def store_interaction(self, session_id, user_prompt, function_name):
        timestamp = time.time()  
        embedding = self.embedding_model.encode(user_prompt).tolist()

        self.session_collection.add(
            documents=[user_prompt],
            embeddings=[embedding],
            ids=[f"{session_id}_{function_name}"],
            metadatas=[{"timestamp": timestamp}]
        )

    def get_session_history(self, session_id):
        results = self.session_collection.get()

        session_history = []
        current_time = time.time()

        for doc_id, metadata in zip(results["ids"], results["metadatas"]):
            if doc_id.startswith(session_id):
                timestamp = metadata.get("timestamp", 0)
                if current_time - timestamp <= SESSION_EXPIRY_TIME:
                    session_history.append(doc_id.split("_")[1])

        return session_history

session_memory = SessionMemory()
