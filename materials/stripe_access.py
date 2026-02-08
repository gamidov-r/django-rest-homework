import os

import stripe

stripe.api_key = os.getenv("STRIPE_API_KEY")


def create_one_time_purchase_session(product_name, unit_amount, currency, success_url, cancel_url):
    try:
        checkout_session = stripe.checkout.Session.create(
            line_items=[
                {
                    "price_data": {
                        "currency": currency,
                        "unit_amount": unit_amount,
                        "product_data": {
                            "name": product_name,
                        },
                    },
                    "quantity": 1,
                }
            ],
            mode="payment",
            success_url=success_url + "?session_id={CHECKOUT_SESSION_ID}",
            cancel_url=cancel_url,
        )
        return checkout_session.url

    except stripe.error.StripeError as e:
        return {"url": "https://example.com/cancel"}
        return None


def get_url():
    if not stripe.api_key:
        raise Exception("api key not configured")
    else:
        payment_url = create_one_time_purchase_session(
            product_name="Lesson",
            unit_amount=200000,
            currency="rub",
            success_url="https://example.com/success",
            cancel_url="https://example.com/cancel",
        )

        if payment_url:
            return {"url": payment_url}
        else:
            return {"url": "https://example.com/cancel"}
