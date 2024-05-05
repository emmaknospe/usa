import json

from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404, redirect

# Create your views here.
from applications.models import Question, Application, ApplicationResponse
from profiles.models import Profile
from scholarships.models import Scholarship


@login_required
def create_question(request, question_type):
    question = Question(question_type=question_type)
    question.set_question_subclass(Question.QUESTION_TYPE_CLASSES[question_type]())
    return render(request, question.get_edit_template(), context={"question": question, "saved": False})


@login_required
def edit_question(request, question_id):
    question = get_object_or_404(Question, id=question_id)
    return render(request, question.get_edit_template(), context={"question": question, "saved": False})


@login_required
def delete_question(request, question_id):
    question = get_object_or_404(Question, id=question_id)
    if request.user.can_edit_scholarship(question.application.scholarship):
        question.delete()
        return JsonResponse({"status": "success"})
    else:
        return JsonResponse({"status": "not authorized"})


@login_required
def edit_question_save(request):
    if request.method == "POST":
        data = json.loads(request.POST['form_data'])
        question = None
        application = get_object_or_404(Application, id=request.POST['application_id'])
        if request.POST['create'] == "true":  # wonky javascript true vs python True. Probably a smart way to do this
            question_type = request.POST['type']
            question = Question(question_type=question_type)
            subclass = Question.QUESTION_TYPE_CLASSES[question_type]()
            subclass.save()
            question.set_question_subclass(subclass)
            question.application = application
            question.save()
            print(application.question_set.count())
            application.question_set.add(question)
            print(application.question_set.count())
        else:
            question = get_object_or_404(Question, id=request.POST['question_id'])

        question.update_values(data)
        return render(request, question.get_display_template(), context={"question": question, "editing": True})
    else:
        # TODO: handle error here
        pass


@login_required
def create_application(request, scholarship_id):
    scholarship = get_object_or_404(Scholarship, id=scholarship_id)
    if request.user.authorized_donor_profile.id == scholarship.organization_id:
        authorized = True
    else:
        authorized = False
    if scholarship.visible:
        # TODO: redirect/edit if scholarship has existing application
        pass
    if scholarship.application:
        application = scholarship.application
    else:
        application = Application()
        application.save()
        scholarship.application = application
        scholarship.save()
    question_type_choices = Question.QUESTION_TYPE_CHOICES
    return render(request, "applications/edit_application.html",
                  {"scholarship": scholarship,
                   "authorized": authorized,
                   "question_type_choices": question_type_choices,
                   "question_type_descriptions": Question.QUESTION_TYPE_DESCRIPTIONS,
                   "questions": application.question_set.order_by("order"),
                   "application": application
                   })


def apply(request, scholarship_id):
    scholarship = get_object_or_404(Scholarship, id=scholarship_id)
    application = scholarship.application
    questions = application.question_set.order_by("order")
    # TODO: redirect and auto-apply if no questions in application
    authorized = request.user.get_role() == Profile.STUDENT and scholarship.visible
    return render(request, "applications/apply.html", {"application": application, "scholarship": scholarship,
                                                       "authorized": authorized, "questions": questions})


@login_required
def submit_application(request, application_id):
    if request.method == "POST":
        application = get_object_or_404(Application, id=application_id)
        application.create_application_response(request)
        return redirect("index")
    else:
        pass # TODO: gracefully handle gets here


def withdraw_application(request, application_response_id):
    response = get_object_or_404(ApplicationResponse, id=application_response_id)
    response.delete()
    return redirect("student-home", tab="applications")