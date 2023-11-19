This repository contains the source code for the project, which is configured to run using Docker Compose.

## Prerequisites

Ensure that you have Docker Engine and Docker Compose installed on your system.

## Getting Started

1. **Clone the Repository:**
   ```bash
   git clone https://github.com/Dooweed/drf_user_demo.git
   cd drf_user_demo

2. **Environment Variables**

   Rename file `example.docker.env` to `docker.env` and change `SECRET_KEY`, `DB_NAME`, `DB_USER` and `DB_PASSWORD`
   
   If you want to locally run the project (not within docker):
   
   Rename file `example.env` to `.env` and change values of `SECRET_KEY`, `DB_NAME`, `DB_USER` and `DB_PASSWORD` 
   environment variables

3. **Launch the Application**

   Run the following command to start the application:

   ```bash
   docker-compose up

4. **Verify Running Containers**

   Check the running containers:
   ```bash 
   docker-compose ps
   
5. Access the Application

   Open your browser and navigate to:

   ```http://localhost/api/user/``` (List of users)

6. Shutdown the Application

   To stop the running containers, execute:

   ```bash
   docker-compose down

Use `docker-compose down -v` to also remove volumes associated with containers.


## Description

- **Redoc** documentation available at `http://localhost/api/schema/redoc/`
- **Swagger UI** available at `http://localhost/api/schema/swagger-ui/`
- **Schema in YAML file format** available at `http://localhost/api/schema/`
- **DRF API UI** for users available at `http://localhost/api/users/`
- User detail url format: `http://localhost/api/users/<pk>/`

Once you start the project, the system will populate DB with some randomly generated users.

For building API `django-rest-framework` package was used. Since building an asynchronous 
API was one of the requirement, I have decided to also include package `adrf`. The `adrf` package
is not fully completed now, so I had to build some tweaks so that the application works asynchronously,
you can see documentation in the code for every class and method that is out of classic Django/DRF structure.

For logging, a standard django logging functionality is used. You can find logs in 
`<project-dir>/logs` directory

Tests are written using `pytest` library, you can run them using `python -m pytest`. 
Data for tests dynamically generated using `factoryboy`

JWT Authentication implemented using package `djangorestframework-simplejwt`