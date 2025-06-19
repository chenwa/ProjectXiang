# ProjectXiang
ProjectXiang is now a backend-only FastAPI project. The React frontend has been migrated to separate repositories (e.g., text-genie, NeutralFit).

---

## Local MySQL Database Setup

1. **Install MySQL**
   - macOS: `brew install mysql`
   - Ubuntu: `sudo apt-get install mysql-server`
   - Windows: [Download MySQL](https://dev.mysql.com/downloads/installer/)

2. **Start MySQL server**
   - macOS: `brew services start mysql`
   - Ubuntu: `sudo service mysql start`
   - Windows: Use the MySQL Workbench or Services panel

3. **Create the database**
   ```sql
   CREATE DATABASE project_xiang;
   ```
   You can do this in the MySQL shell:
   ```sh
   mysql -u root -p
   # then in the prompt:
   CREATE DATABASE project_xiang;
   exit;
   ```

4. **(Optional) Set a password for the root user**
   If you want to use a password other than the default, update your `.env` accordingly.

## .env File Setup

Create a `.env` file in the project root with the following content:

```
DATABASE_URL=mysql+pymysql://root:<your_mysql_password>@localhost/project_xiang
```
Replace `<your_mysql_password>` with your actual MySQL root password.

- **Never commit your `.env` file to version control.**
- The application will automatically load this file and use the `DATABASE_URL` for database connections.

---

## Setup (Docker)

1. **Install Docker**  
   Download and install Docker from [https://www.docker.com/products/docker-desktop](https://www.docker.com/products/docker-desktop).

2. **Clone the Repository**  
   ```bash
   git clone https://github.com/chenwa/ProjectXiang.git
   cd ProjectXiang
   ```

3. **Build and Start the Containers**  
   ```bash
   docker-compose up --build
   ```
   This will build the FastAPI Docker image and start both the FastAPI and MySQL containers.

4. **Database Initialization**  
   The database tables will be created automatically on startup using SQLAlchemy's `Base.metadata.create_all()`.

5. **Access the API Documentation**  
   - Swagger UI: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)  
   - ReDoc: [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc)

---

## (Optional) Local Development Without Docker

1. Install Python3
   ```
   brew install python
   ```
2. Install FastAPI, Uvicorn, and other dependencies:  
   ```bash
   pip install -r requirements.txt
   ```

3. Create and launch a Virtual Environment:  
   ```bash
   python3 -m venv env
   source env/bin/activate
   ```

4. Run the FastAPI Application:  
   ```bash
   uvicorn main:app --reload
   ```

5. Access the API Documentation at:  
   - Swagger UI: http://127.0.0.1:8000/docs  
   - ReDoc: http://127.0.0.1:8000/redoc

---

## Deploying Updates to AWS ECS Fargate

After making changes to your FastAPI backend code, follow these steps to deploy the latest version to AWS:

### 1. Build a New Docker Image Locally

```fish
docker build -t projectxiang:latest .
```

### 2. Tag the Image for ECR

```fish
docker tag projectxiang:latest public.ecr.aws/z3g8u5u2/iwarren/projectxiang:latest
```

### 3. Log in to ECR

```fish
aws ecr-public get-login-password --region us-east-1 | docker login --username AWS --password-stdin public.ecr.aws/z3g8u5u2
```

### 4. Push the New Image to ECR

```fish
docker push public.ecr.aws/z3g8u5u2/iwarren/projectxiang:latest
```

### 5. Update the ECS Service

- Go to AWS Console → ECS → Clusters → [Your Cluster] → Services → [Your Service].
- Click **Update**.
- In the “Task Definition” section, select the latest revision (if you created a new one).
- Click **Next** until the end, then **Update Service**.
- This will force ECS to stop the old task and start a new one with the new image.

### 6. Wait for the New Task to Start

- ECS will stop the old task and start a new one with your updated code.
- Wait until the new task is in the **RUNNING** state.

### 7. Test Your App

- Visit your public IP (e.g., `http://YOUR_PUBLIC_IP:8000/` or `/docs`) to confirm your changes are live.

---

## Notes

- The MySQL database data is persisted in a Docker volume (`db_data`).
- To stop the containers, press `Ctrl+C` in the terminal running Docker Compose, then run:
  ```bash
  docker-compose down
  ```
- To remove all data (reset the database), add the `-v` flag:
  ```bash
  docker-compose down -v
  ```

---

**Summary:**
1. Build Docker image
2. Tag and push to ECR
3. Update ECS service (or task)
4. Wait for new task to run
5. Test

See above for detailed commands and AWS Console navigation.
