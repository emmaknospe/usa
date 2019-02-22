from django.contrib.auth.models import User
from django.db import models
from djmoney.models.fields import MoneyField

# Create your models here.
from usa import settings


class StudentProfile(models.Model):
    school = models.CharField(max_length=30)
    HIGH_SCHOOL = "H"
    COLLEGE = "C"
    GRADUATE = "G"
    STUDENT_TYPE_CHOICES = (
        (HIGH_SCHOOL, "High School"),
        (COLLEGE, "College"),
        (GRADUATE, "Graduate")
    )
    student_type = models.CharField(max_length=1, choices=STUDENT_TYPE_CHOICES, default=COLLEGE)
    hometown = models.CharField(max_length=128)
    college_town = models.CharField(max_length=128)
    dob = models.DateField()
    hs_grad_year = models.IntegerField()
    college_grad_year = models.IntegerField()
    tuition_goal = MoneyField(max_digits=19, decimal_places=2, default_currency='USD')
    tuition_raised = MoneyField(max_digits=19, decimal_places=2, default_currency='USD')

    def get_tuition_remaining(self):
        return self.tuition_goal - self.tuition_raised

    def get_summary(self):
        return "{} | {} | {}".format(self.hometown if self.hometown else "Not Listed",
                                 self.get_student_type_display(), self.college_grad_year)

    def get_progress(self):
        return int(round(self.tuition_raised / self.tuition_goal * 100))


class DonorProfile(models.Model):
    organization_name = models.CharField(max_length=30)
    logo_picture = models.ImageField(upload_to="images", null=True)
    description_text = models.CharField(max_length=2000)
    INDIVIDUAL = "I"
    BUSINESS = "B"
    FOUNDATION = "F"
    DONOR_TYPE_CHOICES = (
        (INDIVIDUAL, "Individual"),
        (BUSINESS, "Business"),
        (FOUNDATION, "Foundation")
    )
    donor_type = models.CharField(max_length=1, choices=DONOR_TYPE_CHOICES, default=BUSINESS)

    def get_scholarship_count(self):
        return self.scholarship_set.count()


class Profile(models.Model):
    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=20)
    email = models.CharField(max_length=40)
    visible = models.BooleanField(default=True)
    profile_picture = models.ImageField(upload_to="images", null=True)
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, related_name="profile")
    profile_text = models.CharField(max_length=2000)
    STUDENT = "S"
    ADMIN = "A"
    DONOR = "D"
    PROFILE_TYPE_CHOICES = (
        (STUDENT, "Student"),
        (ADMIN, "Admin"),
        (DONOR, "Donor")
    )
    profile_type = models.CharField(max_length=1, choices=PROFILE_TYPE_CHOICES, default=ADMIN)
    student_profile = models.OneToOneField(StudentProfile,
                                           on_delete=models.SET_NULL,
                                           default=None,
                                           blank=True,
                                           null=True)

    def get_full_name(self):
        return self.first_name + " " + self.last_name

    def sent_applications(self):
        return self.user.applicationresponse_set.all()

    def get_initials(self):
        return (self.first_name[0] + self.last_name[0]).upper()

    def get_description(self):
        if self.profile_type == self.STUDENT:
            return "Class of {}".format(self.student_profile.college_grad_year)

    def get_scholarship_count(self):
        return self.user.applicationresponse_set.count();

