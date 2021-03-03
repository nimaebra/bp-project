from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.views import View
from django.urls import reverse

# Decorators
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required


# Models
from .models import Practice, Video
from student.models import Answer, Student

# Datetime
import datetime
import jdatetime


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
        return render(request, 'teacher/dashboard.html')


class Practices(View):
    def get(self, request, *args, **kwargs):
        practices = Practice.objects.all()
        for i in range(len(practices)):
            practices[i].deadline = convert_to_jalali(practices[i].deadline)
            practices[i].created_at = convert_to_jalali(
                practices[i].created_at)
        return render(request, 'teacher/practice/index.html', {'practices': practices})


class PracticesAnswers(View):
    def get(self, request, *args, **kwargs):
        practice_id = kwargs['pk']
        practice_title = Practice.objects.get(id=practice_id).title
        answers = Answer.objects.filter(practice_id=practice_id)
        for i in range(len(answers)):
            answers[i].created_at = convert_to_jalali(answers[i].created_at)
            answers[i].student = Student.objects.get(
                id=answers[i].student_id)
        # print(practice_id, answers)
        return render(request, 'teacher/practice/answers.html', {'answers': answers, 'practice_title': practice_title})


class PracticesAnswerDetail(View):
    def get(self, request, *args, **kwargs):
        practice_id = kwargs['practice_id']
        answer_id = kwargs['answer_id']
        answers = Answer.objects.filter(practice_id=practice_id)
        for i in range(len(answers)):
            answers[i].created_at = convert_to_jalali(answers[i].created_at)
            answers[i].student_number = Student.objects.get(
                id=answers[i].student_id).student_number
        # print(practice_id, answers)
        return render(request, 'teacher/practice/answer-detail.html', {'answers': answers})


class PracticeCreate(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'teacher/practice/create.html')

    def post(self, request, *args, **kwargs):
        data = request.POST
        date = list(map(int, data['date'].split("/")))
        time = list(map(int, data['time'].split(":")))
        g_datetime = jdatetime.datetime(
            date[0], date[1], date[2], time[0], time[1]).togregorian()
        newPractice = Practice(
            title=data['title'], comment=data['comment'], deadline=g_datetime)
        newPractice.save()
        return redirect(reverse('teacher-practices-list'))


class VideosList(View):
    def get(self, request, *args, **kwargs):
        videos = Video.objects.all()
        for i in range(len(videos)):
            videos[i].created_at = convert_to_jalali(videos[i].created_at)
        return render(request, 'teacher/video/index.html', {'videos': videos})


class VideosDetail(View):
    def get(self, request, *args, **kwargs):
        video_id = kwargs['pk']
        video = Video.objects.get(id=video_id)
        return render(request, 'teacher/video/detail.html', {'video': video})


class VideoCreate(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'teacher/video/create.html')

    def post(self, request, *args, **kwargs):
        data = request.POST
        video = request.FILES['video']
        newVideo = Video(
            title=data['title'], video=video)
        newVideo.save()
        return redirect(reverse('videos-list'))


'''
Utils Functions
'''


def convert_to_jalali(datetime):
    return jdatetime.datetime.fromgregorian(
        datetime=datetime, locale='fa_IR').strftime("%a، %d %b %Y، %H:%M:%S")
