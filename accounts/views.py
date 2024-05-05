from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.views import generic


class RegisterStudent(generic.CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy('student-profile-setup', args=[0])
    template_name = 'registration/register.html'


class RegisterDonor(generic.CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy('donor-profile-setup', args=[0])
    template_name = 'registration/register.html'
