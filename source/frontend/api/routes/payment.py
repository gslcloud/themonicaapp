import stripe
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, ValidationError

router = APIRouter()

stripe.api_key = "your-api-key"

class CreatePaymentIntentRequest(BaseModel):
    amount: int
    currency: str

@router.post("/create-payment-intent")
def create_payment_intent(request: CreatePaymentIntentRequest):
    try:
        intent = stripe.PaymentIntent.create(
            amount=request.amount,
            currency=request.currency
        )
        return {"client_secret": intent.client_secret}
    except ValidationError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except stripe.error.StripeError as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/process-payment")
def process_payment(request: dict):
    try:
        intent = stripe.PaymentIntent.retrieve(request.get("payment_intent_id"))
        intent.confirm()
        return {"status": intent.status}
    except stripe.error.StripeError as e:
        raise HTTPException(status_code=500, detail=str(e))