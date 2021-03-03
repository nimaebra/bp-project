from django.shortcuts import render, redirect
from django.views import View
from django.urls import reverse

# Decorators
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required

# Models
from teacher.models import Practice, Teacher, Video
from .models import Answer

# Datetime
import datetime
import jdatetime

# Excpetoins
from django.core.exceptions import ObjectDoesNotExist


@method_decorator(login_required(login_url='student-login'), name='dispatch')
class Dashboard(View):
    def get(self, request, *args, **kwargs):
        data = {
            'practices_count': Practice.objects.all().count(),
            'videos_count': Video.objects.all().count()
        }
        return render(request, 'student/dashboard.html', {'data': data})


@method_decorator(login_required(login_url='student-login'), name='dispatch')
class Practices(View):
    def get(self, request, *args, **kwargs):
        practices = Practice.objects.all()
        for i in range(len(practices)):
            practices[i].deadline = convert_to_jalali(practices[i].deadline)
            practices[i].created_at = convert_to_jalali(
                practices[i].created_at)
            practices[i].teacher_name = Teacher.objects.get(
                id=practices[i].teacher_id)
            try:
                practices[i].score = Answer.objects.get(
                    practice_id=practices[i].id).score
                if practices[i].score == None:
                    practices[i].score = '-'
                practices[i].is_send_answer = True
            except ObjectDoesNotExist:
                practices[i].score = '-'
                practices[i].is_send_answer = False

        return render(request, 'student/practice/index.html', {'practices': practices})


@method_decorator(login_required(login_url='student-login'), name='dispatch')
class PracticeAnswer(View):
    def get(self, request, *args, **kwargs):
        practice_id = kwargs['pk']
        practice = Practice.objects.get(id=practice_id)
        try:
            practice.answer = Answer.objects.get(
                practice_id=practice.id).file
            practice.is_send_answer = True
        except ObjectDoesNotExist:
            practice.is_send_answer = False
        practice.deadline = convert_to_jalali(practice.deadline)
        return render(request, 'student/practice/answer.html', {'practice': practice})

    def post(self, request, *args, **kwargs):
        practice_id = kwargs['pk']
        answerFile = request.FILES['answerFile']
        newAnswer = Answer(file=answerFile, practice_id=practice_id)
        newAnswer.save()
        return redirect(reverse('practices-list'))


@method_decorator(login_required(login_url='student-login'), name='dispatch')
class VideosList(View):
    def get(self, request, *args, **kwargs):
        videos = Video.objects.all()
        for i in range(len(videos)):
            videos[i].created_at = convert_to_jalali(videos[i].created_at)
            videos[i].teacher_name = Teacher.objects.get(
                id=videos[i].teacher_id)
        return render(request, 'student/video/index.html', {'videos': videos})


@method_decorator(login_required(login_url='student-login'), name='dispatch')
class VideosDetail(View):
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
        datetime=datetime, locale='fa_IR').strftime("%a، %d %b %Y، %H:%M:%S")
