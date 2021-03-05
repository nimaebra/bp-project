from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.views import View
from django.urls import reverse
from django.http import HttpResponseRedirect, HttpResponseForbidden

# Decorators
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required, permission_required, user_passes_test


# Models
from django.contrib.auth.models import User
from .models import Practice, Video
from student.models import Answer, Student

# Datetime
import datetime
import jdatetime

# Excpetoins
from django.core.exceptions import ObjectDoesNotExist, PermissionDenied

# Mixins
from django.contrib.auth.mixins import UserPassesTestMixin

# def group_check(user):
# if user.groups.filter(name__in=['teacher']):
#     return PermissionDenied


class Login(View):
    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect(reverse('teacher-dashboard'))
        else:
            return render(request, 'teacher/login.html')

    def post(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect(reverse('teacher-dashboard'))
        else:
            data = request.POST
            try:
                username = User.objects.get(email=data['email']).username
            except ObjectDoesNotExist:
                return render(request, 'teacher/login.html', {'error': 'اطلاعات وارد شده صحیح نمی باشد!'})
            user = authenticate(username=username, password=data['password'])
            if user:
                login(request, user)
                if 'next' not in request.GET:
                    return redirect(reverse('teacher-dashboard'))
                else:
                    return HttpResponseRedirect(request.GET['next'])
            else:
                return render(request, 'teacher/login.html', {'error': 'اطلاعات ورود صحیح نمی باشد!'})


@method_decorator(login_required(login_url='teacher-login'), name='dispatch')
class Logout(View):
    def get(self, request, *args, **kwargs):
        logout(request)
        return redirect(reverse('teacher-login'))


# @method_decorator(permission_required('teacher.add_practice', raise_exception=True), name='dispatch')
@method_decorator(login_required(login_url='teacher-login'), name='dispatch')
# @method_decorator(is_student, name='dispatch')
# @method_decorator(group_required('teacher'))
class Dashboard(UserPassesTestMixin, View):
    raise_exception = True

    def test_func(self):
        print(self.request.user.groups)
        return self.request.user.groups.filter(name__in=['Teacher'])

    def get(self, request, *args, **kwargs):
        # practices = Practice.objects.all()
        return render(request, 'teacher/dashboard.html')


@ method_decorator(login_required(login_url='teacher-login'), name='dispatch')
# @method_decorator(permission_required('teacher', raise_exception=True), name='dispatch')
class Practices(View):
    def get(self, request, *args, **kwargs):
        practices = Practice.objects.all()
        for i in range(len(practices)):
            practices[i].deadline = convert_to_jalali(practices[i].deadline)
            practices[i].created_at = convert_to_jalali(
                practices[i].created_at)
        return render(request, 'teacher/practice/index.html', {'practices': practices})


@ method_decorator(login_required(login_url='teacher-login'), name='dispatch')
# @method_decorator(permission_required('teacher', raise_exception=True), name='dispatch')
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


@ method_decorator(login_required(login_url='teacher-login'), name='dispatch')
# @method_decorator(permission_required('teacher', raise_exception=True), name='dispatch')
class PracticesAnswerDetail(View):
    def get_query(self, practice_id, answer_id):
        practice = Practice.objects.get(id=practice_id)
        answer = Answer.objects.get(id=answer_id)
        student = Student.objects.get(id=answer.student_id)
        practice.deadline = convert_to_jalali(practice.deadline)
        answer.created_at = convert_to_jalali(answer.created_at)
        answer.student = Student.objects.get(id=answer.student_id)
        return (answer, practice, student)

    def get(self, request, *args, **kwargs):
        (answer, practice, student) = self.get_query(
            practice_id=kwargs['practice_id'], answer_id=kwargs['answer_id'])
        template_data = {
            'answer': answer,
            'practice': practice,
            'student': student
        }
        if 'score_error' in kwargs:
            template_data['score_error'] = kwargs['score_error']
        return render(request, 'teacher/practice/answer-detail.html', template_data)

    def post(self, request, *args, **kwargs):
        score = request.POST['score']
        if not self.validate_score(score):
            kwargs['score_error'] = 'لطفا یک نمره معتبر وارد کنید!'
            return self.get(request, *args, **kwargs)
        practice_id = kwargs['practice_id']
        answer_id = kwargs['answer_id']

        answer = Answer.objects.get(id=answer_id)
        answer.score = score
        answer.save()

        return redirect(reverse('practices-answers', kwargs={'pk': practice_id}))

    def validate_score(self, score):
        try:
            val = float(score)
            return True
        except ValueError:
            return False


@method_decorator(login_required(login_url='teacher-login'), name='dispatch')
# @method_decorator(permission_required('teacher', raise_exception=True), name='dispatch')
class PracticeCreate(View):
    def get(self, request, *args, **kwargs):
        if 'date_error' in kwargs:
            return render(request, 'teacher/practice/create.html', {'date_error': kwargs['date_error']})
        return render(request, 'teacher/practice/create.html')

    def post(self, request, *args, **kwargs):
        data = request.POST
        try:
            date = list(map(int, data['date'].split("/")))
            time = list(map(int, data['time'].split(":")))
            g_datetime = jdatetime.datetime(
                date[0], date[1], date[2], time[0], time[1]).togregorian()
        except:
            kwargs['date_error'] = 'لطفا یک تاریخ و ساعت معتبر وارد کنید!'
            return self.get(request, *args, **kwargs)
        return HttpResponse(datetime.datetime.now(), jdatetime.datetime(
            date[0], date[1], date[2], time[0], time[1]))
        if datetime.datetime.now() > datetime.datetime(date[0], date[1], date[2], time[0], time[1]):
            kwargs['date_error'] = 'تاریخ انتخابی نمی تواند قبل از الان باشد!'
            return self.get(request, *args, **kwargs)
        newPractice = Practice(
            title=data['title'], comment=data['comment'], deadline=g_datetime)
        newPractice.save()
        return redirect(reverse('teacher-practices-list'))


@method_decorator(login_required(login_url='teacher-login'), name='dispatch')
# @method_decorator(permission_required('teacher', raise_exception=True), name='dispatch')
class VideosList(View):
    def get(self, request, *args, **kwargs):
        videos = Video.objects.all()
        for i in range(len(videos)):
            videos[i].created_at = convert_to_jalali(videos[i].created_at)
        return render(request, 'teacher/video/index.html', {'videos': videos})


@method_decorator(login_required(login_url='teacher-login'), name='dispatch')
# @method_decorator(permission_required('teacher', raise_exception=True), name='dispatch')
class VideosDetail(View):
    def get(self, request, *args, **kwargs):
        video_id = kwargs['pk']
        video = Video.objects.get(id=video_id)
        return render(request, 'teacher/video/detail.html', {'video': video})


@method_decorator(login_required(login_url='teacher-login'), name='dispatch')
# @method_decorator(permission_required('teacher', raise_exception=True), name='dispatch')
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
        datetime=datetime, locale='fa_IR').strftime("%a، %d %b %Y، %H:%M")
