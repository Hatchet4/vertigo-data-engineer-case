# Vertigo Games – Part 1 API

# Overview
This repository contains the **Part 1 solution** for the Vertigo Games Data Engineer case.  
The goal was to design and deploy a **REST API** for managing clan-related data in a scalable and portable way using **FastAPI**, **PostgreSQL**, and **Docker**.

---

# Approach

1. API Framework
- Built with **FastAPI** for speed, type safety, and automatic OpenAPI documentation.
- Organized into modular structure:
  - `app/main.py` → entrypoint
  - `app/models.py` → SQLAlchemy models
  - `app/schemas.py` → Pydantic request/response schemas
  - `app/deps.py` → dependency injection for database sessions

2. Database
- **PostgreSQL** was used as the relational database.
- Schema defined in `schema.sql` (includes clans).
- UUIDs supported via `uuid-ossp` extension for unique identifiers.

3. Containerization
- A **Dockerfile** defines the API environment:
  - Python runtime
  - Installs dependencies (`requirements.txt`)
  - Copies application code
  - Runs Uvicorn server on port **8080** (required by Cloud Run)

4. Deployment
- Built and pushed Docker image with:
  ```bash
  gcloud builds submit --tag gcr.io/$PROJECT_ID/vertigo-clans-api:latest ./part1-api

  gcloud run deploy vertigo-clans-api \
  --image gcr.io/$PROJECT_ID/vertigo-clans-api:latest \
  --platform managed \
  --region europe-west1 \
  --allow-unauthenticated








# Commands used
- For build: gcloud builds submit --tag gcr.io/$PROJECT_ID/vertigo-clans-api:latest ./part1-api
- For deploy: gcloud run deploy vertigo-clans-api \
  --image gcr.io/winter-accord-469013-d5/vertigo-clans-api:latest \
  --platform managed \
  --region europe-west1 \
  --allow-unauthenticated \
  --add-cloudsql-instances winter-accord-469013-d5:europe-west1:vertigocase \
  --set-env-vars DATABASE_URL="postgresql+psycopg2://postgres:Vertigo_123@/casedata?host=/cloudsql/winter-accord-469013-d5:europe-west1:vertigocase" \
  --port 8080

# How to run
- The live URL:https://vertigo-clans-api-1061697115368.europe-west1.run.app/docs
- You can interact with get,post and delete methods in this url withouth needing to write URL requests e.g https://vertigo-clans-api-1061697115368.europe-west1.run.app/clans
- main.py contains all API entry points



