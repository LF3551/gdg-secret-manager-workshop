import os
import hashlib

from google.cloud import secretmanager

SECRET_ID = os.getenv("SECRET_ID", "workshop-demo-secret")
_cached_secret_value = None


def get_project_id():
    return (
        os.getenv("GOOGLE_CLOUD_PROJECT")
        or os.getenv("GCP_PROJECT")
        or os.getenv("PROJECT_ID")
    )


def get_secret_value():
    global _cached_secret_value

    if _cached_secret_value is None:
        project_id = get_project_id()
        if not project_id:
            raise RuntimeError("Project ID is not available in the runtime environment")

        client = secretmanager.SecretManagerServiceClient()
        name = f"projects/{project_id}/secrets/{SECRET_ID}/versions/latest"
        response = client.access_secret_version(request={"name": name})
        _cached_secret_value = response.payload.data.decode("utf-8")

    return _cached_secret_value


def secret_hash(secret_value: str) -> str:
    return hashlib.sha256(secret_value.encode("utf-8")).hexdigest()


def agent_runtime_check(request):
    try:
        latest_secret_value = get_secret_value()

        credential_state = (
            "rotated credential loaded"
            if latest_secret_value.endswith("v2")
            else "initial credential loaded"
        )

        return (
            "Secure agent runtime is up.\n"
            f"Secret ID: {SECRET_ID}\n"
            f"Credential state: {credential_state}\n"
            f"Credential hash: {secret_hash(latest_secret_value)}\n"
        )
    except Exception as e:
        return f"Runtime error: {e}\n", 500
