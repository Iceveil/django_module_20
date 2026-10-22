from django.contrib.auth.views import LoginView
from django.urls import path, include
from django.conf.urls.i18n import i18n_patterns
from django.contrib import admin

from .views import (
get_cookie_view,
set_cookie_view,
set_session_view,
get_session_view,
MyLogoutView,
AboutMeView,
RegisterView,
FooBarView,
UsersListView,
ChangeAvatarView
)


app_name = 'myauth'

urlpatterns = [
    path("login/", LoginView.as_view(template_name='myauth/login.html',
                                     redirect_authenticated_user=True), name='login'),
    path('logout/', MyLogoutView.as_view(), name='logout' ),
    path('cookie/get/', get_cookie_view, name='cookie_get'),
    path('cookie/set/', set_cookie_view, name='cookie_set'),
    path('session/get/', get_session_view, name='session_get'),
    path('session/set/', set_session_view, name='session_set'),
    path('about-me/', AboutMeView.as_view(), name='about-me'),
    path('register/', RegisterView.as_view(), name='register' ),
    path('foo-bar/', FooBarView.as_view(), name='foo-bar'),
    path('users/', UsersListView.as_view(), name='users_list'),
    path('users/<int:user_id>/avatar/', ChangeAvatarView.as_view(), name='change_avatar'),
]

