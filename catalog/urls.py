# URL patterns for the catalog app.
# These are included into the project's root urls.py under the empty prefix "",
# so the homepage ("/") maps directly to item_list with no extra path segment.

from django.urls import path

from . import views


urlpatterns = [
    # Homepage — shows the full item list with search and pagination
    path("", views.item_list, name="item_list"),

    # Individual item page — <int:item_id> captures the numeric primary key from the URL
    path("items/<int:item_id>/", views.item_detail, name="item_detail"),

    # Toggle favourite — POST-only; the item_id tells us which item to add/remove
    path("items/<int:item_id>/favourite/", views.toggle_favourite, name="toggle_favourite"),

    # Logged-in user's saved favourites list
    path("favourites/", views.favourite_list, name="favourite_list"),

    # Registration form for new users
    path("register/", views.register_view, name="register"),
]
