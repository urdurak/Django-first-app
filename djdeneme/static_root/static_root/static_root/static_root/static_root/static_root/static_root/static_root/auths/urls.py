from django.urls import path, re_path
from .views import register,user_login , user_logout , user_profile ,user_settings , user_password_change , my_favorites


urlpatterns =[
    path("register/" , register , name="register"),
    path("login/" , user_login , name="user-login"),
    path("logout/" , user_logout , name="user-logout"),
    path("settings/", user_settings , name="user-settings"),
    path("settings/change-password/" , user_password_change , name="user-password-change"),
    re_path(r'^(?P<username>[\w-]+)/$' , user_profile , name="user-profile"),
    re_path(r'^(?P<username>[\w-]+)/my_favorites/$', my_favorites, name="my-favorite"),
]
