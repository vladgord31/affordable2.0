from django.urls import reverse, reverse_lazy
from django.http import HttpResponseRedirect
from django.views.generic.base import View
from django.shortcuts import redirect, render
from django.contrib import auth
from users.forms import UserSigninForm, UserSignupForm
from django.contrib.auth.views import LoginView

class UserSigninView(LoginView):
    form_class = UserSigninForm
    template_name = "users/signin.html"
    extra_context = {
        'title': 'Вхід'
    }

    def get_success_url(self) -> str:
        return reverse_lazy('users:profile')

class UserSignupView(View):
    def post(self, request):
        form = UserSignupForm(data=request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password1'])
            user.save()
            return HttpResponseRedirect(reverse("users:profile"))
        
        context = {
            "form": form
        }
        return render(request, "users/signup.html", context)

    def get(self, request):
        form = UserSignupForm()
        context = {
            "form": form
        }
        return render(request, "users/signup.html", context)

class UserForgotView(View):
    def get(self, request):
        return render(request, "users/forgot.html")

class UserSignoutView(View):
    def post(self, request):
        auth.logout(request)
        return redirect(reverse("main:index"))

class UserProfileView(View):
    def get(self, request):
        return render(request, "users/profile.html")
