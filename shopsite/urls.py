# Root URL configuration for the entire Shopsite project.
# All three blocks below are included rather than defined here, which keeps
# this file clean and delegates the actual URL logic to each app.
#
#   /admin/      -- Django's built-in admin panel
#   /accounts/   -- Django's built-in auth views (login, logout, password change)
#   /            -- Everything in the catalog app (item list, detail, favourites, register)

from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    # Django admin interface — useful for managing data during development
    path('admin/', admin.site.urls),

    # Hooks in Django's own login/logout views at /accounts/login/ and /accounts/logout/
    # so we don't have to write authentication views ourselves
    path("accounts/", include("django.contrib.auth.urls")),

    # Mount the catalog app at the root so item_list is the homepage
    path("", include("catalog.urls")),
]
