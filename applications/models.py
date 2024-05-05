from django.db import models
from django.http import HttpRequest

from accounts.models import User


class QuestionSubclass:
    def update_values(self, data):
        assert False, "Unimplemented"

    def get_header(self):
        assert False, "Unimplemented"

    def get_result(self, request, qid):
        assert False, "Unimplemented"


class MultipleChoiceQuestion(models.Model, QuestionSubclass):
    question_text = models.CharField(max_length=300)
    description_text = models.CharField(max_length=300)

    def update_values(self, data):
        self.question_text = data['question_text']
        self.description_text = data['description_text']
        cur_list_no = int(data['cur_list_no'])
        actual_list_no = 0
        for i in range(cur_list_no):
            if ('option_' + str(i)) in data:
                text = data['option_' + str(i)]
                option = MultipleChoiceQuestionOption(answer_text=text, list_no=actual_list_no)
                actual_list_no += 1
                option.multiple_choice_question = self
                option.save()
        self.save()

    def get_header(self):
        return self.question_text

    def get_sub_header(self):
        return self.description_text

    def sorted_option_set(self):
        return self.multiplechoicequestionoption_set.order_by('list_no')

    def get_result(self, request, qid):
        value = request.POST["question{}".format(qid)]
        result = QuestionAnswer(mc_answer=int(value))
        return result


class MultipleChoiceQuestionOption(models.Model):
    answer_text = models.CharField(max_length=40)
    correct = models.BooleanField(default=False)
    list_no = models.IntegerField()
    multiple_choice_question = models.ForeignKey(MultipleChoiceQuestion, on_delete=models.CASCADE)


class ShortAnswerQuestion(models.Model, QuestionSubclass):
    question_text = models.CharField(max_length=300)
    description_text = models.CharField(max_length=300)

    def update_values(self, data):
        self.question_text = data['question_text']
        self.description_text = data['description_text']
        self.save()

    def get_header(self):
        return self.question_text

    def get_sub_header(self):
        return self.description_text

    def get_result(self, request, qid):
        value = request.POST["question{}".format(qid)]
        result = QuestionAnswer(sa_answer=value)
        return result


class FileSubmitQuestion(models.Model, QuestionSubclass):
    question_text = models.CharField(max_length=300)
    description_text = models.CharField(max_length=300)

    def update_values(self, data):
        self.question_text = data['question_text']
        self.description_text = data['description_text']
        self.save()

    def get_header(self):
        return self.question_text

    def get_sub_header(self):
        return self.description_text

    def get_result(self, request, qid):
        assert isinstance(request, HttpRequest)
        print(request.FILES)
        value = request.FILES["question{}".format(qid)]
        result = QuestionAnswer(fs_answer=value)
        return result


class DataEntryQuestion(models.Model, QuestionSubclass):
    question_text = models.CharField(max_length=300)
    description_text = models.CharField(max_length=300)

    def update_values(self, data):
        self.question_text = data['question_text']
        self.description_text = data['description_text']
        self.save()

    def get_header(self):
        return self.question_text

    def get_sub_header(self):
        return self.description_text

    def get_result(self, request, qid):
        value = request.POST["question{}".format(qid)]
        result = QuestionAnswer(da_answer=value)
        return result


class Application(models.Model):
    def create_application_response(self, request):
        assert isinstance(request, HttpRequest)
        response = ApplicationResponse(application=self, user=request.user)
        response.save()
        for question in self.question_set.all():
            print(question.id)
        for question in self.question_set.all():
            question_result = question.get_result(request)
            assert isinstance(question_result, QuestionAnswer)
            question_result.question = question
            question_result.application_response = response
            question_result.save()
        return response


class Question(models.Model):
    MULTIPLE_CHOICE = "MC"
    SHORT_ANSWER = "SA"
    FILE_SUBMIT = "FS"
    DATA_ENTRY = "DA"
    QUESTION_TYPE_CLASSES = {
        MULTIPLE_CHOICE: MultipleChoiceQuestion,
        SHORT_ANSWER: ShortAnswerQuestion,
        FILE_SUBMIT: FileSubmitQuestion,
        DATA_ENTRY: DataEntryQuestion
    }
    QUESTION_TYPE_CHOICES = (
        (MULTIPLE_CHOICE, "Multiple Choice"),
        (SHORT_ANSWER, "Short Answer"),
        (FILE_SUBMIT, "File Submit"),
        (DATA_ENTRY, "Data Entry")
    )
    QUESTION_DISPLAY_TEMPLATES = {
        MULTIPLE_CHOICE: "applications/questions/multiple_choice.html",
        SHORT_ANSWER: "applications/questions/short_answer.html",
        FILE_SUBMIT: "applications/questions/file_submit.html",
        DATA_ENTRY: "applications/questions/data_entry.html"
    }
    QUESTION_EDIT_TEMPLATES = {
        MULTIPLE_CHOICE: "applications/questions/multiple_choice_edit.html",
        SHORT_ANSWER: "applications/questions/short_answer_edit.html",
        FILE_SUBMIT: "applications/questions/file_submit_edit.html",
        DATA_ENTRY: "applications/questions/data_entry_edit.html"
    }
    QUESTION_TYPE_DESCRIPTIONS = (
        (MULTIPLE_CHOICE, "Use multiple choice questions when the applicant should choose between a few preset "
                          "options."),
        (SHORT_ANSWER, "Use short answer questions when the applicant should write a short paragraph to respond to your"
                       " question."),
        (FILE_SUBMIT, "Use file submit questions when the applicant should submit a document, like a resume or a cover "
                      "letter."),
        (DATA_ENTRY, "Use data entry questions when the applicant should write a few words at most to respond to your "
                     "question.")
    )
    question_type = models.CharField(max_length=2, choices=QUESTION_TYPE_CHOICES)
    order = models.CharField(max_length=20)  # used to define order of questions lexicographically
    question_mc = models.OneToOneField(MultipleChoiceQuestion, on_delete=models.CASCADE, null=True)
    question_sa = models.OneToOneField(ShortAnswerQuestion, on_delete=models.CASCADE, null=True)
    question_fs = models.OneToOneField(FileSubmitQuestion, on_delete=models.CASCADE, null=True)
    question_da = models.OneToOneField(DataEntryQuestion, on_delete=models.CASCADE, null=True)
    application = models.ForeignKey(Application, on_delete=models.CASCADE)

    def get_edit_template(self):
        return self.QUESTION_EDIT_TEMPLATES[self.question_type]

    def set_question_subclass(self, question_subclass):
        setattr(self, "question_" + self.question_type.lower(), question_subclass)

    def get_question_subclass(self):
        return getattr(self, "question_" + self.question_type.lower())

    def get_display_template(self):
        return self.QUESTION_DISPLAY_TEMPLATES[self.question_type]

    def update_values(self, data):
        self.get_question_subclass().update_values(data)

    def get_header(self):
        return self.get_question_subclass().get_header()

    def get_sub_header(self):
        return self.get_question_subclass().get_sub_header()

    def get_result(self, request):
        return self.get_question_subclass().get_result(request, self.id)


class ApplicationResponse(models.Model):
    application = models.ForeignKey(Application, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)


class QuestionAnswer(models.Model):
    application_response = models.ForeignKey(ApplicationResponse, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    mc_answer = models.IntegerField(default=0)
    sa_answer = models.CharField(max_length=1000, default="")
    da_answer = models.CharField(max_length=80, default="")
    fs_answer = models.FileField(null=True, upload_to="answers")
