from django.forms import ModelForm, CharField, TextInput, Textarea

from content.models import Post


class PostForm(ModelForm):
    class Meta:
        model = Post
        fields = ["title", "text"]
    title = CharField(widget=TextInput(attrs={'class': 'form-input'}))
    text = CharField(widget=Textarea(attrs={'class': 'form-input'}))
