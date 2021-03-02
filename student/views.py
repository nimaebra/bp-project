from django.shortcuts import render
from django.views import View

# Models
from teacher.models import Practice

# Datetime
import datetime
import jdatetime


class Practices(View):
    def get(self, request, *args, **kwargs):
        practices = Practice.objects.all()
        for i in range(len(practices)):
            practices[i].deadline = convert_to_jalali(practices[i].deadline)
            practices[i].created_at = convert_to_jalali(
                practices[i].created_at)
        return render(request, 'student/practice/index.html', {'practices': practices})


class Answers(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'index.html')


'''
Utils Functions
'''


def convert_to_jalali(datetime):
    return jdatetime.datetime.fromgregorian(
        datetime=datetime, locale='fa_IR').strftime("%a، %d %b %Y، %H:%M:%S")
