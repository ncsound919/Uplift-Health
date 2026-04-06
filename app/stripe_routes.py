import os

import stripe
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel


router = APIRouter()

stripe.api_key = os.getenv("STRIPE_SECRET_KEY", "")
DOMAIN = os.getenv("DOMAIN", "http://localhost:8000")


class CheckoutRequest(BaseModel):
    product_id: str


# Very simple in-memory "products" example; replace with DB lookups in real use.
PRODUCTS = {
    "premium_program": {"name": "Premium Health Program", "amount": 9900},  # $99.00
}


@router.post("/create-checkout-session")
async def create_checkout_session(request: CheckoutRequest):
    if request.product_id not in PRODUCTS:
        raise HTTPException(status_code=400, detail="Invalid product")

    product = PRODUCTS[request.product_id]

    try:
        # Pattern based on common FastAPI + Stripe Checkout samples.[web:22][web:28][web:31]
        checkout_session = stripe.checkout.Session.create(
            payment_method_types=["card"],
            line_items=[
                {
                    "price_data": {
                        "currency": "usd",
                        "product_data": {"name": product["name"]},
                        "unit_amount": product["amount"],
                    },
                    "quantity": 1,
                }
            ],
            mode="payment",
            success_url=f"{DOMAIN}/success?session_id={{CHECKOUT_SESSION_ID}}",
            cancel_url=f"{DOMAIN}/cancel",
        )
        return {"checkout_url": checkout_session.url}
    except Exception as e:  # noqa: BLE001
        raise HTTPException(status_code=400, detail=str(e))
