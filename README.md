# BlogLite
This repository contains two versions of the BlogLite application: BlogLite-v1 and BlogLite-v2. Each version represents a distinct iteration of the BlogLite project, featuring different functionalities and improvements.

## Versions

### BlogLite-v1
- **Features:**
  - Implemented user authentication, profile management, and follow system functionalities.
  - Designed CRUD operations for blogs, enabling creation, editing, and deletion, with features for liking and commenting.
- **Technologies Used:**
  - Flask
  - HTML
  - CSS
  - Bootstrap

#### Running the Flask Application
1. Move to the folder path using the command prompt.
2. Run the Python file `app.py` using the command:

    ```bash
    python app.py
    ```
4. The Flask app is served on the default port `5000` on localhost.
5. Open any browser to view the application running on `http://localhost:5000`.

#### Running the API
1. Move to the folder path using the command prompt.
2. Run the Python file `api.py` using the command:

    ```bash
    python api.py
    ```
4. The Flask app is served on port `5050` on localhost.
5. Use the YAML file attached with the zip file to view the API, which performs CRUD operations on blogs or posts.

### BlogLite-v2
- **Features:**
  - Integrated regular reminder notifications through Google Chat and emails for users’ usage activities.
  - Executed CSV export functionality for user reports and optimized API performance with caching for enhanced responsiveness.
- **Technologies Used:**
  - Flask
  - VueJS
  - Redis
  - Celery

#### Running the Flask Application
1. Move to the folder path using the command prompt.
2. Run the Python file `app.py` using the command:

    ```bash
    python app.py
    ```
4. The Flask app is served on the default port `5000` on localhost.
5. Open any browser to view the application running on `http://localhost:5000`.

#### Running the API
1. Move to the folder path using the command prompt.
2. Run the Python file `api.py` using the command:

    ```bash
    python api.py
    ```
4. The Flask app is served on port `5050` on localhost.
5. Use the YAML file attached with the zip file to view the API, which performs CRUD operations on blogs or posts.

#### Running Celery
1. Move to the folder path that contains the Celery configuration using the command prompt.
2. Run the Celery worker present in `api.py` using the command:

    ```bash
    celery -A api.celery worker -l info
    ```
   This command is used to generate the CSV file.
4. Run the Celery beat present in `api.py` using the command:
   
    ```bash
    celery -A api.celery beat -l info
    ```
   This command is used to run the scheduled tasks/jobs.
5. Ensure the Redis server is started in order to process all of the Celery tasks.
