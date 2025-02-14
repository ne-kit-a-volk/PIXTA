FROM python:3.10-slim
RUN apt-get update && \
    apt-get install -y libpq-dev gcc
WORKDIR /JobRoadMap
COPY . /JobRoadMap
RUN pip install -r freeze.txt

CMD python manage.py migrate \
    && python manage.py shell -c "from django.contrib.auth import get_user_model; User = get_user_model(); User.objects.filter(username='root').exists() or User.objects.create_superuser('root', 'root@example.com', 'root')" \
    && python manage.py collectstatic --noinput \
    && gunicorn job_road_map_site.wsgi:application --bind 0.0.0.0:8000 --log-level info