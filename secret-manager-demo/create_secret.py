import os
from google.cloud import secretmanager
from google.api_core.exceptions import AlreadyExists

PROJECT_ID = os.environ["PROJECT_ID"]
SECRET_ID = "workshop-demo-secret"


def create_secret(secret_id: str) -> None:
    client = secretmanager.SecretManagerServiceClient()
    parent = f"projects/{PROJECT_ID}"

    secret = {
        "replication": {
            "automatic": {}
        }
    }

    try:
        response = client.create_secret(
            request={
                "parent": parent,
                "secret_id": secret_id,
                "secret": secret,
            }
        )
        print(f"Created secret: {response.name}")
    except AlreadyExists:
        print(f"Secret already exists: {secret_id}")


def add_secret_version(secret_id: str, payload: str) -> None:
    client = secretmanager.SecretManagerServiceClient()
    parent = f"projects/{PROJECT_ID}/secrets/{secret_id}"

    response = client.add_secret_version(
        request={
            "parent": parent,
            "payload": {
                "data": payload.encode("utf-8")
            },
        }
    )
    print(f"Added secret version: {response.name}")


if __name__ == "__main__":
    create_secret(SECRET_ID)
    add_secret_version(SECRET_ID, "demo-value-v1")
    #add_secret_version(SECRET_ID, "demo-value-v2")
