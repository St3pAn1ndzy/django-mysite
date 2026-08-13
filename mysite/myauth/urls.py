from django.contrib.auth.views import LoginView
from django.urls import path

from .views import (
    MyLogoutView,
    set_cookie_view,
    get_cookie_view,
    set_session_view,
    get_session_view,
    AboutMeView,
    RegisterView,
    UpdateProfileView,
    ProfileListView,
    ProfileDetailView,
)

app_name = 'myauth'

urlpatterns = [
    path('login/',
         LoginView.as_view(
             template_name='myauth/login.html',
             redirect_authenticated_user=True,
         ),
         name='login'),
    path('logout/', MyLogoutView.as_view(), name='logout'),
    path('register/', RegisterView.as_view(), name='register'),
    path('profiles/', ProfileListView.as_view(), name='profile-list'),
    path('profiles/<int:pk>', ProfileDetailView.as_view(), name='profile-details'),
    path('about-me/', AboutMeView.as_view(), name='about-me'),
    path('about-me/<int:pk>/update/', UpdateProfileView.as_view(), name='about-me-update'),
    path('cookie/get/', get_cookie_view, name='cookie-get'),
    path('cookie/set/', set_cookie_view, name='cookie-set'),
    path('session/get/', get_session_view, name='session-get'),
    path('session/get/', get_session_view, name='session-get'),
    path('session/set/', set_session_view, name='session-set'),
]
