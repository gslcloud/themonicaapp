from fastapi import APIRouter, HTTPException, Request
import stripe

router = APIRouter()

stripe.api_key = get_stripe_api_key()


@router.post("/payment")
async def initiate_payment(request: Request):
    try:
        payment_data = await request.json()

        if "amount" not in payment_data or "user_id" not in payment_data:
            raise HTTPException(status_code=400, detail="Invalid payment data. Amount and user ID are required.")

        amount = payment_data["amount"]
        user_id = payment_data["user_id"]

        if not isinstance(amount, int) or amount <= 0:
            raise HTTPException(status_code=400, detail="Invalid payment amount. Amount must be a positive integer.")
        
        if not isinstance(user_id, str) or len(user_id) == 0:
            raise HTTPException(status_code=400, detail="Invalid user ID. User ID must be a non-empty string.")

        session = stripe.checkout.Session.create(
            payment_method_types=["card"],
            line_items=[
                {
                    "price": "YOUR_PRICE_ID",
                    "quantity": 1
                }
            ],
            mode="payment",
            success_url="https://example.com/success",
            cancel_url="https://example.com/cancel"
        )

        return {"payment_url": session.url}

    except stripe.error.AuthenticationError:
        raise HTTPException(status_code=500, detail="Authentication with the payment gateway failed.")
    except stripe.error.APIConnectionError:
        raise HTTPException(status_code=500, detail="Could not connect to the payment gateway. Please try again later.")
    except stripe.error.InvalidRequestError:
        raise HTTPException(status_code=500, detail="Invalid request to the payment gateway. Please check your data.")
    except stripe.error.StripeError as e:
        raise HTTPException(status_code=500, detail=str(e))