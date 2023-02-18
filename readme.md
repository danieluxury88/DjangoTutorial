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

### Play with the API

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
```

### Django Admin

- Create an admin user
**python manage.py createsuperuser**

- Start server **python manage.py runserver** and go to http://127.0.0.1:8080/admin/

- Log in with credentials, check editable content: groups and users

- Make the poll app modifiable in the admin

- We need to tell the admin that Question objects have an admin interface. To do this, open the polls/admin.py file, and edit it to look like this:

```
from django.contrib import admin
from .models import Question
admin.site.register(Question)
```
- Visit again admin index page. Question has been registered.
- Enter Question link and note what Django has made:
 . the form was automatically generate from Question model
 . the model fields have a HTML widget.
 . DateTimeField have JavaScript shortcuts.
 . Additional buttons were added.


 ## Part 3 - Creating new views

- In Django, web pages and other content are delivered by views. Each view is represented by a Python function (or method, in case the case of class-based views). Django will choose a view by examining the URL that's requested (to ve preceise, the part of the URL after the domain name)

 - Add more views to **polls/views.py**. These are different because they take an argument:

 ```
 def detail(request, question_id):
    return HttpResponse("You're looking at question %s." % question_id)

def results(request, question_id):
    response = "You're looking at the results of question %s."
    return HttpResponse(response % question_id)

def vote(request, question_id):
    return HttpResponse("You're voting on question %s." % question_id)

```

- Connect the new views into polls.urls module by adding the following path() calls in **polls/urls.py**:

```
from django.urls import path
from . import views

urlspatterns = [
    #ex: /polls/
    path('', views.index, name = 'index'),
    #ex: /polls/5/
    path('<int:question_id>/', view.detail, name ='detail'),
    #ex: /polls/5/results/
    path('<int:question_id>/results/', view.results, name = 'results'),
    #ex: /polls/5/vote/
    path('<int:question_id>/vote/', view.vote, namte = 'vote'),

]
```
- Run server, and access on browser to /polls/34/

### Making views do something
- Read Question db and add info to index view. Modify def index from **views.py**

```
from django.http import HttpResponse

from . models import Question

def index(request):
    latest_question_list = Question.objects.order_by('-pub_date')[:5]
    output = ', '.join([q.question_text for q in latest_question_list])
    return HttpResponse(output)
```

- There is a problem here: page's design is hard-coded. Let's use Django template system to separate design from Python.

- First create a directory called **templates** in polls directory, and inside create another directory called **polls**. Within that create a file called **index.html**

```
{% if latest_question_list %}
    <ul>
    {% for question in latest_question_list %}
        <li><a href ="/polls/{{ question.id }}/">{{ question.question_text }} </a>
        </li>
    {% endfor %}
    </ul>
{% else %}
    <p> No polls are available. </p>
{% endif %}

```

- Update index view in polls/views.py to use template:
```
from django.http import HttpResponse
from django.template import loader

from .models import Question

def index(request):
    latest_question_list = Question.objects.order_by('-pub_date')[:5]
    template = loader.get_template('polls/index.html')
    context = {
        'latest_question_list':latest_question_list,
    }
    return HttpReponse(template.render(context, request))
```
- That code load the template called polls/index.html and passes it a context. The context is a dictionary mapping template variable names to Python objects.

- Use render instead of returning HttpResponse. Change **index function in views.py**
```
from django.shortcuts import render
from .model import Question

def index(request):
    latest_question_list = Question.objects.order_by('-pub_date')[:5]
    context = {'latest_question_list': latest_question_list}
    return render(request, 'polls/index.html', context)
```

- Raise 404 error if question does not exist
```
from django.http import Http404
from django.shortcuts import render

from .models import Question

def detail(request, question_id):
    try:
        question = Question.objects.get(pk=question_id)
    except Question.DoesNotExist:
        raise Http404("Question does not exist")
    return render (request, 'polls/detail.html', {'question': question})
```

- Use shortcut get_object_or_404()
```
from django.shortcuts import get_object_or_404, render

from .models import Question

def detail (request, question_id):
    question = get_object_or_404(Question, pk = question_id)
    return render(request, 'polls/detail.html', {'question': question})
```  