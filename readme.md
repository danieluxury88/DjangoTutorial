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
