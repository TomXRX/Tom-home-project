import os
os.system("python manage.py migrate")
# os.system("python manage.py createsuperuser")
n=os.popen("celery -A home.celery beat -l info --scheduler django_celery_beat.schedulers:DatabaseScheduler")
f=os.popen("celery -A home.celery worker -l INFO -P gevent")
# n=os.popen("celery -A home.celery beat -l info")
import socket
print(socket.gethostbyname(socket.gethostname()))
os.system("python manage.py runserver 0.0.0.0:80")
