from stomatology.celery import app
from rest_framework.authtoken.models import Token
from datetime import datetime


@app.task
def delete_user_token_every_day():
    current_time = datetime.now()
    tokens = Token.objects.all()
    if tokens:
        for token in tokens:
            if (current_time - token.created).days >= 1:
                token.delete()
