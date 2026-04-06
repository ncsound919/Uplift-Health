import os

import stripe
from fastapi import APIRouter, HTTPException, Request


router = APIRouter()

stripe.api_key = os.getenv("STRIPE_SECRET_KEY", "")
WEBHOOK_SECRET = os.getenv("STRIPE_WEBHOOK_SECRET", "")


@router.post("/stripe/webhook")
async def stripe_webhook(request: Request):
    payload = await request.body()
    sig_header = request.headers.get("stripe-signature")

    try:
        # Verify webhook signature following Stripe docs and FastAPI examples.[web:22][web:25][web:29][web:26]
        event = stripe.Webhook.construct_event(
            payload=payload,
            sig_header=sig_header,
            secret=WEBHOOK_SECRET,
        )
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid payload")
    except stripe.error.SignatureVerificationError:
        raise HTTPException(status_code=400, detail="Invalid signature")

    event_type = event["type"]

    if event_type == "checkout.session.completed":
        session = event["data"]["object"]
        # TODO: mark premium access in your DB; send confirmation email, etc.
        print("Payment successful for session", session.get("id"))

    return {"status": "success"}
