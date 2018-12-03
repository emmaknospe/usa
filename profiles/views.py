from django.http import HttpResponseServerError
from django.shortcuts import redirect, render, get_object_or_404
from django.utils.decorators import method_decorator
from django.views import generic
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import AuthenticationForm
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from django.forms.models import model_to_dict

from profiles.models import Profile, StudentProfile
from profiles.constants import *


class RegisterView(generic.CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'registration/register.html'


class LoginView(generic.FormView):
    form_class = AuthenticationForm
    success_url = reverse_lazy('user-home')
    template_name = 'registration/login.html'


@method_decorator(login_required, name='dispatch')
class UserHomeView(generic.TemplateView):
    template_name = 'profiles/user_homepage_overview.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        try:
            context['profile'] = self.request.user.profile
        except Profile.DoesNotExist:
            context['profile'] = None
        return context


@login_required
def setup_student(request, setup_stage):
    defaults = {'error': '',
                'first_name': '',
                'last_name': '',
                'email': '',
                'profile_text': '',
                'student_type': 'C',
                'school': '',
                'dob': '',
                'hs_grad_year': '',
                'college_grad_year': '',
                'profile_id': '',
                'hometown': '',
                'college_town': '',
                'tuition': ''}
    context = defaults.copy()
    ignore_attrs = ['error']
    tracked_attrs = [key for key in context.keys() if key not in ignore_attrs]
    print(tracked_attrs)
    profile = None
    if request.method == "POST":
        if request.POST.get("resume", ''):
            print("resuming")
            profile_id = request.POST['profile_id']
            profile = get_object_or_404(Profile, id=int(profile_id))
            context.update(model_to_dict(profile))
            print(model_to_dict(profile))
            context['profile_id'] = profile_id
        else:
            print("not resuming")
            profile_id = request.POST.get('profile_id', '')
            for attr in tracked_attrs:
                context[attr] = request.POST.get(attr, defaults[attr])
                print("Set " + attr + "to " + str(context[attr]))

            if profile_id != '':
                profile = get_object_or_404(Profile, id=int(profile_id))
                profile.first_name = context['first_name']
                profile.last_name = context['last_name']
                profile.email = context['email']
                profile.profile_text = context['profile_text']
                profile.save()
            action = request.POST.get('action', 'next')
            if action == "next":
                setup_stage += 1
            elif action == "previous":
                setup_stage -= 1
            else:
                return HttpResponseServerError("Invalid action")
    elif setup_stage != 0:
        return redirect("student-profile-setup", 0)
    print(context)
    if setup_stage == 3:
        if not hasattr(request.user, "profile"):
            profile = Profile()
            profile.profile_picture = request.FILES["profile_picture"]
            profile.first_name = request.POST['first_name']
            profile.last_name = request.POST['last_name']
            profile.email = request.POST['email']
            profile.profile_text = request.POST['profile_text']
            profile.profile_type = profile.STUDENT
            profile.user = request.user
            profile.save()
            context['profile_id'] = profile.id
    if setup_stage == 5:
        if not profile:
            return HttpResponseServerError("Invalid profile setup.")
        student_profile = StudentProfile()
        student_profile.student_type = request.POST['student_type']
        student_profile.dob = request.POST['dob']
        student_profile.hs_grad_year = int(request.POST['hs_grad_year'])
        student_profile.college_grad_year = int(request.POST['college_grad_year'])
        student_profile.tuition_goal = int(request.POST['tuition'])
        student_profile.tuition_raised = 0
        student_profile.save()
        profile.student_profile = student_profile
        profile.save()
        print("this occurred")
        return redirect("user-home")
    context['HS_GRADUATION_LABEL_TEXT'] = HS_GRADUATION_LABEL_TEXT_BY_STUDENT_TYPE(context['student_type'])
    context['COLLEGE_GRADUATION_LABEL_TEXT'] = COLLEGE_GRADUATION_LABEL_TEXT_BY_STUDENT_TYPE(context['student_type'])
    context['setup_stage'] = setup_stage
    return render(request, "profiles/setup_student.html", context)


@login_required
def setup_donor(request, setup_stage):
    context = {'error': '',
               'first_name': '',
               'last_name': '',
               'email': '',
               'profile_text': '',
               }

    if request.method == "POST":
        context['first_name'] = request.POST.get('first_name', '')
        context['last_name'] = request.POST.get('last_name', '')
        context['email'] = request.POST.get('email', '')
        context['profile_text'] = request.POST.get('profile_text', '')
        action = request.POST.get('action', 'next')
        if action == "next":
            setup_stage += 1
        elif action == "previous":
            setup_stage -= 1
    if setup_stage == 3:
        profile = Profile()
        profile.profile_picture = request.FILES["profile_picture"]
        profile.first_name = request.POST['first_name']
        profile.last_name = request.POST['last_name']
        profile.email = request.POST['email']
        profile.profile_text = request.POST['profile_text']
        profile.profile_type = profile.DONOR
        profile.user = request.user
        profile.save()
        return redirect("user-home")

    context['setup_stage'] = setup_stage
    return render(request, "profiles/setup_donor.html", context)
