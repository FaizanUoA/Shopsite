from django.urls import path

from . import views


urlpatterns = [
    path("", views.item_list, name="item_list"),
    path("items/<int:item_id>/", views.item_detail, name="item_detail"),
    path("items/<int:item_id>/favourite/", views.toggle_favourite, name="toggle_favourite"),
    path("favourites/", views.favourite_list, name="favourite_list"),
    path("register/", views.register_view, name="register"),
]
