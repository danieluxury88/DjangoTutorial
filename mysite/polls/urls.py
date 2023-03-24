from django.urls import path

from . import views

app_name = 'polls'

urlpatterns = [
    path('', views.index, name='index'),
    #ie: http://127.0.0.1:8000/polls/5/
    #path('<int:question_id>/', views.detail, name ='detail'),
    #ie: http://127.0.0.1:8000/polls/specifics/5/
    path('<int:question_id>/', views.detail, name='detail'),
    #ie: http://127.0.0.1:8000/polls/5/vote
    path('<int:question_id>/vote', views.vote, name ='vote'),
    #ie: http://127.0.0.1:8000/polls/5/results
    path('<int:question_id>/results/', views.results, name='results'),
]