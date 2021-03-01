from django import forms
# from django.contrib.auth.forms import UserCreationForm
from django.forms import ModelForm

from .models import Practice


class CreatePracticeForm(ModelForm):
    class Meta:
        model = Practice
        fields = '__all__'
