from django.urls import path
from .views import *

urlpatterns = [
    path('', index, name='index'),
    path("login/", login_view, name = "login"),
    path("logout/", login_view, name = "logout"),
    path("register/", register_view, name = "register"),
    path("accounts/logout/", login_view, name = "logout1"),
    path("accounts/login", login_view, name = "login1"),
    path("accounts/register", register_view, name = "register1"),

]