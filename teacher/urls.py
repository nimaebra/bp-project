from django.urls import path

from .views import Practices, PracticesAnswers, PracticeCreate, VideosList, VideosDetail, Login, Dashboard, VideoCreate

urlpatterns = [
    path('login', Login.as_view(), name='login'),
    path('dashboard', Dashboard.as_view(), name='dashboard'),
    path('practices', Practices.as_view(), name='practices-list'),
    path('practices/create', PracticeCreate.as_view(), name='practice-create'),
    path('practices/<int:pk>', PracticesAnswers.as_view(),
         name='practices-answers'),
    path('videos', VideosList.as_view(), name='videos-list'),
    path('videos/<int:pk>', VideosDetail.as_view(), name='videos-detail'),
    path('videos/create', VideoCreate.as_view(), name='video-create'),
]
