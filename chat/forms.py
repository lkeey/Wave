from .models import Message, Group
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

class GroupEditForm(ModelForm):
    class Meta:
        model = Group
        fields = ['name', 'bio']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['name'].widget = Textarea(
            attrs= {
                'rows': 1,
                'class':'input-post-title',
                'placeholder': 'Enter The Name Of Group:',
            }
        )

        self.fields['bio'].widget = Textarea(
            attrs= {
                'rows': 1,
                'class':'input-post-title',
                'placeholder': 'Enter The Bio Of Group:',
            }
        )

        self.fields['name'].widget.attrs['class'] = 'form-control, input-post-title'
        self.fields['bio'].widget.attrs['class'] = 'form-control, input-post-title'



