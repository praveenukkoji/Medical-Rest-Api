from rest_framework.generics import GenericAPIView
from django.http import JsonResponse
from rest_framework.response import Response
import json

from order.models import Order, OrderMedicine
from medicine.models import Medicine, StoreMedicine
from store.models import Store
from user.models import User
from uuid import uuid4
from datetime import datetime
from medical import settings

import stripe

stripe.api_key = settings.STRIPE_SECRET_KEY


# add order
class AddOrderView(GenericAPIView):
    def post(self, requests):
        try:
            requests = json.load(requests)
            order_obj = requests.get("order")

            user_id = order_obj["user_id"]
            store_id = order_obj["store_id"]
            medicines = order_obj["medicines"]

            can_place_order = True
            total_amount = 0
            store = Store.objects.get(pk=store_id)
            for medicine_obj in medicines:
                medicine = Medicine.objects.get(pk=medicine_obj["medicine_id"])
                store_medicine = StoreMedicine.objects.get(store_id=store, medicine_id=medicine)
                if store_medicine.quantity >= medicine_obj["quantity"]:
                    total_amount += medicine_obj["quantity"] * store_medicine.price
                    continue
                can_place_order = False
                total_amount = 0
                break

            if can_place_order:

                order_id = uuid4()
                order_datetime = datetime.now()

                user = User.objects.get(pk=user_id)
                new_order = Order(order_id=order_id, user_id=user, store_id=store,
                                  order_datetime=order_datetime, total_amount=total_amount)
                new_order.save()

                order = Order.objects.get(pk=order_id)
                for medicine_obj in medicines:
                    medicine = Medicine.objects.get(pk=medicine_obj["medicine_id"])
                    store_medicine = StoreMedicine.objects.get(store_id=store, medicine_id=medicine)
                    new_quantity = store_medicine.quantity - medicine_obj["quantity"]

                    StoreMedicine.objects.filter(store_id=store, medicine_id=medicine).update(quantity=new_quantity)

                    new_order_medicine = OrderMedicine(order_id=order, medicine_id=medicine,
                                                       order_quantity=medicine_obj["quantity"])
                    new_order_medicine.save()

                total_amount = round(total_amount * 100)
                customer = stripe.Customer.create(email=user.user_email)
                intent = stripe.PaymentIntent.create(
                    amount=total_amount,
                    currency='inr',
                    customer=customer['id']
                )
                response = {
                    'clientSecret': intent['client_secret'],
                    'order_id': order.order_id
                }
            else:
                response = {
                    "message": "order failed"
                }
        except Exception as e:
            print(e)
            response = {"error": str(e)}
        return JsonResponse(response)


# order success
class OrderSuccessView(GenericAPIView):
    def post(self, requests):
        try:
            requests = json.load(requests)
            order_id = requests.get("order_id")
            Order.objects.filter(order_id=order_id).update(order_fulfilment_datetime=datetime.now(),
                                                           order_fulfilment_status="success")

            response = Response({
                "message": "payment done"
            })
        except Exception as e:
            print(e)
            response = Response(status=500)
        return response


# order cancel view
class OrderCancelView(GenericAPIView):
    def post(self, requests):
        try:
            requests = json.load(requests)

            order_id = requests.get("order_id")
            order = Order.objects.get(pk=order_id)
            store = Store.objects.get(pk=order.store_id.store_id)
            order_medicines = OrderMedicine.objects.filter(order_id=order)
            for order_medicine in order_medicines:
                medicine = Medicine.objects.get(pk=order_medicine.medicine_id.medicine_id)
                refill_quantity = order_medicine.order_quantity
                store_medicine = StoreMedicine.objects.get(store_id=store, medicine_id=medicine)
                available_quantity = store_medicine.quantity
                new_quantity = available_quantity + refill_quantity
                StoreMedicine.objects.filter(store_id=store, medicine_id=medicine).update(quantity=new_quantity)
            Order.objects.filter(order_id=order_id).update(order_fulfilment_datetime=datetime.now(),
                                                           order_fulfilment_status="cancelled")

            response = Response({
                "message": "order cancelled"
            })
        except Exception as e:
            print(e)
            response = Response(status=500)
        return response


# get order
class GetOrderView(GenericAPIView):
    def post(self, requests):
        try:
            requests = json.load(requests)
            orders = requests.get("orders")
            data = []
            for order_id in orders:
                order = Order.objects.get(pk=order_id)
                order_medicine = OrderMedicine.objects.get(order_id=order)
                data.append({
                    "order_id": order.order_id,
                    "user_id": order.user_id,
                    "store_id": order.store_id,
                    "order_datetime": order.order_datetime,
                    "order_fulfilment_datetime": order.order_fulfilment_datetime,
                    "order_fulfilment_status": order.order_fulfilment_status,
                    "total_amount": order.total_amount,
                    "medicines": [
                        {
                            "medicine_id": medicine.medicine_id,
                            "quantity": medicine.quantity
                        } for medicine in order_medicine
                    ]
                })
            response = {
                "data": data
            }
        except Exception as e:
            print(e)
            response = {"error": str(e)}
        return JsonResponse(response)
