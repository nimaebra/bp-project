from django.urls import path

from .views import Practices, PracticesAnswers

urlpatterns = [
    path('practices', Practices.as_view(), name='practices'),
    path('practices/<int:pk>', PracticesAnswers.as_view(), name='practices-answers')
]
