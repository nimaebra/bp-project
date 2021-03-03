from django.urls import path

from .views import Practices, PracticesAnswers, PracticeCreate, VideosList, VideosDetail, Login, Dashboard, VideoCreate, PracticesAnswerDetail, Logout

urlpatterns = [
    path('login', Login.as_view(), name='teacher-login'),
    path('logout', Logout.as_view(), name='teacher-logout'),
    path('dashboard', Dashboard.as_view(), name='teacher-dashboard'),
    path('practices', Practices.as_view(), name='teacher-practices-list'),
    path('practices/create', PracticeCreate.as_view(), name='practice-create'),
    path('practices/<int:pk>/answers', PracticesAnswers.as_view(),
         name='practices-answers'),
    path('practices/<int:practice_id>/answers/<int:answer_id>', PracticesAnswerDetail.as_view(),
         name='practices-answer-detail'),
    path('videos', VideosList.as_view(), name='teacher-videos-list'),
    path('videos/<int:pk>', VideosDetail.as_view(), name='videos-detail'),
    path('videos/create', VideoCreate.as_view(), name='video-create'),
]
