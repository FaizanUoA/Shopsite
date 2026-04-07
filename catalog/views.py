# This file contains all the view functions for the catalog app.
# Each function maps to a URL and is responsible for building the right
# context and returning a rendered HTML response (or a redirect).
# Views that modify data (toggle_favourite) are restricted to POST requests
# to avoid accidental changes from browsers pre-fetching links.

from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404, redirect, render
from django.utils.http import url_has_allowed_host_and_scheme
from django.views.decorators.http import require_POST

from .models import Favourite, Item


def item_list(request):
    # Grab the search term from the URL query string, e.g. ?search=rice
    # .strip() removes accidental whitespace that users sometimes type
    search_query = request.GET.get("search", "").strip()
    # Always join with category in the same query so we don't hit the DB
    # separately for every row when the template accesses item.category.name
    items = Item.objects.select_related("category").all().order_by("price")
    if search_query:
        # Case-insensitive partial match -- "rice" will match "Basmati Rice"
        items = items.filter(name__icontains=search_query)
    # Show 10 items per page; get_page() handles out-of-range page numbers gracefully
    paginator = Paginator(items, 10)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    # Build a set of item IDs the current user has already favourited so the
    # template can show a filled/empty star without an extra query per row
    favourite_ids = set()
    if request.user.is_authenticated:
        favourite_ids = set(
            Favourite.objects.filter(user=request.user).values_list("item_id", flat=True)
        )
    context = {
        "items": page_obj.object_list,
        "page_obj": page_obj,
        "search_query": search_query,
        "favourite_ids": favourite_ids,
    }
    return render(request, "catalog/item_list.html", context)


def item_detail(request, item_id):
    # get_object_or_404 automatically returns a proper 404 page if the ID
    # doesn't exist in the database, rather than crashing with a 500 error
    item = get_object_or_404(Item.objects.select_related("category"), pk=item_id)
    # Only bother checking the Favourite table if someone is actually logged in
    is_favourite = False
    if request.user.is_authenticated:
        is_favourite = Favourite.objects.filter(user=request.user, item=item).exists()
    return render(request, "catalog/item_detail.html", {"item": item, "is_favourite": is_favourite})


def register_view(request):
    # On a GET request we just show an empty registration form.
    # On POST we validate it, save the new user, log them in straight away
    # so they don't have to sign in again, then redirect to the catalogue.
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Log the user in immediately after registering -- no separate login step needed
            login(request, user)
            messages.success(request, f"Welcome, {user.username}! Your account has been created.")
            return redirect("item_list")
    else:
        form = UserCreationForm()
    return render(request, "catalog/register.html", {"form": form})


@login_required
def favourite_list(request):
    # @login_required handles the redirect to /accounts/login/ automatically
    # if an anonymous user tries to visit this page
    favourites = Favourite.objects.filter(user=request.user).select_related(
        "item", "item__category"
    )
    return render(request, "catalog/favourites.html", {"favourites": favourites})


@login_required
@require_POST  # Only accept POST -- prevents plain links from toggling favourites
def toggle_favourite(request, item_id):
    item = get_object_or_404(Item, pk=item_id)
    # get_or_create returns a tuple: (object, created_bool)
    # If created is False, the favourite already existed so we remove it (toggle off)
    fav, created = Favourite.objects.get_or_create(user=request.user, item=item)
    if not created:
        fav.delete()
        messages.success(request, f'"{item.name}" removed from your favourites.')
    else:
        messages.success(request, f'"{item.name}" added to your favourites.')
    # Redirect back to wherever the user came from (list or detail page).
    # We validate the URL first to prevent open-redirect attacks where an attacker
    # could craft a ?next= URL pointing at a malicious external site.
    next_url = request.POST.get("next", "/")
    if not url_has_allowed_host_and_scheme(next_url, allowed_hosts={request.get_host()}):
        next_url = "/"
    return redirect(next_url)