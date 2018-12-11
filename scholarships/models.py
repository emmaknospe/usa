from django.db import models
from djmoney.forms import MoneyField

from profiles.models import DonorProfile


class KeyWord(models.Model):
    key_word = models.CharField(max_length=20, primary_key=True)


class AcademicField(models.Model):
    field_name = models.CharField(max_length=20, primary_key=True)


class MultipleChoiceQuestion(models.Model):
    question_text = models.CharField(max_length=300)


class MultipleChoiceQuestionOption(models.Model):
    answer_text = models.CharField(max_length=40)
    multiple_choice_question = models.ForeignKey(MultipleChoiceQuestion, on_delete=models.CASCADE)


class ShortAnswerQuestion(models.Model):
    question_text = models.CharField(max_length=300)


class FileSubmitQuestion(models.Model):
    question_text = models.CharField(max_length=300)


class DataEntryQuestion(models.Model):
    question_text = models.CharField(max_length=300)


class Application(models.Model):
    pass


class Question(models.Model):
    MULTIPLE_CHOICE = "MC"
    SHORT_ANSWER = "SA"
    FILE_SUBMIT = "FS"
    DATA_ENTRY = "DA"
    QUESTION_TYPE_CHOICES = (
        (MULTIPLE_CHOICE, "Multiple Choice"),
        (SHORT_ANSWER, "Short Answer"),
        (FILE_SUBMIT, "File Submit"),
        (DATA_ENTRY, "Data Entry")
    )
    question_type = models.CharField(max_length=2, choices=QUESTION_TYPE_CHOICES)
    order = models.CharField(max_length=20)  # used to define order of questions lexicographically
    application = models.ForeignKey(Application, on_delete=models.CASCADE)


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
    # TODO: handle location here and in students
