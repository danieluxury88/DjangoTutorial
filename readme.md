## Readme
Following Django Project tutorial
## Prerequisites
* Create a conda environment
    * conda env list
    * conda create --name CS50Web python=3.9
    * conda activate CS50Web
* Install libraries
    * pip3 install Django
    * pip install ipython

## Procedure
1. django-admin startproject mysite
2. python manage.py runserver 8090
3. python manage.py startapp polls
4. edit polls/views.py
```
from django.http import HttpResponse

def index(request):
    return HttpResponse("Hello. You are at polls index")
```
5. create urls.py file
```
from django.urls import path
from .import views

urlspatterns = [
    path('', views.index, name='index')
]
```
6. Include the app urls in the project urlpatters in mysite/urls.py
```
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('polls/', include('polls.ulrs')),
    path('admin/', admin.site.urls)
]
```

## Part 2 - Create a database, create first model and quick introduction to admin site

1. in polls/models.py, create two models: Question and Choice

```
from django.db import models

class Question(models.Model):
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField('data published')


class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)

```

2. Add Polls app in Project settings
3. Run makemigrations command to update changes on the models
```
python manage.py makemigrations polls
```
4. Run sqlmigrate command
```
python manage.py sqlmigrate polls 0001
```

5. Run migrate command to create those models in the database


6. Change the models in models.py
- run python manage.py makemigrations
- run python manage.py migrate