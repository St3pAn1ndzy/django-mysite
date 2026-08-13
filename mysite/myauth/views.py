from django.contrib.auth import logout, authenticate, login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import TemplateView, CreateView, UpdateView, ListView, DetailView

from .models import Profile


# Create your views here.

class MyLogoutView(View):
    def get(self, request):
        logout(request)
        return redirect('myauth:login')


class AboutMeView(TemplateView):
    template_name = 'myauth/about-me.html'


class ProfileListView(ListView):
    queryset = (
        Profile.objects
        .select_related("user")
    )
    template_name = 'myauth/profiles-list.html'


class ProfileDetailView(DetailView):
    queryset = (
        Profile.objects
        .select_related("user")
    )


class UpdateProfileView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Profile
    fields = 'bio', 'avatar'
    success_url = reverse_lazy('myauth:about-me')
    template_name_suffix = '_update_form'

    def get_object(self, queryset=None):
        return get_object_or_404(Profile, pk=self.kwargs.get("pk"))

    def test_func(self):
        profile = self.get_object()
        return self.request.user.is_staff or self.request.user == profile.user


class RegisterView(CreateView):
    form_class = UserCreationForm
    template_name = 'myauth/register.html'
    success_url = reverse_lazy('myauth:about-me')

    def form_valid(self, form):
        response = super().form_valid(form)
        Profile.objects.create(user=self.object)

        user = authenticate(self.request,
                            username=form.cleaned_data['username'],
                            password=form.cleaned_data['password1']
                            )
        login(self.request, user=user)

        return response


def set_cookie_view(request: HttpRequest) -> HttpResponse:
    response = HttpResponse("Cookie set")
    response.set_cookie('username', 'admin', max_age=3600)
    return response


def get_cookie_view(request: HttpRequest) -> HttpResponse:
    value = request.COOKIES.get('username', 'user')
    return HttpResponse(f"Cookie value: {value!r}")


def set_session_view(request: HttpRequest) -> HttpResponse:
    request.session['username'] = 'admin'
    return HttpResponse("Session set")


def get_session_view(request: HttpRequest) -> HttpResponse:
    value = request.session.get('username', 'user')
    return HttpResponse(f"Session value: {value!r}")
