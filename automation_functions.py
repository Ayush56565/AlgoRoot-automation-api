import os
import webbrowser
import psutil
import subprocess

def open_chrome():
    webbrowser.open("https://www.google.com")

def open_calculator():
    os.system("calc")

def get_cpu_usage():
    return f"CPU Usage: {psutil.cpu_percent()}%"

def get_ram_usage():
    return f"RAM Usage: {psutil.virtual_memory().percent}%"

def list_directory(path="./Desktop"):
    try:
        return subprocess.getoutput(f"ls {path}")
    except Exception as e:
        return f"Error listing directory: {str(e)}"

def get_working_directory():
    try:
        return subprocess.getoutput("pwd")
    except Exception as e:
        return f"Error getting working directory: {str(e)}"