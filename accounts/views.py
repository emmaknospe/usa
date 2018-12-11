from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.views import generic
from accounts.models import User


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")


class RegisterStudent(generic.CreateView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('setup-student', args=[0])
    template_name = 'registration/register.html'


class RegisterDonor(generic.CreateView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('setup-donor')
    template_name = 'registration/register.html'
