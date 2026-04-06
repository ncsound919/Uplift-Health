# Ultimate Health Center

One-stop online health and wellness platform.

This repo is an early scaffold for:
- A FastAPI backend with:
  - A small open-source chat model (TinyLlama 1.1B Chat) for a health assistant endpoint.
  - Stripe Checkout + webhook endpoints for paid add-ons (e.g., premium programs, partner tools).
- Future front-end (React/Next.js or similar) that talks to this API.

## Stack
- Python 3.11+
- FastAPI + Uvicorn
- Stripe Python SDK
- TinyLlama 1.1B Chat via `transformers` or `llama-cpp-python` (you can swap to another small open-source model).

## Getting started

1. Clone the repo:
   ```bash
   git clone https://github.com/ncsound919/ultimate-health-center.git
   cd ultimate-health-center
   ```

2. Create and activate a virtualenv (optional but recommended).

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Copy `.env.example` to `.env` and fill in:
   - `STRIPE_SECRET_KEY`
   - `STRIPE_WEBHOOK_SECRET`
   - `DOMAIN` (e.g. http://localhost:8000)
   - `MODEL_BACKEND` ("transformers" or "llama_cpp")
   - `MODEL_NAME` (e.g. TinyLlama/TinyLlama-1.1B-Chat-v1.0)

5. Run the app:
   ```bash
   uvicorn app.main:app --reload
   ```

## API overview (initial)
- `POST /api/chat` — proxy to the local small open-source model for simple health/wellness Q&A.
- `POST /api/create-checkout-session` — create a Stripe Checkout session for a sample product.
- `POST /api/stripe/webhook` — receive Stripe webhooks.

From here you can add:
- User auth and profiles.
- Content, plans, and a professional directory.
- UI in a separate front-end app.
