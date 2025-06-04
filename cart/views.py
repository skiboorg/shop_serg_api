from decimal import Decimal

from rest_framework.response import Response
from rest_framework.views import APIView

from shop.models import Style
from .serializers import *
from .models import *

def get_cart(request) -> Cart:
    session_id = request.query_params.get('session_id', None)
    print('session_id',session_id)
    cart, _ = Cart.objects.get_or_create(session_uuid=session_id)
    return cart

class CartView(APIView):
    def get(self, request):
        cart = get_cart(request)
        serializer = CartSerializer(cart, many=False)
        return Response(serializer.data, status=200)


    def delete(self, request):
        product_id = request.data.get('product_id', None)
        if product_id:
            CartItem.objects.get(id=product_id).delete()
            result = {'result': True, 'message': 'Товар удален'}
        else:
            cart = get_cart(request)
            cart.delete()
            get_cart(request)
            result = {'result': True,'message':'Корзина очищена'}
        return Response(result, status=200)

    def patch(self, request):
        print(request.data)
        item = CartItem.objects.get(id=request.data['product_id'])
        amount = Decimal(request.data['amount'])
        if amount > 0:
            item.amount = amount
            item.save()
            result = {'result': True, 'message': 'Количество товара изменено'}
        else:
            item.delete()
            result = {'result': True, 'message': 'Товар удален'}
        return Response(result,status=200)

    def post(self, request):
        print(request.data)

        cart = get_cart(request)
        style_id = request.data.get('style_id', None)
        if style_id:
            style = Style.objects.get(id=style_id)
            for product in style.products.all():

                cart_item,created = CartItem.objects.get_or_create(
                    cart=cart,
                    product=product.product
                )
                if created:
                    print('created')
                    cart_item.amount = 1
                    cart_item.save()
                    result = {'result': True, 'message': 'Товар добавлен'}
                else:
                    print('updated')
                    cart_item.amount += 1
                    cart_item.save()
                    result = {'result': True, 'message': 'Количество товара изменено'}
        else:
            cart_item, created = CartItem.objects.get_or_create(
                cart=cart,
                product_id=request.data['product_id']
            )

            if created:
                print('created')
                cart_item.amount = request.data['amount']
                cart_item.save()
                result = {'result': True, 'message': 'Товар добавлен'}
            else:
                print('updated')
                cart_item.amount += request.data['amount']
                cart_item.save()
                result = {'result': True, 'message': 'Количество товара изменено'}

        return Response(result, status=200)


