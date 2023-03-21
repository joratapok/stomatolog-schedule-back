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
  # Build and up docker containers
  docker-compose -f docker-compose.prod.yml up -d --build

  # Create superuser
  docker-compose -f docker-compose.prod.yml exec web python manage.py createsuperuser

  # Access to the docker container from the inside
  docker exec -it --user root stomatolog-schedule-back_web_1 /bin/bash

  # Delete all work containers with volumes
  docker-compose -f docker-compose.prod.yml down -v

  # Restart all docker containers
  docker-compose -f docker-compose.prod.yml restart
