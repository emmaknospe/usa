from django.contrib.auth.models import User
from django.db import models
from djmoney.models.fields import MoneyField

# Create your models here.


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


class OrganizationProfile(models.Model):
    organization = models.CharField(max_length=30)


class Profile(models.Model):
    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=20)
    email = models.CharField(max_length=40)
    profile_picture = models.ImageField(upload_to="images")
    user = models.OneToOneField(User, on_delete=models.SET_NULL, null=True, related_name="profile")
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
    organization_profile = models.ForeignKey(OrganizationProfile,
                                             on_delete=models.SET_NULL,
                                             default=None,
                                             blank=True,
                                             null=True)

