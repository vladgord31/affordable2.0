from django.views.generic.list import ListView
from django.views.generic.base import View
from django.shortcuts import render
from main.models import Movie

class MovieView(ListView):
    model = Movie
    queryset = Movie.objects.all()
    template_name = "main/index.html"
    context_object_name = "movies"

class MovieAboutView(View):
    def get(self, request):
        return render(request, "main/about.html")

class MoviePrivacyView(View):
    def get(self, request):
        return render(request, "main/privacy.html")

class MovieContactsView(View):
    def get(self, request):
        return render(request, "main/contacts.html")
    
class MovieFaqView(View):
    def get(self, request):
        return render(request, "main/faq.html")
