import stripe
from django.conf import settings

stripe.api_key = settings.STRIPE_SECRET_KEY

'''Создание продукта'''

def create_stripe_product(course):
    return stripe.Product.create(
        name=course.title,
        description=course.description
    )

'''Создание цены'''

def create_stripe_price(product_id, amount):
    return stripe.Price.create(
        product=product_id,
        unit_amount=amount * 100,  # В КОПЕЙКАХ!
        currency="usd"
    )

'''Создание checkout-сессии'''

def create_checkout_session(price_id):
    session = stripe.checkout.Session.create(
        mode="payment",
        line_items=[
            {
                "price": price_id,
                "quantity": 1
            }
        ],
        success_url=settings.STRIPE_SUCCESS_URL,
        cancel_url=settings.STRIPE_CANCEL_URL,
    )
    return session
