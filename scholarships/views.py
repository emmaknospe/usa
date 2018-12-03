from django.shortcuts import render, redirect

# Create your views here.
from django.views.generic import TemplateView


class IndexView(TemplateView):
    template_name = "index.html"

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('user-home')
        return super(TemplateView, self).dispatch(request, *args, **kwargs)
