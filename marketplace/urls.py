from django.urls import path
from marketplace.views import games_views, user_dashboard_views, auth_views

urlpatterns = [
    path('', user_dashboard_views.index, name='index'),
    path('games', games_views.index, name='games'),

    path("login/", auth_views.login_view, name = "login"),
    path("logout/", auth_views.login_view, name = "logout"),
    path("register/", auth_views.register_view, name = "register"),
    path("accounts/logout/", auth_views.login_view, name = "logout1"),
    path("accounts/login", auth_views.login_view, name = "login1"),
    path("accounts/register", auth_views.register_view, name = "register1"),


]