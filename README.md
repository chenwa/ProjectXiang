# ProjectXiang
ProjectXiang is the start of an API tool using FastAPI and Uvicorn


Setup:

1. Install Python3

2. Install Fast API and Uvicorn, and other dependancies:    
```pip install -r requirements.txt```

3. Create database and add tables:
```
CREATE TABLE users (
    id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(100) NOT NULL UNIQUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    encrypted_password VARCHAR(255)
);

CREATE TABLE addresses (
    id INT PRIMARY KEY AUTO_INCREMENT, -- Auto-increment primary key
    user_id INT NOT NULL, -- Foreign key to the users table
    street VARCHAR(255) NOT NULL,
    city VARCHAR(100) NOT NULL,
    state VARCHAR(100),
    zip_code VARCHAR(20),
    country VARCHAR(100) NOT NULL,
    CONSTRAINT fk_user
        FOREIGN KEY (user_id) REFERENCES users(id) -- Ensures referential integrity
);

```

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
