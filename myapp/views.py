from django.shortcuts import render
from simplejson import dumps
from django.contrib.auth.decorators import login_required
#from django.contrib.auth.mixins import
from django.views.generic import ListView
# Create your views here.
from django.urls import reverse_lazy
from django.db.models import Avg, Count, Max
from django.views import generic
from . forms import MyUserCreationForm, QuestionForm
from . models import Question, Answer,User
from django.http import HttpResponse,HttpResponseRedirect, JsonResponse
from .checker.report import Report
import json
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from datetime import datetime
from django.db.models import Avg
import random
import string
#from . misc import score_calculator

datetimeformat = "%Y %d %m %H:%M"

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
def questionmanager(request):
    user = request.user
    if user.is_staff:
        context = dict()
        if request.method == "POST":
            form = QuestionForm(request.POST)
            code = ''.join(random.choices(string.ascii_lowercase + string.ascii_uppercase + string.digits, k=8))
            c = Question.objects.filter(code=code)
            while len(list(c))>0:
                code = ''.join(random.choices(string.ascii_lowercase + string.ascii_uppercase + string.digits, k=8))
                c = Question.objects.filter(code=code)
            if form.is_valid():
                question = form.save(commit = False)
                question.user = request.user
                question.code = code
                question.save()
                print(question)
        else:
            form = QuestionForm()
        context['form'] = form
        context['object_list'] = Question.objects.filter(user_id=request.user.id)
        return render(request, template_name = 'questionmanager.html', context=context)
    else:
        return render(request, template_name = '', context=context)

@login_required(login_url="login")
def practice(request):
    context = dict()
    context['object_list'] = Question.objects.filter(user_id = 1)
    return render(request, template_name = 'practice.html', context=context)

@login_required(login_url="login")
def main_view(request):
    return render(request,template_name="homepage.html", context={"user": request.user})


@login_required(login_url="login")
def attempt(request,qid):
    s = datetime.strftime(datetime.now(), datetimeformat)
    return render(request, template_name="answer.html",context = {'question': Question.objects.get(pk=qid), 'starttime':s})

@login_required(login_url="login")
def getanswerforuser(request):
    if request.method == "POST":
        uid = request.user.id
        qid = request.POST['qid']
        #print(uid, qid)
        #get the json from DB in variable d
        qs =  list(Answer.objects.filter(question_id = qid, user_id = uid))[0]
        #d = json.loads(json.dumps(qs.Json))
        #print(d)
        #print(qs.Json)
        return HttpResponse(qs.Json)

@login_required(login_url="login")
def get_results(request):
    if request.use.is_staff and request.method == "POST":
        uid = request.POST['uid']
        qid = request.POST['qid']
        #print(uid, qid)
        #get the json from DB in variable d
        userid = list(User.objects.filter(username=uid))[0].id
        qs =  list(Answer.objects.filter(question_id = qid, user_id = userid))[0]
        #d = json.loads(json.dumps(qs.Json))
        #print(d)
        #print(qs.Json)
        return HttpResponse(qs.Json)
    else:
        return JsonResponse([])

@login_required(login_url="login")
def fetch_results(request):
    if request.method == "POST":
        d = Report(request.POST['essay']).reprJSON()
        essay = request.POST['essay']
        qid = request.POST['qid']
        starttime = datetime.strptime(request.POST['starttime'], datetimeformat)
        endtime = datetime.now()
        qs = Answer.objects.filter(question_id = qid, user_id = request.user.id)
        if qs:
            qs.delete()
        score = d['score']
        grammarCount = d['grammarErrorCount']
        spellingCount = d['spellingErrorCount']
        json_object = json.dumps(d)
        foo_instance = Answer(user_id=request.user.id,question_id = qid,Json = json_object,score = score,grammarErrors = grammarCount ,spellingErrors = spellingCount, starttime=starttime, endtime=endtime)
        foo_instance.save()
       
        return HttpResponse(json_object)

