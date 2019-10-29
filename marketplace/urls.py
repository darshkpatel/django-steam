from django.urls import path
from marketplace.views import games_views, user_dashboard_views, auth_views, marketplace_views, listing_views

urlpatterns = [
    path('', user_dashboard_views.index, name='index'),
    path('games', games_views.index, name='games'),
    path('market', marketplace_views.market, name='market'),
    path('listings', listing_views.mylistings, name='listings'),
    path('market/sell', listing_views.sell, name='market_sell'),
    path('market/buy', marketplace_views.buy, name='market_buy'),
    path('listings/delete', listing_views.delete_inv, name='delete_inv'),

    # Depriciated
    # path('market_table', marketplace_views.table, name='market-table'),

    path("login/", auth_views.login_view, name = "login"),
    path("logout/", auth_views.login_view, name = "logout"),
    path("register/", auth_views.register_view, name = "register"),
    path("accounts/logout/", auth_views.login_view, name = "logout1"),
    path("accounts/login", auth_views.login_view, name = "login1"),
    path("accounts/register", auth_views.register_view, name = "register1"),


]