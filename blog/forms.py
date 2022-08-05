from .models import Post, Comment
from django.forms import ModelForm, Textarea
 

class PostCreateForm(ModelForm):

    class Meta:
        model = Post
        fields = ('title', 'content')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['title'].widget = Textarea(
            attrs= {
                'rows': 1,
                'class':'input-post-title',
                'placeholder': 'Enter The Title:',
                
            }
        )

        self.fields['content'].widget = Textarea(
            attrs= {
                'rows': 10,
                'class':'input-comment',
                'placeholder': 'Share Your Thoughts:',
                
            }
        )
        
        self.fields['title'].widget.attrs['class'] = 'form-control, input-post-title'
        self.fields['content'].widget.attrs['class'] = 'form-control, input-post-content'


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
        
        
