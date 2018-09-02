from django.shortcuts import render
from simplejson import dumps
from django.contrib.auth.decorators import login_required
#from django.contrib.auth.mixins import
from django.views.generic import ListView
# Create your views here.
from django.urls import reverse_lazy
from django.db.models import Avg, Count, Max
from django.db import transaction
from django.views import generic
from . forms import UserForm, QuestionForm, ProfileForm
from . models import Question, Answer,User
from django.contrib.sites.shortcuts import get_current_site
from .tokens import account_activation_token
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes, force_text
from django.http import HttpResponse,HttpResponseRedirect, JsonResponse
from .checker.report import Report
import json
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.shortcuts import redirect
from datetime import datetime
from django.db.models import Avg
from django.core.mail import EmailMessage
from django.contrib.auth import login, authenticate
import random
import string
#from . misc import score_calculator

datetimeformat = "%Y %d %m %H:%M"


@login_required(login_url="login")
#@transaction.atomic
def update_profile(request):
    # if request.method == 'POST':
    #     user_form = UserForm(request.POST, instance=request.user)
    #     profile_form = ProfileForm(request.POST, instance=request.user.profile)
    #     if user_form.is_valid() and profile_form.is_valid():
    #         user_form.save()
    #         profile_form.save()
    #         messages.success(request, _('Your profile was successfully updated!'))
    #         return redirect('settings:profile')
    #     else:
    #         messages.error(request, _('Please correct the error below.'))
    # else:
    #     user_form = UserForm(instance=request.user)
    #     profile_form = ProfileForm(instance=request.user.profile)
    # return render(request, 'registration/profile.html', {
    #     'user_form': user_form,
    #     'profile_form': profile_form
    # })
    return render(request, 'registration/profile.html', {
        'user': request.user,
        'profile': request.user.profile
    })

def signup(request):
    if request.method == 'POST':
        user_form = UserForm(request.POST)
        profile_form = ProfileForm(request.POST)
        user_form = UserForm(request.POST)
        profile_form = ProfileForm(request.POST)
        if user_form.is_valid() and profile_form.is_valid():
            profile = profile_form.save(commit = False)
            user = user_form.save(commit = False)
            user.is_active = False
            user.save()
            user.profile.name = profile.name
            user.profile.college = profile.college
            user.profile.college_id = profile.college_id
            user.profile.branch_of_study = profile.branch_of_study
            user.save()
            
            
            current_site = get_current_site(request)
            mail_subject = 'Activate your grammar check account.'
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            tok = account_activation_token.make_token(user)          
            message = render_to_string('acc_active_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid':uid.decode('utf-8'),
                'token':tok,
            })
            to_email = user_form.cleaned_data.get('email')
            email = EmailMessage(
                        mail_subject, message, to=[to_email]
            )
            email.send()
            return render(request, 'registration/message.html', {'message':'Please confirm your email address to complete the registration'})
    else:
        user_form = UserForm()
        profile_form = ProfileForm()
    return render(request, 'registration/signup.html', {
        'user_form': user_form,
        'profile_form': profile_form
    })

# class SignUp(generic.CreateView):
#     form_class = UserForm
#     success_url = reverse_lazy('login')
#     template_name = 'registration/signup.html'

#     def post(self,request, *args, **kwargs):
#         user_form = UserForm(request.POST)
#         profile_form = ProfileForm(request.POST)
#         if user_form.is_valid() and profile_form.is_valid():
#             user = user_form.save(commit = False)
#             user.is_active = False
#             user.save()
#             profile_form.save()
#             current_site = get_current_site(request)
#             mail_subject = 'Activate your grammar check account.'
#             uid = urlsafe_base64_encode(force_bytes(user.pk))
#             tok = account_activation_token.make_token(user)          
#             message = render_to_string('acc_active_email.html', {
#                 'user': user,
#                 'domain': current_site.domain,
#                 'uid':uid.decode('utf-8'),
#                 'token':tok,
#             })
#             to_email = user_form.cleaned_data.get('email')
#             email = EmailMessage(
#                         mail_subject, message, to=[to_email]
#             )
#             email.send()
#             #TODO:Create a nice page for confirmation and use that
#             return HttpResponse('Please confirm your email address to complete the registration')
#         else:
#             return render(request,'registration/signup.html',{'user_form': user_form, 'profile_form': profile_form})

def activate(request, uidb64, token, backend='django.contrib.auth.backends.ModelBackend'):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)

    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user, backend='django.contrib.auth.backends.ModelBackend')
        return redirect('homepage')
    else:
        return render(request, 'registration/message.html', {"message":'Activation link is invalid!'})

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
        else:
            form = QuestionForm()
        context['form'] = form
        context['object_list'] = Question.objects.filter(user_id=request.user.id)
        return render(request, template_name = 'questionmanager.html', context=context)
    else:
        return redirect('homepage')

@login_required(login_url="login")
def practice(request):
    context = dict()
    results = []
    questions = Question.objects.filter(user_id = 1)
    for q in questions:
        a = list(Answer.objects.filter(user_id=request.user.id,question_id=q.id))
        s = 0
        n = 0
        avg = 0
        for x in a:
            s += x.score
            n += 1
        if n>0:
            avg = s/n
        if len(a) < q.attempts_allowed:
            results.append((q, True, avg, n, q.attempts_allowed))
        else:
            
            results.append((q, False, avg, n, q.attempts_allowed))
    return render(request, template_name = 'practice.html', context={"questions":results})

