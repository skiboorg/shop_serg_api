import json
import requests
from dadata import Dadata
from dotenv import load_dotenv
from collections import defaultdict
import os

from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import generics, status

from cart.views import get_cart
from .serializers import *
from .models import *

from requests.exceptions import RequestException

load_dotenv()

import uuid
class OrderView(APIView):
    def get(self, request):
        print(request.data)
        result = {}
        return Response(status=200)

    def delete(self, request):
        print(request.data)
        result = {}
        return Response(status=200)

    def patch(self, request):
        print(request.data)
        result = {}
        return Response(result,status=200)

    def post(self, request):
        data = request.data
        print(data)
        cart = get_cart(request)
        # payment_type_id = data.get('payment',None)
        # delivery_type_id = data.get('delivery',None)
        # payment_type = Payment.objects.get(id=payment_type_id)
        # if not payment_type_id:
        #     payment_type = Payment.objects.first()
        #     delivery_type_id = Delivery.objects.first().id

        order_data = {
            "order":
                {
                    "id":"9f436c59c9b8201db22e67477497e6c0",
                    "delivery_sum":368,
                    "payment_type":2,
                    "send_date":"05.06.2025",
                    "comment":"",
                    "weight":100,
                    "city_id":"79b806cd-e36c-48fc-b82c-8cbb5cfd9450",
                    "place_id":291329,
                    "index":None,
                    "street":"ул Алексеевский Пост",
                    "building_1":"5",
                    "options":
                        {"partial_return":0,
                         "manual_confirm":False,
                         "delivery_asap":True
                         }
                },
            "customer":
                {
                    "firstname":"Марина",
                    "middlename":"Александровна",
                    "lastname":"Карельская",
                    "phone":"+79213056193",
                    "email":"nekonaeko@mail.ru",
                    "address":"г Москва, ул Алексеевский Пост, д 5"
                },
            "items":[
                {
                    "name":"Rich B*tch",
                    "item_id":"notcatart Rich",
                    "quantity":1,"price":"2990"
                },
                {"name":"Style is War",
                 "item_id":"notcatart Style",
                 "quantity":1,
                 "price":"2990"
                 }
            ]
        }
        new_order = Order.objects.create(
            order_id=data['order_id'],
            customer=data['fio'],
            phone=data['phone'],
            email=data['email'],
            # comment=data['comment'],
            # payment_type=payment_type,
            # delivery_type_id=delivery_type_id,
            # delivery_address=data['delivery_address']
        )
        for item in cart.items.all():
            OrderItem.objects.create(
                order=new_order,
                article=item.product.article,
                name=item.product.name,
                price=item.product.price,
                amount=item.amount
            )
            item.delete()


        result = {'result': True, 'message': f'Заказ {new_order.id} создан'}
        return Response(result, status=200)


class GetDeliveries(generics.ListAPIView):
    serializer_class = DeliverySerializer
    queryset = Delivery.objects.all()

class GetPayments(generics.ListAPIView):
    serializer_class = PaymentSerializer
    queryset = Payment.objects.all()

class GetDeliveryOptions(APIView):
    def post(self, request):
        fias = request.data.get('fias')
        api_key = os.getenv("ZAO_SDT_API_KEY")

        if not fias:
            return Response({"detail": "Missing 'fias' parameter."}, status=status.HTTP_400_BAD_REQUEST)

        if not api_key:
            return Response({"detail": "API key is not configured."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        try:
            url = f'https://api-k2.zao-sdt.ru/{api_key}/delivery_city'
            params = {'fias': fias, 'payment_type': 2}
            response = requests.get(url, params=params, timeout=10)

            if response.status_code != 200:
                return Response(
                    {"detail": "Failed to retrieve delivery options.", "status_code": response.status_code},
                    status=status.HTTP_502_BAD_GATEWAY
                )

            result = response.json()

            if not result.get('data'):
                return Response({"detail": "No delivery data found."}, status=status.HTTP_404_NOT_FOUND)

            city_info = result['data'][0].copy()
            delivery_types = city_info.pop('delivery_types', {})

            # Группировка по (delivery_code, delivery_id)
            grouped = defaultdict(list)
            for item in delivery_types.values():
                key = (item["delivery_code"], item["delivery_id"], item["name"])
                grouped[key].append(item)

            # Преобразование в нужный формат
            grouped_list = [
                {
                    "delivery_code": key[0],
                    "delivery_id": key[1],
                    "delivery_name": key[2],
                    "min_cost": min(option["cost"] for option in options),
                    "options": options
                }
                for key, options in grouped.items()
            ]
            city_info['deliveries'] = grouped_list

            return Response( {"city_info":city_info}, status=status.HTTP_200_OK)

        except RequestException as e:
            return Response(
                {"detail": "Error communicating with delivery service.", "error": str(e)},
                status=status.HTTP_502_BAD_GATEWAY
            )
class GetFias(APIView):
    def post(self, request):
        token = os.getenv("DADATA_API_TOKEN")
        secret = os.getenv("DADATA_SECRET")
        dadata = Dadata(token, secret)
        query = request.data.get('query')
        result = dadata.suggest("address", query)


        result_list = [
            {
                "value": item.get("value"),
                "postal_code": item.get("data", {}).get("postal_code"),
                "fias_id": item.get("data", {}).get("fias_id")
            }
            for item in result
        ]
        return Response(result_list,status=200)