from dataclasses import fields
from . models import Discussion
from django.forms import ModelForm

class DiscussionCreateForm(ModelForm):

    class Meta:
        model = Discussion
        fields = ('title', 'content')
