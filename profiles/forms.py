from django.forms import ModelForm, CharField, TextInput, ImageField, Textarea, FileInput

from profiles.models import Profile


class AdminProfileForm(ModelForm):
    class Meta:
        model = Profile
        fields = ['first_name', 'last_name', 'profile_picture', 'profile_text']
    first_name = CharField(widget=TextInput(attrs={'class': 'form-input'}))
    last_name = CharField(widget=TextInput(attrs={'class': 'form-input'}))
    profile_picture = ImageField(widget=FileInput(attrs={'class': 'form-input'}))
    profile_text = CharField(widget=Textarea(attrs={'class': 'form-input'}))

