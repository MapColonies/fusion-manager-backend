export DJANGO_DEBUG=False
export FUSION_PATH="/opt/google/share/tutorials/fusion/"

# Apply django migrations
python3.7 manage.py makemigrations imagery
python3.7 manage.py migrate
python3.7 manage.py collectstatic

# Run server
uwsgi --ini geefusion_project_server/wsgi-docker.ini
