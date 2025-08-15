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



