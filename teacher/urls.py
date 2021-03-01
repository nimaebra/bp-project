from django.urls import path

from .views import Practices, PracticesAnswers, PracticeCreate, VideosList, VideosDetail

urlpatterns = [
    path('practices', Practices.as_view(), name='practices'),
    path('practices/create', PracticeCreate.as_view(), name='practice-create'),
    path('practices/<int:pk>', PracticesAnswers.as_view(),
         name='practices-answers'),
    path('videos', VideosList.as_view(), name='videos'),
    path('videos/<int:pk>', VideosDetail.as_view(), name='videos-detail'),
]
