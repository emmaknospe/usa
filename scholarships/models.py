from django.db import models
from djmoney.models.fields import MoneyField

from applications.models import Application
from profiles.models import DonorProfile


class KeyWord(models.Model):
    key_word = models.CharField(max_length=20, primary_key=True)


class AcademicField(models.Model):
    field_name = models.CharField(max_length=20, primary_key=True)


class Scholarship(models.Model):
    title = models.CharField(max_length=25)
    amount = MoneyField(max_digits=19, decimal_places=2, default_currency='USD')
    required_gpa = models.FloatField()
    key_words = models.ManyToManyField(KeyWord, related_name="scholarships")
    fields = models.ManyToManyField(AcademicField, related_name="fields")
    description = models.CharField(max_length=2000)
    visible = models.BooleanField(default=False)
    organization = models.ForeignKey(DonorProfile, on_delete=models.CASCADE)
    # Constraint: If scholarship is visible, application must exist
    application = models.OneToOneField(Application, on_delete=models.SET_NULL, default=None, blank=True, null=True)

    def short_description(self):
        if len(self.description) > 100:
            return self.description[0:100] + "..."
        else:
            return self.description

    def get_responses(self):
        return self.application.applicationresponse_set.all()

    def get_related_scholarships(self):
        # TODO: FIX
        return []
        if Scholarship.objects.count() > 4:
            return Scholarship.objects.exclude(id == self.id)[0:3]
        else:
            return Scholarship.objects.exclude(id == self.id)
    # TODO: handle location here and in students