@login_required(login_url="login")
def main_view(request):
    return render(request,template_name="homepage.html", context={"user": request.user})


@login_required(login_url="login")
def attempt(request,code):
    s = datetime.strftime(datetime.now(), datetimeformat)
    
    q = Question.objects.get(code=code)
    a = list(Answer.objects.filter(user_id=request.user.id,question_id=q.id))
    if len(a) < q.attempts_allowed:
        return render(request, template_name="attempt.html",context = {'question': q, 'starttime':s})
    else:
        return redirect('homepage')


@login_required(login_url="login")
def canattempt(request, code):
    q = Question.objects.get(code=code)
    a = list(Answer.objects.filter(user_id=request.user.id,question_id=q.id))
    if len(a) < q.attempts_allowed:
        return JsonResponse({"status":"OK", "url":request.build_absolute_uri("/attempt/"+code)})
    else:
        return JsonResponse({"status":"You have already reached maximum attempt limit. Please try with diferent code or practice!"})

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
    if request.user.is_staff and request.method == "POST":
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
        essay = request.POST['essay']
        qid = request.POST['qid']
        q = Question.objects.get(pk=qid)
        starttime = datetime.strptime(request.POST['starttime'], datetimeformat)
        endtime = datetime.now()
        d = Report(essay, q.word_limit).reprJSON()
        score = d['score']
        grammarCount = d['grammarErrorCount']
        spellingCount = d['spellingErrorCount']
        json_object = json.dumps(d)
        foo_instance = Answer(user_id=request.user.id,question_id = qid,Json = json_object,score = score,grammarErrors = grammarCount ,spellingErrors = spellingCount, starttime=starttime, endtime=endtime)
        foo_instance.save()
       
        return HttpResponse(json_object)

@login_required(login_url="login")
def updatequestion(request, qid):
    if request.user.is_staff:
        form = QuestionForm(request.POST)
        q = Question.objects.get(pk = qid)
        return render(request,"editquestion.html",{'form':form})
        
@login_required(login_url="login")
def getquestiondata(request, qid):
    if request.user.is_staff:
        obj = Question.objects.get(pk = qid)
        return JsonResponse({"wordlimit":obj.word_limit, "timelimit":obj.time_limit, "attempts":obj.attempts})

class EditQuestion(PermissionRequiredMixin,LoginRequiredMixin,generic.UpdateView):
    login_url = '/login/'
    model = Question
    form_class = QuestionForm
    template_name = 'editquestion.html'
    success_url = reverse_lazy("questionmanager")

    def has_permission(self):
        question  = Question.objects.get(id=self.kwargs['pk'])
        return question.user == self.request.user

    def has_no_permission(self):
        if self.raise_exception:
            raise PermissionDenied(self.get_permission_denied_message())
        return redirect(self.request.META.get("HTTP_REFERER"))


@login_required(login_url="login")
def delete_question(request, qid):
    if request.user.is_staff:
        question = Question.objects.get(pk=qid)
        # add case where user can del question which is created by him only
        if question.user_id != request.user.id:
            return HttpResponse("Not allowed")
        else:
            question.delete()
            return redirect('questionmanager')
    else:
        return redirect('homepage')

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
        return redirect('homepage')

@login_required(login_url="login")
def getuserattemptdata(request):
    a =  Answer.objects.filter(user_id=request.user.id).order_by('starttime').only("score", "starttime")
    data = []
    labels = []
    for x in a:
        data.append(x.score)
        labels.append(x.starttime)
    return JsonResponse({"data":data, "labels":labels})

@login_required(login_url="login")
def getuserperformance(request):
    #TODO: calculate rank of user overall and also branchwise.
    # should we consider all essays or only with users who attempted same essays
    # should we be comparing progress trends as well. What to maintain in the cube?
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
    
    return render(request, template_name="userperformance.html", context={"results": results, "user":request.user, "avgscore":avgscore, "totalattempts":totalattempts, "lastattempted":lastattempted})

@login_required(login_url="login")
def getuserperfdata(request, uid):
    if request.user.is_staff:
        a = Answer.objects.filter(question__user_id=request.user.id, user_id=uid).order_by('starttime').only('score', 'starttime')
        data = []
        labels = []
        for x in a:
            data.append(x.score)
            labels.append(x.starttime)
        return JsonResponse({"data":data, "labels":labels})
    else:
        return JsonResponse({"data":[], "labels":[]})

    

@login_required(login_url="login")
def getallusersummary(request):
    if request.user.is_staff:
        minscore = 0
        maxscore = 10
        if request.method=="POST":
            minscore = request.POST["minscore"]
            maxscore = request.POST["maxscore"]

        qs = Answer.objects.filter(question__user_id=request.user.id, score__gte = minscore, score__lte = maxscore).select_related().values("user_id").annotate(Avg('score'), Count('question'), Max('starttime'))
        results = []
        for result in qs:
            u = User.objects.get(pk=result['user_id'])
            results.append({"userid":result['user_id'], "username":u.username, "profile":u.profile, "avgscore":result['score__avg'], "count":result['question__count'], "lastattempted":result['starttime__max']})
        attrs = {"minscore":minscore, "maxscore":maxscore}
        return render(request, template_name="getallusersummary.html", context={"results":results, "attrs":attrs})
    else:
        return redirect('homepage')