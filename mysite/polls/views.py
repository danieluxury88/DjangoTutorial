from django.http import HttpResponse


def index(request):
    return HttpResponse("Hello. You are at polls index")


def detail(request, question_id):
    return HttpResponse("You are looking at question %s." % question_id)


def vote(request, question_id):
    return HttpResponse("You are vorting for question %s." % question_id)


def results(request, question_id):
    response = "You're looking at the results of question %s."
    return HttpResponse(response % question_id)
