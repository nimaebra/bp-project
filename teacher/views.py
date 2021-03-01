from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.views import View
from django.urls import reverse

# Decorators
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required


# Import Models
from .models import Practice, Video
from student.models import Answer

# Datetime
import datetime


class Login(View):
    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect(reverse('dashboard'))
        else:
            return render(request, 'login.html')

    def post(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect(reverse('dashboard'))
        else:
            data = request.POST
            user = authenticate(email=data['email'], password=data['password'])
            if user:
                login(request, user)
                return redirect(reverse('dashboard'))
            else:
                return render(request, 'login.html', {'error': 'اطلاعات ورود صحیح نمی باشد!'})


@method_decorator(login_required(login_url='login'), name='dispatch')
class Dashboard(View):
    def get(self, request, *args, **kwargs):
        # practices = Practice.objects.all()
        return render(request, 'dashboard.html')


class Practices(View):
    def get(self, request, *args, **kwargs):
        practices = Practice.objects.all()
        return render(request, 'practices.html', {'practices': practices})


class PracticesAnswers(View):
    def get(self, request, *args, **kwargs):
        practice_id = kwargs['pk']
        answers = Answer.objects.filter(id=practice_id)
        return render(request, 'answers.html', {'answers': answers})


class PracticeCreate(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'create-practice.html')

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


class VideoCreate(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'video/create.html')

    def post(self, request, *args, **kwargs):
        data = request.POST
        newPractice = Practice(
            title=data['title'], comment=data['comment'], deadline=datetime.datetime.now())
        newPractice.save()
        return redirect('/teachers/practices')
