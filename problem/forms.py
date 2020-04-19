from django import forms
from problem.models import Problem


class Submission(forms.Form):
    file = forms.FileField()
    fields = ['file']
