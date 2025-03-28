from fastapi import FastAPI
from pydantic import BaseModel
from function_retriever import retrieve_best_function
from session_memory import session_memory
from code_generator import generate_invocation_code

app = FastAPI()

class ExecuteRequest(BaseModel):
    prompt: str
    session_id: str | None = None 

@app.post("/execute")
def execute_function(request: ExecuteRequest):
    
    session_id = request.session_id or session_memory.generate_session_id()
    function_name = retrieve_best_function(request.prompt,session_id)

    if not function_name:
        return {"error": "No matching function found"}

    session_memory.store_interaction(session_id, request.prompt, function_name)
    generated_code = generate_invocation_code(function_name)

    return {
        "function": function_name,
        "code": generated_code
    }
