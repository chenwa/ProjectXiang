# ProjectXiang

Setup:

    1. Install Python3

    2. Install Fast API and Uvicorn
        ```pip install fastapi uvicorn```

    3. Create a Virtual Enviroment
        ```python3 -m venv evn```
        ```source env/bin/activate```

    4. Run the FastAPI Application
        ```uvicorn main:app --reload```

    5. Access the API Documentation at 
        -Swagger UI: http://127.0.0.1:8000/docs
        -ReDoc: http://127.0.0.1:8000/redoc
