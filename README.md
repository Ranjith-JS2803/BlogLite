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

#### For running flask application 
- Move to the folder path using command prompt.
- Run the python file app.py using command ```python app.py```.
- The flask app is served on default port ```5000``` in the localhost.
- Open any browser to view the application running on ```localhost:5000```.

#### For running API
- Move to the folder path using command prompt.
- Run the python file api.py using command ```python api.py```.
- The flask app is served on port ```5050``` in the localhost.
- Use the yaml file attached with the zip file to view the api created, which performs CRUD operations on blogs or posts.

### BlogLite-v2
- **Features:**
  - Integrated regular reminder notifications through Google Chat and emails for users’ usage activities.
  - Executed CSV export functionality for user reports and optimized API performance with caching for enhanced responsiveness.
- **Technologies Used:**
  - Flask
  - VueJS
  - Redis
  - Celery

#### For running flask application 
- Move to the folder path using command prompt.
- Run the python file app.py using command ```python app.py```.
- The flask app is served on default port ```5000``` in the localhost.
- Open any browser to view the application running on ```localhost:5000```.

#### For running API
- Move to the folder path using command prompt.
- Run the python file api.py using command ```python api.py```.
- The flask app is served on port ```5050``` in the localhost.
- Use the yaml file attached with the zip file to view the api created, which performs CRUD operations on blogs or posts.

#### For running Celery
- Move to the folder path which contains the celery using command prompt.
- Run the celery content that is present in the api.py using command ```celery -A api.celery worker -l info``` this is used to generate csv file.
- Run the celery content that is present in the api.py using command ```celery -A api.celery beat -l info``` this is used to run the scheduled tasks / jobs.
- Redis-server needs to be started in order to process all of the celery material.
