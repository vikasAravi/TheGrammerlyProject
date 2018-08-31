from django.shortcuts import render
from simplejson import dumps
from django.contrib.auth.decorators import login_required
#from django.contrib.auth.mixins import
from django.views.generic import ListView
# Create your views here.
from django.urls import reverse_lazy
from django.views import generic
from . forms import MyUserCreationForm, QuestionForm
from . models import Question, Answer,User
from django.http import HttpResponse,HttpResponseRedirect
from .checker.report import Report
import json
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
#from . misc import score_calculator


class SignUp(generic.CreateView):
    form_class = MyUserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'signup.html'

    def post(self,request, *args, **kwargs):
        form = MyUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit = False)
            if request.POST['role'] == 'creator':
                user.is_staff = True
            user.save()
            return HttpResponseRedirect('/login/')
        return render(request,'signup.html',{'form': form})


# class QuestionsListView(LoginRequiredMixin,ListView):
#     login_url = "login"
#     template_name = "home.html"
#     model = Question

@login_required(login_url="login")
def question_view(request):
    user = request.user
    if user.is_staff:
        context = dict()
        if request.method == "POST":
            form = QuestionForm(request.POST)
            if form.is_valid():
                question = form.save(commit = False)
                question.user = request.user
                question.save()
        else:
            form = QuestionForm()
        context['form'] = form
        context['object_list'] = Question.objects.filter(user_id=request.user.id)
        return render(request, template_name = 'testcreator home.html', context=context)
    else:
        context = dict()
        context['object_list'] = Question.objects.filter(user_id = 1)
        return render(request, template_name = 'testtaker home.html', context=context)

def HomePage_view(request):
    return render(request,template_name="homepage.html", context={"user": request.user})


@login_required(login_url="login")
def answer_view(request,qid):
    return render(request, template_name="answer.html",context = {'question': Question.objects.get(pk=qid)})

def get_results(request):
    if request.method == "POST":
        uid = request.POST['uid']
        qid = request.POST['qid']
        #print(uid, qid)
        #get the json from DB in variable d
        userid = list(User.objects.filter(username=uid))[0].id
        qs =  list(Answer.objects.filter(question_id = qid, user_id = userid))[0]
        d = json.loads(json.dumps(qs.Json))
        print(d)
        return HttpResponse(json.dumps(d))

def fetch_results(request):
    if request.method == "GET":
         return HttpResponse("hey") 
    if request.method == "POST":
        d = Report(request.POST['essay']).reprJSON()
        essay = request.POST['essay']
        qid = request.POST['qid']
        qs = Answer.objects.filter(question_id = qid, user_id = request.user.id)
        if qs:
            qs.delete()
        score = d['score']
        grammarCount = d['grammarErrorCount']
        spellingCount = d['spellingErrorCount']
        json_object = d
        foo_instance = Answer(user_id=request.user.id,question_id = qid,Json = json_object,score = score,grammarErrors = grammarCount ,spellingErrors = spellingCount)
        foo_instance.save()
       
        return HttpResponse(json.dumps(d))
    #return render(request,template_name="answer.html",context={"obj":json.dumps(d)})

def delete_question(request, qid):
    question = Question.objects.get(pk=qid)
    # add case where user can del question which is created by him only
    if question.user_id != request.user.id:
        return HttpResponse("Not allowed")
    else:
        question.delete()
        return redirect('home')


def leaderboard(request, qid):
    qs = Answer.objects.filter(question_id=qid).order_by('-score')
    results = []
    if qs:
        users = list(qs.values_list('user_id', flat=True))
        scores = list(qs.values_list('score', flat=True))
        gc = list(qs.values_list('grammarErrors',flat=True))
        sc =  list(qs.values_list('spellingErrors',flat=True))
        js = list(qs.values_list('Json',flat=True))
        prev = 11
        rank = 0
        for i in range(len(users)):
            username = User.objects.get(pk=users[i]).username
            score = scores[i]
            if prev > score:
                prev = score
                rank += 1
            results.append((username, rank, score))
    return render(request, template_name="leaderboard.html", context={"results": results})

# def modal(request,qid):
#      qs = Answer.objects.filter(question_id=qid)
#      js = list(qs.values_list('Json',flat=True))

def extended(request):
    return render(request,template_name= 'extended.html')


def review(request,uid,qid):
      qs = Answer.objects.filter(question_id = qid, user_id = request.user.id)
      print(qs)
      return render(request,template_name= 'review.html', context = {'qs': qs})