from django.shortcuts import render
from django.views import View

# Import Django Models
from .models import Practice
from student.models import Answer


class Practices(View):
    def get(self, request, *args, **kwargs):
        practices = Practice.objects.all()
        return render(request, 'practices.html', {'practices': practices})


class PracticesAnswers(View):
    def get(self, request, *args, **kwargs):
        practice_id = kwargs['pk']
        print(practice_id)
        answers = Answer.objects.filter(id=practice_id)
        return render(request, 'answers.html', {'answers': answers})


class Answers(View):
    def get(self, request, *args, **kwargs):
        answers = Answer.objects.all()
        return render(request, 'answers.html', {'answers': answers})
