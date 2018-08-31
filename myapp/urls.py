from django.contrib import admin
from django.urls import path, include
from django.views.generic.base import TemplateView
from . import views


urlpatterns = [
    path('', include('django.contrib.auth.urls')),
    path('signup/', views.SignUp.as_view(), name='signup'),
    path('home/', views.question_view, name='home'),
    path('home/<int:qid>', views.answer_view, name='answer'),
    path('',views.HomePage_view,name='homepage'),
    path('fetch/',views.fetch_results,name='fetch_results'),
    path('getresult/',views.get_results,name='get_results'),
    path('getanswerforuser/',views.getanswerforuser,name='getanswerforuser'),
    path('getuserperformance/',views.getuserperformance,name='getuserperformance'),
    path('home/del/<int:qid>',views.delete_question, name = 'delete'),
    path('leaderboard/<int:qid>',views.leaderboard, name = 'leaderboard'),
]