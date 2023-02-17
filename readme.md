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

# Procedure
## Part 1 - Create Project and App
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

## Part 3 - Play with the API

- Run **python manage.py shell** to invoke shell
- Explore the database API usign shell commands
```
>>> from polls.models import Choice, Question
>>> Question.objects.all()
>>> from django.utils import timezone
>>> q = Question(question_text="What's up?", pub_date = timezone.now())
>>> q.save()
>>> q.id
1
>>> q.question.text
"What's up?"
>>> q.question_text = "What's new?"
>>> q.save()
>>> Question.objects.all()
```

- Replace Question representation implementing __str__() method
```
    class Question(models.Model) :
        def __str__(self):
            return self.question_text


    class Choice(models.Model):
        def __str__(self):
            return self.choice_text
```

- Add a custom model to Question model
```
    import datetime
    from django.utils import timezone

    class Question(models.Model):
        def was_published_recently(self):
            return self.pub_date >= timezone.now() - datetime.timedelta(days=1)
```
- Save changes and start a new Python interactive shell ** python manage.py shell **

```
>>> from polls.models import Choice, Question
>>> Question.objects.all()
>>> Question.objects.filter(id=1)
>>> Question.objects.filter(question_text__startswith='What')
>>> from django.utils import timezone
>>> current_year = timezone.now().year
>>> Question.objects.get(pub_date__year = current_year)
>>> Question.objects.get(id=2)
>>> Question.objects.get(pk=1)
>>> q = Question.objects.get(pk=1)
>>> q.was_published_recently()
>>> #Give a couple of Choices: the create call constructs a new Choice object does the INSERT statement, add the choice to the set of available choices and return the new Choice object.
>>> q.choice_set.all()
>>> q.choice_set.create(choice_text='Not much', votes = 0)
>>> q.choice_set.create(choice_text='The sky', votes = 0)
>>> c = q.choice_set.create(choice_text='Just hacking again', votes=0)
>>> c.question
>>> q.choice_set.all()
>>> q.choice_set.count()
```
- The API automatically follow relationships as far as you need. Use double underscores to separate relationships. This works as many levels deep as you want.

```
>>> Choice.objects.filter(question__pub_date__year = current_year)
>>> c = q.choice_set.filter(choice_text__startswith='Just hack')
>>> c.delete()
