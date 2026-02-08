import os

import stripe

stripe.api_key = os.getenv("STRIPE_SECRET_KEY")


def create_stripe_price(amount):
    """Create amount for stripe"""
    return stripe.Price.create(
        currency="rub",
        unit_amount=amount * 100,
        product_data={
            "name": "lesson",
        },
    )


def create_stripe_sessions(price):
    """Create session for stripe"""
    session = stripe.checkout.Session.create(
        success_url="https://stripe.com/checkout",
        line_items=[{"price": price.get("id"), "quantity": 1}],
        mode="payment",
    )
    return session.get("id"), session.get("url")
