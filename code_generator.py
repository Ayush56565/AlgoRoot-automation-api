def generate_invocation_code(function_name):
    
    template = f'''from automation_functions import {function_name}

def main():
    try:
        {function_name}()
        print("{function_name.replace("_", " ").capitalize()} executed successfully.")
    except Exception as e:
        print(f"Error executing function: {{e}}")

if __name__ == "__main__":
    main()
    '''
    return template
