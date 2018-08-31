from django.contrib import admin
from django.urls import path, include
from django.views.generic.base import TemplateView
from . import views
from . views import question_view,delete_question,leaderboard,extended,review


urlpatterns = [
    path('', include('django.contrib.auth.urls')),
    path('signup/', views.SignUp.as_view(), name='signup'),
    path('home/', question_view, name='home'),
    path('home/<int:qid>', views.answer_view, name='answer'),
    path('',views.HomePage_view,name='homepage'),
    path('fetch/',views.fetch_results,name='fetch_results'),
    path('getresult/',views.get_results,name='get_results'),
    path('home/del/<int:qid>',delete_question, name = 'delete'),
    path('leaderboard/<int:qid>',leaderboard, name = 'leaderboard'),
    path('test1/',extended,name='extended'),
]