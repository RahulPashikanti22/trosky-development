# Trosky Microservices Split

This repo contains a proposed split of your monolithic `src` into 5 Flask microservices:

- **auth-service**: signup, login, Stripe subscription
- **communication-service**: email, sms dispatch
- **content-service**: content generation related flows
- **journey-service**: student journey orchestration
- **master-service**: master data like templates

## Inter-service links

- `auth-service` -> `communication-service` to send welcome emails after signup.
- `content-service` -> `auth-service` to validate user tokens (stubbed).
- `journey-service` -> `communication-service` for notifications, and may validate users via `auth-service`.
- `master-service` is standalone but can be used by others to fetch templates.

Environment variables in `.env.sample` define base URLs so services can call each other (e.g., `COMM_SERVICE_URL`).

## Run locally

```bash
docker compose up --build
```

Then hit:

- http://localhost:8001/auth/health
- http://localhost:8002/comm/health
- http://localhost:8003/content/health
- http://localhost:8004/journey/health
- http://localhost:8005/master/health

## Porting your domain logic

Where you see `TODO` comments in each `app.py`, copy the code from your original modules:
- `src/modules/Authentication/Login.py` -> login logic
- `src/modules/Authentication/Signup.py` -> signup logic
- `src/modules/Authentication/Stripe.py` -> stripe helpers
- `src/modules/CommunicationModule/CommunicationEngine.py` -> email/SMS send logic
- `src/modules/ContenEngine/ContentEngine.py` & `ContentEngineLib.py` -> content generation
- `src/modules/Journey/StudentJourney.py` -> journey flow
- `src/modules/MasterScreens/Master.py` -> master templates

Refactor those functions into these services as needed.