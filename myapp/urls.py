from django.contrib import admin
from django.urls import path, include, re_path
from django.views.generic.base import TemplateView
from . import views


urlpatterns = [
    path('', include('django.contrib.auth.urls')),
    path('signup/', views.signup, name='signup'),
    path('profile/', views.update_profile, name='profile'),
    path('activate/<str:uidb64>/<str:token>', views.activate, name='activate'),
    path('attempt/<str:code>', views.attempt, name='attempt'),
    path('questionmanager',views.questionmanager,name='questionmanager'),
    path('questionmanager/del/<int:qid>',views.delete_question, name = 'delete'),
    path('',views.main_view,name='homepage'),
    path('practice/',views.practice,name='practice'),
    path('fetch/',views.fetch_results,name='fetch_results'),
    path('getresult/',views.get_results,name='get_results'),
    path('getanswerforuser/',views.getanswerforuser,name='getanswerforuser'),
    path('getuserperformance/',views.getuserperformance,name='getuserperformance'),
    path('leaderboard/<int:qid>',views.leaderboard, name = 'leaderboard'),
    path('getuserattemptdata/', views.getuserattemptdata, name='getuserattemptdata'),
    path('analytics/', views.getallusersummary, name='analytics'),
    path('getuserperfdata/<int:uid>',views.getuserperfdata, name = 'getuserperfdata'),
    path('canattempt/<str:code>',views.canattempt, name = 'canattempt'),
    path('updatequestion/<int:pk>',views.EditQuestion.as_view(), name = 'updatequestion'),
    
]