# GDG Secret Manager Workshop

Demo materials for the workshop:

**Build with AI: Secure Your Agents with Google Secret Manager**

## Contents

- `secret-manager-demo/` — local Python examples for creating, versioning, and reading secrets
- `secret-manager-run-demo/` — serverless runtime example showing how a cloud function accesses a secret at runtime

## Notes

- Demo values only
- No real credentials included

## 1. Setup project

gcloud config set project <PROJECT_ID>

export PROJECT_ID=$(gcloud config get-value project)
export REGION=europe-west1

echo $PROJECT_ID
echo $REGION

## 2. Enable Secret Manager API

gcloud services enable secretmanager.googleapis.com

## 3. Install Python client

pip3 install --user google-cloud-secret-manager==2.10.0

## 5. Create secret (v1)

python3 create_secret.py

## 6. Read secret

python3 access_secret.py

## 9. Enable Cloud Functions

gcloud services enable cloudfunctions.googleapis.com cloudbuild.googleapis.com

## 11. Create service account

export PROJECT_ID=$(gcloud config get-value project)
export REGION=europe-west1
export SA_NAME=secret-demo-sa

gcloud iam service-accounts create $SA_NAME \
  --display-name="Secret demo runtime service account"

## 12. Grant access to secret

gcloud secrets add-iam-policy-binding workshop-demo-secret \
  --role="roles/secretmanager.secretAccessor" \
  --member="serviceAccount:${SA_NAME}@${PROJECT_ID}.iam.gserviceaccount.com"


## 13. Deploy function

gcloud functions deploy agent_runtime_check \
  --gen2 \
  --region=$REGION \
  --runtime=python312 \
  --source=. \
  --entry-point=agent_runtime_check \
  --trigger-http \
  --allow-unauthenticated \
  --service-account=${SA_NAME}@${PROJECT_ID}.iam.gserviceaccount.com \
  --set-env-vars=PROJECT_ID=${PROJECT_ID},SECRET_ID=workshop-demo-secret


## 14. Check env vars

gcloud functions describe agent_runtime_check \
  --gen2 \
  --region=europe-west1 \
  --format="yaml(serviceConfig.environmentVariables)"


## 15. Test function

curl https://<YOUR_FUNCTION_URL>
