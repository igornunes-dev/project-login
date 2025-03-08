# Authentication Project with Django
This is a simple authentication project built using Django, featuring user registration, login, password recovery, two-factor authentication (2FA), and Google login. The project also allows users to view the last login date and entry date. Additionally, it is configured to run easily in a Docker environment using Docker Compose.

# Features
#### User Registration: Allows users to create an account with basic information.
#### Login: Users can log in using their email and password.
#### Password Recovery: Allows users to recover their password through an email.
#### Two-Factor Authentication (2FA): Adds an extra layer of security with a second authentication factor.
#### Google Login: Enables users to log in using their Google account.
#### Last Login & Entry Date: Users can see the date they last logged in and their entry date.
# Images
## Screen Register
![image](https://github.com/user-attachments/assets/10124f25-d9f2-426f-9fc5-66444fec32ff)
## Screen Login
![image](https://github.com/user-attachments/assets/755a14c3-a1b3-4be2-9645-fd618ef10a92)
## Screen Account
![image](https://github.com/user-attachments/assets/9f7e5976-3410-4243-ae14-a8581d6a66fb)
# Technologies Used
#### Django: Web framework for building the application.
#### HTML & CSS: Used for creating the front-end structure and styling.
#### Docker: Containerization for the development and production environments.
#### Docker Compose: Orchestrates the containers for Django and PostgreSQL.
#### PostgreSQL: Database used to store user information.
#### Google OAuth2: Integration for allowing login through Google accounts.
#### Django Allauth: For managing authentication, including social login and password recovery.
# Prerequisites
Before running the project, you need to have the following installed on your machine:

#### Docker: For containerizing the application.
#### Docker Compose: To manage the project's containers.

# Instalação:

## Docker:

### 1. Instalação do Docker:

Primeiro, instale o Docker em sua máquina:
- Para Linux: [Guia de instalação Docker para Linux](https://docs.docker.com/engine/install/ubuntu/)
- Para Windows: [Docker Desktop para Windows](https://docs.docker.com/desktop/install/windows-install/)
- Para Mac: [Docker Desktop para Mac](https://docs.docker.com/desktop/install/mac-install/)

### 2. Clone o repositório:

```bash
git clone https://github.com/igornunes-dev/project-login.git
cd project-login
```

### 3. Construa e inicie os containers:

```bash
docker-compose up --build
```

O projeto estará disponível em `http://localhost:8000`

Para parar os containers:
```bash
docker-compose down
```

### 4. Executando migrações:

Em outro terminal, com os containers rodando, execute:
```bash
docker exec -it web python /app/manage.py makemigrations

docker exec -it web python /app/manage.py migrate
```

### 5. Criando superusuário (opcional):

```bash
docker-compose exec web python manage.py createsuperuser
```

Sempre que quiser iniciar o projeto, basta utilizar esse comando, sempre garantindo que está com a venv ativa e na raiz do projeto. Não é necessário repetir todos os passos sempre. As migrações só serão necessárias caso o Django aponte (no terminal, quando você iniciar o projeto) que há migrações não aplicadas.
