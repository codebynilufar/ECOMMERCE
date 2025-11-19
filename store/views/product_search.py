from django.views import View
from django.http import JsonResponse
from ..models import Product

class ProductSearchView(View):
    def get(self, request):
        query = request.GET.get("q", "")
        products = Product.objects.filter(name__icontains=query)
        result = [
            {
                "id": p.pk,
                "name": p.name,
                "price": p.price,
                "category_id": p.category_id,
            }
            for p in products
        ]
        return JsonResponse({"products": result})
