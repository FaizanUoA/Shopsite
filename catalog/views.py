from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404, render

from .models import Item


def item_list(request):
    search_query = request.GET.get("search", "").strip()
    items = Item.objects.select_related("category").all().order_by("price")

    if search_query:
        items = items.filter(name__icontains=search_query)

    paginator = Paginator(items, 10)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    context = {
        "items": page_obj.object_list,
        "page_obj": page_obj,
        "search_query": search_query,
    }
    return render(request, "catalog/item_list.html", context)


def item_detail(request, item_id):
    item = get_object_or_404(Item.objects.select_related("category"), pk=item_id)
    return render(request, "catalog/item_detail.html", {"item": item})
