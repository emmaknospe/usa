from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from scholarships.constants import ACADEMIC_DISCIPLINES
from scholarships.models import Scholarship, KeyWord, AcademicField
from django.db.models import Q

# Create your views here.
from django.views.generic import TemplateView


class IndexView(TemplateView):
    template_name = "index.html"

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('redirect-to-home-view')
        return super(TemplateView, self).dispatch(request, *args, **kwargs)


@login_required
def search_scholarships(request):
    if request.method == "POST":
        print("Error, only gets")
        # TODO Better error here
    scholarships = Scholarship.objects
    params = request.GET
    zipped_disciplines = []
    selected_fields = []
    for field in ACADEMIC_DISCIPLINES:
        #  instantiate mini-object to zip up our date
        if field != "No Specific Field":
            pair = type('pair', (object,), {"name": field, "on": bool(params.get(field, ""))})()
            zipped_disciplines.append(pair)
            if params.get(field, ""):
                selected_fields.append(field)
    params_without_disciplines = {key: params[key] for key in params if key not in ACADEMIC_DISCIPLINES}
    context = {"zipped_disciplines": zipped_disciplines}
    context.update(params_without_disciplines)
    # search logic starts here
    fields_q = None
    for field in selected_fields:
        if fields_q:
            fields_q = fields_q | Q(fields__field_name=field)
        else:
            fields_q = Q(fields__field_name=field)
    if fields_q:
        scholarships = scholarships.filter(fields_q)
    if params.get("key_words", ""):
        key_words = params['key_words'].split(",")
        key_word_q = None
        for key_word in key_words:
            if key_word_q:
                key_word_q = key_word_q | Q(key_words__key_word__iexact=key_word)
            else:
                key_word_q = Q(key_words__key_word__iexact=key_word)
        if key_word_q:
            scholarships = scholarships.filter(key_word_q)
    if params.get("title", ""):
        scholarships = scholarships.filter(title__icontains=params.get("title"))
    context['scholarships'] = scholarships.all()
    if params.get("view", "") == "card":
        context['tile'] = False
        context['view'] = 'card'
    else:
        context['tile'] = True
        context['view'] = 'list'
    return render(request, "scholarships/search_scholarships.html", context)

@login_required
def create_scholarship(request, organization_id):
    context = {"organization_id": organization_id,
               "key_words_string_list": "",
               "required_gpa": "",
               "key_words": [],
               "fields_string_list": "",
               "fields": [],
               "title": "",
               "amount": "",
               "description": ""}
    if request.user.authorized_donor_profile.id == organization_id:
        context['authorized'] = True
    else:
        context['authorized'] = False
    if request.method == "POST":
        if request.POST.get("action", "") == "submit_form":
            key_words = request.POST.get("key_words_string_list", "").split(",")
            fields = request.POST.get("fields_string_list", "").split(",")
            required_gpa = int(request.POST.get("required_gpa", ""))
            title = request.POST.get("title", "")
            amount = float(request.POST.get("amount", ""))
            description = request.POST.get("description")
            scholarship = Scholarship(required_gpa=required_gpa, title=title, description=description)
            scholarship.amount = amount
            scholarship.organization_id = organization_id
            scholarship.save()
            for key_word in key_words:
                key_word_entry, created = KeyWord.objects.get_or_create(key_word=key_word)
                scholarship.key_words.add(key_word_entry)
            for field in fields:
                field_entry, created = AcademicField.objects.get_or_create(field_name=field)
                scholarship.fields.add(field_entry)
            scholarship.save()
            return redirect('view-scholarship', scholarship_id=scholarship.id)
        else:
            key_word_old_string = request.POST.get("key_words_string_list", "")
            key_words = []
            fields = []
            if key_word_old_string:
                key_words = key_word_old_string.split(",")
            field_old_string = request.POST.get("fields_string_list", "")
            if field_old_string:
                fields = field_old_string.split(",")

            if request.POST.get("action", "") == "add_key_word":
                new_key_word = request.POST.get("new_key_word", "")
                if ',' in new_key_word:
                    print("Failed validation!")  # TODO: Handle validation, basically everywhere
                if new_key_word not in key_words:
                    key_words.append(new_key_word)
            elif request.POST.get("delete_key_word", ""):
                key_word_to_delete = request.POST.get("delete_key_word")
                if key_word_to_delete in key_words:
                    key_words.remove(key_word_to_delete)
            elif request.POST.get("action", "") == "add_field":
                new_field = request.POST.get("new_field")
                if ',' in new_field:
                    print("Failed validation!")  # TODO: Handle validation, basically everywhere
                if new_field not in fields:
                    fields.append(new_field)
            elif request.POST.get("delete_field", ""):
                field_to_delete = request.POST.get("delete_field")
                if field_to_delete in fields:
                    fields.remove(field_to_delete)

            context['key_words_string_list'] = ','.join(key_words)
            context['key_words'] = key_words
            context['fields_string_list'] = ','.join(fields)
            context['fields'] = fields
            context['required_gpa'] = request.POST.get("required_gpa")
            context['title'] = request.POST.get("title", "")
            context['amount'] = float(request.POST.get("amount", ""))
            context['description'] = request.POST.get("description")

    context['ACADEMIC_DISCIPLINES'] = ACADEMIC_DISCIPLINES
    return render(request, "scholarships/create_scholarship.html", context)


@login_required
def view_scholarship(request, scholarship_id):
    # refactor into distinct views for donors/students
    scholarship = get_object_or_404(Scholarship, id=scholarship_id)
    return render(request, "scholarships/view_scholarship.html", {"scholarship": scholarship})


def get_similar_key_words(request, key_word):
    key_words = KeyWord.objects.filter(key_word__istartswith=key_word)[:4]
    return render(request, "utilities/key_word_recommendations.html", {"key_words": key_words})
