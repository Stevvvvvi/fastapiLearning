install using venv 
create venv environment: python3 -m venv venv
start venv: source ./venv/bin/activate
install requirements: pip install -r requirements.txt
start app: uvicorn app:app --reload
app runs on port 8000
