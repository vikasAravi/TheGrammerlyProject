from django.db import models
from django.contrib.auth.models import User
# Create your models here.


class Question(models.Model):
    question = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    code = models.CharField(max_length = 8,unique = True)
    # should we add timelimit and wordcount to this?

    def __str__(self):
        return "{}".format(self.question)


class Answer(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    score = models.FloatField()
    Json = models.TextField()
    spellingErrors = models.IntegerField()
    grammarErrors = models.IntegerField()
    starttime = models.DateTimeField()
    endtime = models.DateTimeField()