@login_required(login_url="login")
def delete_question(request, qid):
    if request.user.is_staff:
        question = Question.objects.get(pk=qid)
        # add case where user can del question which is created by him only
        if question.user_id != request.user.id:
            return HttpResponse("Not allowed")
        else:
            question.delete()
            return redirect('home')
    else:
        return render(request, template_name = '', context=context)

@login_required(login_url="login")
def leaderboard(request, qid):
    if request.user.is_staff:
        qs = Answer.objects.filter(question_id=qid).order_by('-score').only("user", "score", "starttime", "endtime")
        q = Question.objects.get(pk=qid).question
        results = []
        if qs:
            rank = 1
            for attempt in qs:
                results.append((attempt.user, rank, attempt.score, datetime.strftime(attempt.starttime, "%d-%m-%Y"), datetime.strftime(attempt.starttime, "%H:%M"), datetime.strftime(attempt.endtime, "%H:%M")))
                rank += 1
        return render(request, template_name="leaderboard.html", context={"results": results, "question":q})
    else:
        return render(request, template_name = '', context=context)

@login_required(login_url="login")
def getuserattemptdata(request):
    a =  Answer.objects.filter(user_id=request.user.id).order_by('starttime').only("score")
    data = []
    for x in a:
        data.append(x.score)
    return JsonResponse({"data":data})

@login_required(login_url="login")
def getuserperformance(request):
    score = Answer.objects.filter(user_id = request.user.id).aggregate(Avg('score'))
    avg_score = score['score__avg']
    no_of_attempts = Answer.objects.filter(user_id = request.user.id).count()
    qs = Answer.objects.filter(user_id=request.user.id).order_by('-score').only("question_id", "score", "starttime", "endtime", "grammarErrors", "spellingErrors")
    results = []
    avgscore = 0
    totalattempts = 0
    attempttimes = []
    lastattempted = "nil"
    
    if qs:
        for attempt in qs:
            avgscore += attempt.score
            totalattempts += 1
            attempttimes.append(attempt.starttime)
            q = Question.objects.get(pk=attempt.question_id).question
            results.append((q, attempt.score, datetime.strftime(attempt.starttime, "%d-%m-%Y"), datetime.strftime(attempt.starttime, "%H:%M"), datetime.strftime(attempt.endtime, "%H:%M"), attempt.grammarErrors, attempt.spellingErrors, attempt.question_id))
    if(totalattempts>0):
        avgscore /= totalattempts
        lastattempted = sorted(attempttimes)[-1]
    
    return render(request, template_name="userperformance.html", context={"results": results, "user":request.user.id, "avgscore":avgscore, "totalattempts":totalattempts, "lastattempted":lastattempted})

@login_required(login_url="login")
def getuserperfdata(request, uid):
    if request.user.is_staff:
        a = Answer.objects.filter(question__user_id=request.user.id, user_id=uid).order_by('starttime').only('score')
        data = []
        for x in a:
            data.append(x.score)
        print(data)
        return JsonResponse({"data":data})
    else:
        return JsonResponse({"data":[]})

    

@login_required(login_url="login")
def getallusersummary(request):
    if request.user.is_staff:
        qs = Answer.objects.filter(question__user_id=request.user.id).select_related().values("user_id").annotate(Avg('score'), Count('question'), Max('starttime'))
        results = []
        for result in qs:
            u = User.objects.get(pk=result['user_id'])
            results.append({"userid":result['user_id'], "username":u.username, "avgscore":result['score__avg'], "count":result['question__count'], "lastattempted":result['starttime__max']})
        
        return render(request, template_name="getallusersummary.html", context={"results":results})
    else:
        return render(request, template_name = '', context=context)

@login_required(login_url="login")
def canattempt(request, code):
    q = Answers.objects.filter(user_id=request.user.id, question_code=code).annotate(Count('question_code'))
    #idea is to see how many attempts he has made and what is allowed for this question
    #if allowed return json {"status":"OK", "url":"/attempt/qid"}
    #else return json {"status":"You have reached the maximum limit to answer this question. Try other!"}
    print(q)