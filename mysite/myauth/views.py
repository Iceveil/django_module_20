import profile
from urllib import request

from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from django.contrib.auth.views import LogoutView
from django.http import HttpRequest, HttpResponse, JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse, reverse_lazy
from django.views import View
from django.views.generic import TemplateView, CreateView, UpdateView, ListView

from .models import Profile, user_image_directory_path
from .forms import AvatarForm


class AboutMeView(LoginRequiredMixin, UpdateView):
    template_name = 'myauth/about-me.html'
    model = Profile
    form_class = AvatarForm
    success_url = reverse_lazy('myauth:about-me')

    def get_object(self, queryset = None):
        profile, _ = Profile.objects.get_or_create(user=self.request.user)
        return profile



class RegisterView(CreateView):
    form_class = UserCreationForm
    template_name = 'myauth/register.html'
    success_url = reverse_lazy('myauth:about-me')

    def form_valid(self, form):
        response = super().form_valid(form)
        Profile.objects.create(user=self.object)

        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password1')

        user = authenticate(self.request,
                            username=username,
                            password=password)
        login(self.request, user)
        return response


def login_view(request: HttpRequest):
    if request.method == 'GET':
        if request.user.is_authenticated:
            return redirect('/admin/')
        return render(request,'myauth/login.html')

    username = request.POST['username']
    password = request.POST['password']

    user = authenticate(request, username=username, password=password)

    if user is not None:
        login(request, user)
        return redirect('/admin/')

    return render(request,'myauth/login.html', {'error': 'Invalid login credentials'})

#
# def logout_view(request: HttpRequest):
#     logout(request)
#     return redirect(reverse('myauth:login'))


class MyLogoutView(View):
    def get(self, request: HttpRequest):
        logout(request)
        return redirect('myauth:login')



def set_cookie_view(request: HttpRequest) -> HttpResponse:
    response = HttpResponse('Cookie set')
    response.set_cookie('fizz', 'buzz' , max_age=3600)
    return response

def get_cookie_view(request: HttpRequest) -> HttpResponse:
    value = request.COOKIES.get('fizz', 'default value')
    return HttpResponse(f'Cookie value = {value!r}')

def set_session_view(request: HttpRequest) -> HttpResponse:
    request.session['foobar'] = 'spamegs'
    return HttpResponse('Session set!')

def get_session_view(request: HttpRequest) -> HttpResponse:
    value = request.session.get('foobar', 'default value')
    return HttpResponse(f'Session Value = {value!r}')


class FooBarView(View):
    def get(self, request: HttpRequest) -> JsonResponse:
        return JsonResponse({'foo': 'bar', 'spam': 'eggs'})


class UsersListView(ListView):
    queryset = User.objects.all()
    template_name = 'myauth/users-list.html'
    context_object_name = 'users'
    model = User


class ChangeAvatarView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    template_name = 'myauth/change_avatar.html'
    form_class = AvatarForm
    model = Profile

    def test_func(self):
        profile = self.get_object()
        if self.request.user.is_staff or profile.user == self.request.user:
            return True
        return False

    def get_success_url(self):
        return reverse_lazy('myauth:users_list')

    def get_object(self, queryset = None):
        return get_object_or_404(Profile, user_id=self.kwargs['user_id'])
