import importlib

def run_function(function_name):
    try:
        automation_module = importlib.import_module("automation_functions")

        if hasattr(automation_module, function_name) and callable(getattr(automation_module, function_name)):
            func = getattr(automation_module, function_name)
            return {"status": "success", "output": func()}
        else:
            return {"status": "error", "message": "Function not found."}

    except Exception as e:
        return {"status": "error", "message": str(e)}
