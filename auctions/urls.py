from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("create", views.create, name="create"),
    path("watchlist/<int:listing_id>", views.watchlist, name="watchlist"),
    path("categories", views.categories, name="categories"),
    path("categories/<str:category_name>", views.categoryListings, name="categoryListings"),
    path("categories/<str:category_name>/<int:listing_id>", views.listing, name="listing"),
    path("myauctions", views.userAuctions, name="userAuctions"),
    path("watchlist_view", views.watchlist_view, name="watchlist_view"),
    path("closeAuction/<int:listing_id>", views.close, name="close"),
]
