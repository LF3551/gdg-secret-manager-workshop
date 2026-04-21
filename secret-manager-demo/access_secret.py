import os
import hashlib
from google.cloud import secretmanager
from google.api_core.exceptions import NotFound

PROJECT_ID = os.getenv("PROJECT_ID")

if not PROJECT_ID:
    raise RuntimeError(
        "PROJECT_ID is not set. Run: export PROJECT_ID=$(gcloud config get-value project)"
    )

SECRET_ID = "workshop-demo-secret"


def access_secret_version(secret_id: str, version_id: str = "latest") -> str:
    client = secretmanager.SecretManagerServiceClient()
    name = f"projects/{PROJECT_ID}/secrets/{secret_id}/versions/{version_id}"
    response = client.access_secret_version(request={"name": name})
    return response.payload.data.decode("utf-8")


def secret_hash(secret_value: str) -> str:
    return hashlib.sha256(secret_value.encode("utf-8")).hexdigest()


def print_secret_hash(label: str, version_id: str) -> None:
    try:
        value = access_secret_version(SECRET_ID, version_id)
        print(f"{label}: {secret_hash(value)}")
    except NotFound:
        print(f"{label}: version {version_id} not found yet")


if __name__ == "__main__":
    print_secret_hash("latest", "latest")
    print_secret_hash("v1", "1")
    print_secret_hash("v2", "2")

    # print("v1 raw:    ", access_secret_version(SECRET_ID, "1"))
    # print("v2 raw:    ", access_secret_version(SECRET_ID, "2"))
    print("v3 raw:    ", access_secret_version(SECRET_ID, "3"))
