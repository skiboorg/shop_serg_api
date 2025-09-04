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
        selected_address = data['selected_address']
        selected_delivery = data['selected_delivery']
        cart = get_cart(request)
        api_key = os.getenv("ZAO_SDT_API_KEY")

        items = []

        for item in cart.items.all():
            items.append({
                    "name":item.product.name,
                    "item_id":item.product.inner_id,
                    "quantity":item.amount,
                    "price":float(item.total_price)
                })


        order_data = {
            "order":
                {
                    "id":data['order_id'],
                    "delivery_sum":float(selected_delivery['cost']),
                    "payment_type":2,
                    "send_date":selected_delivery['delivery_date'],
                    "comment":data.get('comment'),
                    "weight":100,
                    "city_id":selected_address['fias_id'],
                    "place_id":selected_delivery['place_id'],
                    "index":selected_address['postal_code'],
                    "street":data['street'],
                    "building_1":data['building_1'],
                    "building_2":data['building_2'],
                    "room":data['room'],
                    "options":
                        {"partial_return":0,
                         "manual_confirm":False,
                         "delivery_asap":True
                         }
                },
            "customer":
                {
                    "firstname":data['firstname'],
                    "middlename":data.get('middlename'),
                    "lastname":data['lastname'],
                    "phone":f"+7{data['phone']}",
                    "email":data['email'],
                    "address":f"{selected_address['value']} {data['street']} {data['building_1']} {data['building_2']}"
                },
            "items":items
        }

        print(order_data)
        # ?check = 1
        url = f'https://api-k2.zao-sdt.ru/{api_key}/order'

        response = requests.put(url, json=order_data)
        if response.status_code == 200:
            response_json = response.json()
            print(response_json)
            if not response_json.get('success'):
                result = {'success': False, 'message': response_json}

        else:
            result = {'success': False, 'message': 'error'}



        new_order = Order.objects.create(
            order_id=data['order_id'],
            customer=f"{data['firstname']} {data.get('middlename')} {data['lastname']}",
            phone=f"+7{data['phone']}",
            email=data['email'],
            delivery_address=f"{selected_address['value']} {data['street']} {data['building_1']} {data['building_2']}",
            selected_delivery = f"{selected_delivery['name']}, стоимость доставки {selected_delivery['cost']} руб, дата {selected_delivery['delivery_date']}",
            comment=data.get('comment'),
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


        result = {'success': True, 'message': f'Заказ {new_order.id} создан'}
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