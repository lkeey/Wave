from .models import Post, Comment
from django.forms import ModelForm, Textarea
 

class PostCreateForm(ModelForm):

    class Meta:
        model = Post
        fields = ('title', 'content')


class CommentForm(ModelForm):
 
    class Meta:
        model = Comment
        fields = ('content',) 

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['content'].widget = Textarea(
            attrs= {
                'rows': 2,
                'class':'input-comment',
                'placeholder': 'Write here you comment:',
                
            }
        )

        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'
        
        
