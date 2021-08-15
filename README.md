install using venv 
create venv environment: python3 -m venv venv
start venv: source ./venv/bin/activate
install requirements: pip install -r requirements.txt
create local environment: create a sql file with name test.db in root folder
                            create .env file
                            with HASH_SECRET_KEY, ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES
                            (ALGORITHM = "HS256" ACCESS_TOKEN_EXPIRE_MINUTES = 30)
start app: uvicorn app:app --reload
app runs on port 8000
