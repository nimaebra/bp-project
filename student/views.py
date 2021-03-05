from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.views import View
from django.urls import reverse
from django.http import HttpResponseRedirect

# Decorators
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required, permission_required

# Models
from django.contrib.auth.models import User
from teacher.models import Practice, Teacher, Video
from .models import Answer, Student

# Datetime
import datetime
import jdatetime

# Excpetoins
from django.core.exceptions import ObjectDoesNotExist

# Mixins
from django.contrib.auth.mixins import UserPassesTestMixin

# Consts
STUDENT_GROUP_NAME = 'Student'


class Login(View):
    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect(reverse('student-dashboard'))
        else:
            return render(request, 'student/login.html')

    def post(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect(reverse('student-dashboard'))
        else:
            data = request.POST
            try:
                username = User.objects.get(email=data['email']).username
            except ObjectDoesNotExist:
                return render(request, 'student/login.html', {'error': 'اطلاعات وارد شده صحیح نمی باشد!'})
            user = authenticate(username=username, password=data['password'])
            if user:
                login(request, user)
                if 'next' not in request.GET:
                    return redirect(reverse('student-dashboard'))
                else:
                    return HttpResponseRedirect(request.GET['next'])
            else:
                return render(request, 'teacher/login.html', {'error': 'اطلاعات ورود صحیح نمی باشد!'})


@method_decorator(login_required(login_url='student-login'), name='dispatch')
class Logout(UserPassesTestMixin, View):
    raise_exception = True

    def test_func(self):
        return self.request.user.groups.filter(name=STUDENT_GROUP_NAME)

    def get(self, request, *args, **kwargs):
        logout(request)
        return redirect(reverse('student-login'))


@method_decorator(login_required(login_url='student-login'), name='dispatch')
class Dashboard(UserPassesTestMixin, View):
    raise_exception = True

    def test_func(self):
        return self.request.user.groups.filter(name=STUDENT_GROUP_NAME)

    def get(self, request, *args, **kwargs):
        data = {
            'practices_count': Practice.objects.all().count(),
            'videos_count': Video.objects.all().count()
        }
        return render(request, 'student/dashboard.html', {'data': data})


@method_decorator(login_required(login_url='student-login'), name='dispatch')
class Practices(UserPassesTestMixin, View):
    raise_exception = True

    def test_func(self):
        return self.request.user.groups.filter(name=STUDENT_GROUP_NAME)

    def get(self, request, *args, **kwargs):
        practices = Practice.objects.all()
        student = Student.objects.get(user_id=request.user.id)
        for i in range(len(practices)):
            practices[i].deadline = convert_to_jalali(practices[i].deadline)
            practices[i].created_at = convert_to_jalali(
                practices[i].created_at)
            practices[i].teacher_name = Teacher.objects.get(
                id=practices[i].teacher_id)
            try:
                practices[i].score = Answer.objects.get(
                    practice_id=practices[i].id, student_id=student.id).score
                practices[i].is_send_answer = True
            except ObjectDoesNotExist:
                practices[i].is_send_answer = False

        return render(request, 'student/practice/index.html', {'practices': practices})


@method_decorator(login_required(login_url='student-login'), name='dispatch')
class PracticeAnswer(UserPassesTestMixin, View):
    raise_exception = True

    def test_func(self):
        return self.request.user.groups.filter(name=STUDENT_GROUP_NAME)

    def get(self, request, *args, **kwargs):
        practice_id = kwargs['pk']
        practice = Practice.objects.get(id=practice_id)
        student = Student.objects.get(user_id=request.user.id)
        try:
            practice.answer = Answer.objects.get(
                practice_id=practice.id, student_id=student.id).file
            practice.is_send_answer = True
        except ObjectDoesNotExist:
            practice.is_send_answer = False
        practice.deadline = convert_to_jalali(practice.deadline)
        return render(request, 'student/practice/answer.html', {'practice': practice})

    def post(self, request, *args, **kwargs):
        practice_id = kwargs['pk']
        student_id = Student.objects.get(user_id=request.user.id).id
        answerFile = request.FILES['answerFile']
        newAnswer = Answer(
            file=answerFile, practice_id=practice_id, student_id=student_id)
        newAnswer.save()
        return redirect(reverse('practices-list'))


@method_decorator(login_required(login_url='student-login'), name='dispatch')
class VideosList(UserPassesTestMixin, View):
    raise_exception = True

    def test_func(self):
        return self.request.user.groups.filter(name=STUDENT_GROUP_NAME)

    def get(self, request, *args, **kwargs):
        videos = Video.objects.all()
        for i in range(len(videos)):
            videos[i].created_at = convert_to_jalali(videos[i].created_at)
            videos[i].teacher_name = Teacher.objects.get(
                id=videos[i].teacher_id)
        return render(request, 'student/video/index.html', {'videos': videos})


@method_decorator(login_required(login_url='student-login'), name='dispatch')
class VideosDetail(UserPassesTestMixin, View):
    raise_exception = True

    def test_func(self):
        return self.request.user.groups.filter(name=STUDENT_GROUP_NAME)

    def get(self, request, *args, **kwargs):
        video_id = kwargs['pk']
        video = Video.objects.get(id=video_id)
        video.teacher_name = Teacher.objects.get(
            id=video.teacher_id)
        return render(request, 'student/video/detail.html', {'video': video})


'''
Utils Functions
'''


def convert_to_jalali(datetime):
    return jdatetime.datetime.fromgregorian(
        datetime=datetime, locale='fa_IR').strftime("%a، %d %b %Y، %H:%M")
