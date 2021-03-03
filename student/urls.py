from django.urls import path

from .views import Practices, Dashboard, VideosList, VideosDetail, PracticeAnswer, Login

urlpatterns = [
    path('login', Login.as_view(), name='student-login'),
    path('dashboard', Dashboard.as_view(), name='dashboard'),
    path('practices', Practices.as_view(), name='practices-list'),
    path('practices/<int:pk>', PracticeAnswer.as_view(),
         name='practice-answer'),
    path('videos', VideosList.as_view(), name='videos-list'),
    path('videos/<int:pk>', VideosDetail.as_view(), name='videos-detail'),
]
