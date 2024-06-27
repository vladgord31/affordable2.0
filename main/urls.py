from django.urls import path
from main import views as main_views

app_name = "main"

urlpatterns = [
    path("", main_views.MovieView.as_view(), name="index"),
    path("about/", main_views.MovieAboutView.as_view(), name="about"),
    path("contacts/", main_views.MovieContactsView.as_view(), name="contacts"),
    path("privacy/", main_views.MoviePrivacyView.as_view(), name="privacy"),
    path("help-center/", main_views.MovieFaqView.as_view(), name="faq"),
]
