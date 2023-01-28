# Celery Run

Install and run Celery with RabbitMQ for this project:

Install Celery:
1. pip install celery gevent 

Before run Celery:
  run RabbitMQ server
  
Run Celery:
1. In the first terminal - python manage.py runserver
2. In the second terminal - celery -A stomatology worker -P gevent
3. In the third terminal - celery -A stomatology beat -l info


# Docker Run

For the first time:
  1. docker-compose build
  2. docker-compose run --rm web sh -c "python manage.py migrate"   # Where "web" this is name of service from file docker-compose.yml
  3. docker-compose run --rm web sh -c "python manage.py createsuperuser"
  4. docker-compose up
