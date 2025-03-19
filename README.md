# Authentication Project with Django
This is a simple authentication project built using Django, featuring user registration, login, password recovery, two-factor authentication (2FA). The project also allows users to view the last login date and entry date. Additionally, it is configured to run easily in a Docker environment using Docker Compose.

# Features
#### User Registration: Allows users to create an account with basic information.
#### Login: Users can log in using their email and password.
#### Password Recovery: Allows users to recover their password through an email.
#### Two-Factor Authentication (2FA): Adds an extra layer of security with a second authentication factor.
#### Last Login & Entry Date: Users can see the date they last logged in and their entry date.
# Images
## Screen Register
![image](https://github.com/user-attachments/assets/295678f2-054a-4237-83d1-3fda003a6855)
## Screen Login
![image](https://github.com/user-attachments/assets/91d5fd1a-bfc9-4389-bccd-4052b2ac1f53)
## Screen Account
![image](https://github.com/user-attachments/assets/eabe93f7-0310-44d2-8198-3c8a954ad57a)
# Link to project
https://project-login-eewwtjttu-igornunes-devs-projects.vercel.app/
# Technologies Used
#### Django: Web framework for building the application.
#### HTML & CSS: Used for creating the front-end structure and styling.
#### Docker: Containerization for the development and production environments.
#### Docker Compose: Orchestrates the containers for Django and PostgreSQL.
#### PostgreSQL: Database used to store user information.
#### Django Allauth: For managing authentication, including password recovery.
# Prerequisites
Before running the project, you need to have the following installed on your machine:

#### Docker: For containerizing the application.
#### Docker Compose: To manage the project's containers.

#Installation:

## Docker:

### 1. Install Docker:

First, install Docker on your machine:
- For Linux: [Docker Installation Guide for Linux](https://docs.docker.com/engine/install/ubuntu/)
- For Windows: [Docker Desktop for Windows](https://docs.docker.com/desktop/install/windows-install/)
- For Mac: [Docker Desktop for Mac](https://docs.docker.com/desktop/install/mac-install/)

### 2. Clone the repository:

```bash
git clone https://github.com/igornunes-dev/project-login.git
cd project login
```

### 3. Build and start the containers:

```bash
docker-compose up --build
```

The project will be available at `http://localhost:8000`

To stop the containers:
```bash
docker-compose down
```

### 4. Running migrations:

In another terminal, with the containers running, run:
```bash
docker exec -it web python /app/manage.py makemigrations

docker exec -it web python /app/manage.py migrate
```

### 5. Creating a superuser (optional):

```bash
docker-compose exec web python manager.py createsuperuser
```

Whenever you want to start the project, just use this command, always making sure that the venv is active and in the root of the project. It is not necessary to repeat all the steps every time. Migrations will only be necessary if Django points out (in the terminal, when you start the project) that there are unapplied migrations.
