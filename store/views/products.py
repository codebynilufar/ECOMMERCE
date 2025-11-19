import json
from django.views import View
from django.http import JsonResponse, HttpRequest
from ..models import Category, Product, ProductImage
from django.shortcuts import get_object_or_404


class ProductListView(View):
    def get(self, request: HttpRequest) -> JsonResponse:
        products = [
            {
                "id": p.pk,
                "name": p.name,
                "price": p.price,
                "category_id": p.category_id,
                "images": [img.image.url for img in p.images.all()],
                "created_at": p.created_at.isoformat(),
                "updated_at": p.updated_at.isoformat(),
            }
             for p in Product.objects.all().prefetch_related("images")

        ]
        return JsonResponse({"products": products}, status=200)
    


    def post(self, request: HttpRequest) -> JsonResponse:
        try:
            data = json.loads(request.body)
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON format."}, status=400)

        name = data.get("name")
        price = data.get("price")
        category_id = data.get("category_id")      

        if not name:
            return JsonResponse({"name": "Required."}, status=400)

        if price is None:
            return JsonResponse({"price": "Required."}, status=400)

        if category_id is None:
            return JsonResponse({"category_id": "Required."}, status=400)

        
        category = get_object_or_404(Category, pk=category_id)

        
        product = Product.objects.create(
            name=name,
            price=price,
            category=category
        )

        
        images = data.get("images", [])  

        if not isinstance(images, list):
            return JsonResponse({"images": "Must be list."}, status=400)

        for img_path in images:
            ProductImage.objects.create(
                product=product,
                image=img_path
            )

    
        return JsonResponse(
            {
                "id": product.pk,
                "name": product.name,
                "price": product.price,
                "category_id": product.category_id,
                "images": [img.image.url for img in product.images.all()],
                "created_at": product.created_at.isoformat(),
                "updated_at": product.updated_at.isoformat(),
            },
            status=201
        )     
        

      
        
        
class ProductDetailView(View):

    def get(self, request: HttpRequest, pk: int) -> JsonResponse:
        product = get_object_or_404(Product.objects.prefetch_related("images"), pk=pk)

        data = {
            "id": product.pk,
            "name": product.name,
            "price": product.price,
            "category_id": product.category_id,
            "images": [img.image.url for img in product.images.all()],
            "created_at": product.created_at.isoformat(),
            "updated_at": product.updated_at.isoformat(),
        }

        return JsonResponse(data, status=200)



    def put(self, request: HttpRequest, pk: int) -> JsonResponse:
        try:
            data = json.loads(request.body)
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON"}, status=400)

        product = get_object_or_404(Product, pk=pk)

        name = data.get("name", product.name)
        price = data.get("price", product.price)
        category_id = data.get("category_id", product.category_id)

        category = None
        if category_id:
            category = get_object_or_404(Category, pk=category_id)

        product.name = name
        product.price = price
        product.category = category
        product.save()

   
        images = data.get("images")

        if images is not None:
            if not isinstance(images, list):
                return JsonResponse({"images": "Must be list."}, status=400)

            product.images.all().delete()

            for img_path in images:
                ProductImage.objects.create(product=product, image=img_path)

        updated = {
            "id": product.pk,
            "name": product.name,
            "price": product.price,
            "category_id": product.category_id,
            "images": [img.image.url for img in product.images.all()],
            "created_at": product.created_at.isoformat(),
            "updated_at": product.updated_at.isoformat(),
        }

        return JsonResponse(updated, status=200)



    def delete(self, request: HttpRequest, pk: int) -> JsonResponse:
        product = get_object_or_404(Product, pk=pk)
        product.delete()
        return JsonResponse({"message": "Product deleted successfully."}, status=204)
