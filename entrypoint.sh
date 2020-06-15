export DJANGO_DEBUG=False

# Apply django migrations
python3.7 manage.py makemigrations projects
python3.7 manage.py migrate
python3.7 manage.py collectstatic

# Run server
uwsgi --ini geefusion_project_server/wsgi-docker.ini
