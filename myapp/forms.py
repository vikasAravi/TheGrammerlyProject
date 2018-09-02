from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.contrib.auth.models import User
from . models import Answer,Question,Profile

 

class UserForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]

    def clean_email(self):
        data = self.cleaned_data['email']
        if User.objects.filter(email=data).exists():
            raise forms.ValidationError("This email is already used")
        return data

    def save(self, commit=True):
        user = super(UserForm, self).save(commit=False)
        user.email = self.clean_email()
        if commit:
            user.save()
        return user

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('name', 'college', 'college_id', 'branch_of_study')

class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ["question", "attempts_allowed", "word_limit", "time_limit"]