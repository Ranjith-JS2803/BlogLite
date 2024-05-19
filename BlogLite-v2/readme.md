# BLOG LITE APPLICATION

### For running flask application 
- Move to the folder path using command prompt.
- Run the python file app.py using command ```python app.py```.
- The flask app is served on default port ```5000``` in the localhost.
- Open any browser to view the application running on ```localhost:5000```.

### For running API
- Move to the folder path using command prompt.
- Run the python file api.py using command ```python api.py```.
- The flask app is served on port ```5050``` in the localhost.
- Use the yaml file attached with the zip file to view the api created, which performs CRUD operations on blogs or posts.

### For running Celery
- Move to the folder path which contains the celery using command prompt.
- Run the celery content that is present in the api.py using command ```celery -A api.celery worker -l info``` this is used to generate csv file.
- Run the celery content that is present in the api.py using command ```celery -A api.celery beat -l info``` this is used to run the scheduled tasks / jobs.
- Redis-server needs to be started in order to process all of the celery material.