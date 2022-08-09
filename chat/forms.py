from .models import Message
from django.forms import ModelForm, Textarea

class MessageForm(ModelForm):
    class Meta:
        model = Message
        fields = ['message']
        labels = {'message': ""}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['message'].widget = Textarea(
            attrs= {
                'type': "text",
                'rows': 1,
                'class':'send-field',
                'placeholder': 'Message',
                # 'min_length': 1,
            }
        )