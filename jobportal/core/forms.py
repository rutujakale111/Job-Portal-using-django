from django import forms
from .models import Job, Application
from .models import Profile

class JobForm(forms.ModelForm):
    class Meta:
        model = Job
        fields = ['title','description','location']

class ApplicationForm(forms.ModelForm):
    class Meta:
        model = Application
        fields = ['resume','cover_letter']


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['full_name', 'bio', 'phone', 'resume', 'profile_picture', 'skills', 'linkedin', 'github']
