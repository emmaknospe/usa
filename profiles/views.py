from django.http import HttpResponseServerError
from django.shortcuts import redirect, render, get_object_or_404
from django.utils.decorators import method_decorator
from django.views import generic
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import AuthenticationForm
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from django.forms.models import model_to_dict

from profiles.forms import AdminProfileForm
from profiles.models import Profile, StudentProfile, DonorProfile
from profiles.constants import *


class RegisterView(generic.CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'registration/register.html'


class LoginView(generic.FormView):
    form_class = AuthenticationForm
    success_url = reverse_lazy('redirect-to-home-view')
    template_name = 'registration/login.html'


@login_required
def redirect_to_home_view(request):
    if hasattr(request.user, "profile"):
        profile = request.user.profile
        if profile.profile_type == Profile.STUDENT:
            return redirect("student-home", tab="default")
        elif profile.profile_type == Profile.ADMIN:
            return redirect("admin-home", tab="default")
        elif profile.profile_type == Profile.DONOR:
            if request.user.authorized_donor_profile and not profile.visible:
                # do not display donor profiles if they have not created one.
                return redirect("organization-home",
                                tab='default',
                                organization_id=request.user.authorized_donor_profile.id)
            else:
                return redirect("donor-home", tab="default")
        else:
            return HttpResponseServerError("Invalid profile type.")
    else:
        return render(request, "profiles/homepage/homepage_incomplete_profile.html", {})


@login_required
def student_home(request, tab):
    context = {'profile': request.user.profile}
    tabs = ['overview', 'saved_scholarships', 'applications', 'responses', 'my_information']
    if tab in tabs:
        context['tab'] = tab
    else:
        context['tab'] = 'overview'
    return render(request, "profiles/homepage/student_homepage.html", context)


@login_required
def organization_homepage(request, tab, organization_id):
    organization = get_object_or_404(DonorProfile, id=organization_id)
    context = {'organization': organization, 'id': organization_id}
    tabs = ['overview', 'scholarships', 'applicants', 'manage']
    if tab in tabs:
        context['tab'] = tab
    else:
        context['tab'] = 'overview'
    if request.user.authorized_donor_profile == organization:
        context['authorized'] = True
    else:
        context['authorized'] = False
    return render(request, 'profiles/homepage/organization_homepage.html', context)


@login_required
def admin_home(request, tab):
    return render(request, 'profiles/homepage/admin_homepage.html')


@login_required
def donor_home(request, tab):
    return None


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
    profile = None
    if request.method == "POST":
        if request.POST.get("resume", ''):
            profile_id = request.POST['profile_id']
            profile = get_object_or_404(Profile, id=int(profile_id))
            context.update(model_to_dict(profile))
            context['profile_id'] = profile_id
        else:
            profile_id = request.POST.get('profile_id', '')
            for attr in tracked_attrs:
                context[attr] = request.POST.get(attr, defaults[attr])

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
        return redirect("setup-student", 0)
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
        return redirect("redirect-to-home-view")
    context['HS_GRADUATION_LABEL_TEXT'] = HS_GRADUATION_LABEL_TEXT_BY_STUDENT_TYPE(context['student_type'])
    context['COLLEGE_GRADUATION_LABEL_TEXT'] = COLLEGE_GRADUATION_LABEL_TEXT_BY_STUDENT_TYPE(context['student_type'])
    context['setup_stage'] = setup_stage
    return render(request, "profiles/setup_student.html", context)


@method_decorator(login_required, name='dispatch')
class SetupDonorView(generic.TemplateView):
    template_name = 'profiles/setup_donor.html'


@method_decorator(login_required, name='dispatch')
class SetupOrganizationView(generic.TemplateView):
    template_name = 'profiles/setup_organization.html'


@login_required
def process_setup_organization(request):
    if request.method == "POST":
        donor_profile = DonorProfile()
        donor_profile.organization_name = request.POST["organization_name"]
        donor_profile.donor_type = request.POST["donor_type"]
        donor_profile.logo_picture = request.FILES["logo_picture"]
        donor_profile.description_text = request.POST["description_text"]
        donor_profile.save()
        request.user.authorized_donor_profile = donor_profile
        request.user.save()
        if not hasattr(request.user, "profile"):
            # insert placeholder profile
            user_profile = Profile(first_name="", last_name="", email="", visible=False, profile_picture=None,
                                   profile_text="", profile_type="D")
            user_profile.save()
            user_profile.user = request.user
            user_profile.save()
        return redirect("index")
    else:
        return redirect("index")


def view_profile(request, profile_id):
    profile = get_object_or_404(Profile, id=profile_id)
    return render(request, "profiles/view_profile.html", {"profile": profile})


@login_required
def setup_admin(request):
    if request.method == "POST":
        form = AdminProfileForm(request.POST, request.FILES)
        if form.is_valid():
            profile_instance = form.save(commit=False)
            assert isinstance(profile_instance, Profile)
            profile_instance.user = request.user
            profile_instance.profile_type = Profile.ADMIN
            profile_instance.save()
            return redirect("index")
        else:
            return render(request, "profiles/setup_admin.html", {'form': form})
    else:
        form = AdminProfileForm()
        return render(request, "profiles/setup_admin.html", {'form': form})
