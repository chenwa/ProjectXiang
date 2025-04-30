# ProjectXiang
ProjectXiang is the start of an API tool using FastAPI and Uvicorn


Setup:

1. Install Python3

2. Install Fast API and Uvicorn, and other dependancies:    
```pip install -r requirements.txt```

3. Create database and add tables:
Run migration scripts to create tables (./migration/)

4. Create and launch a Virtual Enviroment:    
```
python3 -m venv evn
```
```
source env/bin/activate
```

5. Run the FastAPI Application:    
``` 
uvicorn main:app --reload
```

6. Access the API Documentation at:    
-Swagger UI: http://127.0.0.1:8000/docs    
-ReDoc: http://127.0.0.1:8000/redoc
