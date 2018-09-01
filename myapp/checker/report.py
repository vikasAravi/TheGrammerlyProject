import requests
from .error import Error
from nltk.corpus import stopwords
import re
languagecheckurl = 'http://localhost:8082/v2/check'
class Report:
    def __init__(self, essay, wordlimit):
        global languagecheckurl
        self.essay = essay
        payload = {"text":essay,"language":"en-US", "enabledOnly":"false"}
        response = requests.post(languagecheckurl,data = payload)
        self.errors = [Error(m) for m in response.json()['matches']]
        self.words = re.sub(r"[.,?!;():\"\']", " ", essay).split()
        self.wordCount = len(self.words)
        stop_words = set(stopwords.words('english'))
        tot = 0
        
        self.avg_sentences = len(essay.split('.'))

        self.spellingErrorCount = len(list(filter(lambda x:x.errorType()=='spelling', self.errors)))
        self.grammarErrorCount = len(self.errors)-self.spellingErrorCount
        #add properties for average worldlenght, sentence length, readability index etc.
        self.score = 10-((self.spellingErrorCount * 0.25) + (self.grammarErrorCount * 0.25))
        if self.score < 0:
            self.score = 0
    def reprJSON(self):
        return dict(answer=self.essay, score = self.score,errors = [e.reprJSON() for e in self.errors],
        wordCount = self.wordCount, spellingErrorCount = self.spellingErrorCount, 
        grammarErrorCount = self.grammarErrorCount)

    
    