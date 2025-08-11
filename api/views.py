from django.shortcuts import render, get_object_or_404
from django.views import View
from django.http import JsonResponse
from django.conf import settings
import stripe
from .models import Item, Order

stripe.api_key = settings.STRIPE_SECRET_KEY

class ItemDetailView(View):
    def get(self, request, id):
        item = get_object_or_404(Item, id=id)
        return render(request, 'item.html', {
            'item': item
        })

class ItemPaymentPageView(View):
    def get(self, request, id):
        item = get_object_or_404(Item, id=id)
        return render(request, 'item_payment.html', {'item': item, 'stripe_public_key': settings.STRIPE_PUBLIC_KEY})

class CreateItemPaymentIntentView(View):
    def post(self, request, id):
        item = get_object_or_404(Item, id=id)
        try:
            intent = stripe.PaymentIntent.create(
                amount=int(item.price * 100),
                currency=item.currency.lower(),
                automatic_payment_methods={"enabled": True}
            )
            return JsonResponse({"clientSecret": intent.client_secret})
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)

class OrderDetailView(View):
    def get(self, request, id):
        order = get_object_or_404(Order, id=id)
        items = order.items.all()
        total = sum([item.price for item in items])
        return render(request, 'order.html', {
            'order': order,
            'items': items,
            'total': total,
        })

class OrderPaymentPageView(View):
    def get(self, request, id):
        order = get_object_or_404(Order, id=id)
        items = order.items.all()
        total_amount = sum([item.price for item in items])
        currencies = set(item.currency.lower() for item in items)
        if len(currencies) > 1:
            return JsonResponse({'error': 'Products have different currencies'}, status=400)
        else:
            currency = currencies.pop()

        base_amount_cents = int(total_amount * 100)
        tax_amount_cents = 0
        discount_amount_cents = 0

        try:
            coupon = stripe.Coupon.retrieve(order.discount.stripe_promotion_code_id)
            if coupon.percent_off:
                discount_amount_cents = int(base_amount_cents * (coupon.percent_off / 100))
            elif coupon.amount_off:
                discount_amount_cents = int(coupon.amount_off)
        except Exception:
            discount_amount_cents = 0

        base_minus_discount_cents = base_amount_cents - discount_amount_cents
        if base_minus_discount_cents < 0:
            base_minus_discount_cents = 0

        try:
            tax_rate = stripe.TaxRate.retrieve(order.tax.stripe_tax_rate_id)
            tax_percent = tax_rate.percentage or 0
            tax_amount_cents = int(base_minus_discount_cents * (tax_percent / 100))
        except Exception:
            tax_amount_cents = 0

        final_amount_cents = base_minus_discount_cents + tax_amount_cents
        final_amount = final_amount_cents / 100

        return render(request, 'order_payment.html', {
            'order': order,
            'amount': final_amount,
            'currency': currency,
            'stripe_public_key': settings.STRIPE_PUBLIC_KEY,
        })

class CreateOrderPaymentIntentView(View):
    def post(self, request, id):
        order = get_object_or_404(Order, id=id)
        items = order.items.all()
        total_amount = sum([item.price for item in items])
        currencies = set(item.currency.lower() for item in items)

        if len(currencies) > 1:
            return JsonResponse({'error': 'Products have different currencies'}, status=400)
        else:
            currency = currencies.pop()

        base_amount_cents = int(total_amount * 100)
        tax_amount_cents = 0
        discount_amount_cents = 0

        try:
            coupon = stripe.Coupon.retrieve(order.discount.stripe_promotion_code_id)
            if coupon.percent_off:
                discount_amount_cents = int(base_amount_cents * (coupon.percent_off / 100))
            elif coupon.amount_off:
                discount_amount_cents = int(coupon.amount_off)
        except Exception:
            discount_amount_cents = 0

        base_minus_discount_cents = base_amount_cents - discount_amount_cents
        if base_minus_discount_cents < 0:
            base_minus_discount_cents = 0

        try:
            tax_rate = stripe.TaxRate.retrieve(order.tax.stripe_tax_rate_id)
            tax_percent = tax_rate.percentage or 0
            tax_amount_cents = int(base_minus_discount_cents * (tax_percent / 100))
        except Exception:
            tax_amount_cents = 0

        final_amount_cents = base_minus_discount_cents + tax_amount_cents

        try:
            intent = stripe.PaymentIntent.create(
                amount=final_amount_cents,
                currency=currency,
                automatic_payment_methods={"enabled": True},
            )
            return JsonResponse({"clientSecret": intent.client_secret})
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)
