from django import forms
from django.contrib.auth.models import User
# from sns.models import Message

##投稿フォーム
class PostForm(forms.Form):
    content = forms.CharField(max_length=500,widget=forms.Textarea(attrs={"class":"form-control","rows":2}))
    
    def __init__(self, user, *args, **kwargs):
        super(PostForm, self).__init__(*args, **kwargs)
