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
    search_query = request.GET.get("search", "").strip()
    items = Item.objects.select_related("category").all().order_by("price")

    if search_query:
        items = items.filter(name__icontains=search_query)

    paginator = Paginator(items, 10)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

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
    item = get_object_or_404(Item.objects.select_related("category"), pk=item_id)
    is_favourite = False
    if request.user.is_authenticated:
        is_favourite = Favourite.objects.filter(user=request.user, item=item).exists()
    return render(request, "catalog/item_detail.html", {"item": item, "is_favourite": is_favourite})


def register_view(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, f"Welcome, {user.username}! Your account has been created.")
            return redirect("item_list")
    else:
        form = UserCreationForm()
    return render(request, "catalog/register.html", {"form": form})


@login_required
def favourite_list(request):
    favourites = Favourite.objects.filter(user=request.user).select_related(
        "item", "item__category"
    )
    return render(request, "catalog/favourites.html", {"favourites": favourites})


@login_required
@require_POST
def toggle_favourite(request, item_id):
    item = get_object_or_404(Item, pk=item_id)
    fav, created = Favourite.objects.get_or_create(user=request.user, item=item)
    if not created:
        fav.delete()
        messages.success(request, f"“{item.name}” removed from your favourites.")
    else:
        messages.success(request, f"“{item.name}” added to your favourites.")
    next_url = request.POST.get("next", "/")
    if not url_has_allowed_host_and_scheme(next_url, allowed_hosts={request.get_host()}):
        next_url = "/"
    return redirect(next_url)
