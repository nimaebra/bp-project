from django.shortcuts import render, redirect
from django.views import View

# Import Models
from .models import Practice, Video
from student.models import Answer

# Import Forms
from .forms import CreatePracticeForm

# Datetime
import datetime


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


class PracticeCreate(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'create-practice.html', {'form': CreatePracticeForm()})

    def post(self, request, *args, **kwargs):
        data = request.POST
        newPractice = Practice(
            title=data['title'], comment=data['comment'], deadline=datetime.datetime.now())
        newPractice.save()
        return redirect('/teachers/practices')


class Answers(View):
    def get(self, request, *args, **kwargs):
        answers = Answer.objects.all()
        return render(request, 'answers.html', {'answers': answers})


class VideosList(View):
    def get(self, request, *args, **kwargs):
        videos = Video.objects.all()
        return render(request, 'video/index.html', {'videos': videos})


class VideosDetail(View):
    def get(self, request, *args, **kwargs):
        video_id = kwargs['pk']
        video = Video.objects.get(id=video_id)
        print(video)
        return render(request, 'video/detail.html', {'video': video})
