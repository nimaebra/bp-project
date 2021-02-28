from django.urls import path

from .views import Practices

urlpatterns = [
    path('practices', Practices.as_view(), name='practices')
]
