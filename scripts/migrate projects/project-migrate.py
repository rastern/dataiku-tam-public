import os
import time
import random
import dataiku
import boto3
from datetime import datetime
from dataikuapi.dss.future import DSSFuture
import sys

# ─── CONFIGURATION ─────────────────────────────────────────────────────────────
# Source (Dev) DESIGN NODE
DEV_DSS_HOST    = "https://host:port"
DEV_DSS_API_KEY = "xxx"

# Prod DESIGN NODE
PROD_DSS_HOST    = "https://host:port"
PROD_DSS_API_KEY = "xxx"

AWS_REGION      = "us-east-1"
AWS_ACCESS_KEY  = "xxx"
AWS_SECRET_KEY  = "xxx"
S3_BUCKET       = "s3-bucket-name"

dev_client = DSSClient(DEV_DSS_HOST, DEV_DSS_API_KEY)

PROJECT_KEYS = [
    "DKU_TSHIRTS"
]

export_options = {
    "exportUploads":               True,
    "exportManagedFS":             False,
    "exportAnalysisModels":        True,
    "exportSavedModels":           True,
    "exportManagedFolders":        False,
    "exportAllInputDatasets":      False,
    "exportAllDatasets":           False,
    "exportAllInputManagedFolders":False,
    "exportGitRepository":         True,
    "exportInsightsData":          False
}

# ─── RETRY SETTINGS ────────────────────────────────────────────────────────────
MAX_RETRIES     = 5
INITIAL_DELAY   = 1     # in seconds
BACKOFF_FACTOR  = 2
MAX_DELAY       = 30
JITTER_FACTOR   = 0.1

# ─── CLIENTS ───────────────────────────────────────────────────────────────────
dev_client = dataiku.api_client()
s3 = boto3.client(
    "s3",
    region_name=AWS_REGION,
    aws_access_key_id=AWS_ACCESS_KEY,
    aws_secret_access_key=AWS_SECRET_KEY
)

# ─── RETRY WRAPPER ─────────────────────────────────────────────────────────────
def with_retries(fn, *args, **kwargs):
    last_exc = None
    for attempt in range(1, MAX_RETRIES + 1):
        try:
            return fn(*args, **kwargs)
        except Exception as e:
            last_exc = e
            if attempt == MAX_RETRIES:
                raise
            delay = min(INITIAL_DELAY * (BACKOFF ** (attempt - 1)), MAX_DELAY)
            delay += random.uniform(-JITTER * delay, JITTER * delay)
            print(f"[!] Attempt {attempt} failed: {e} — retrying in {delay:.1f}s")
            time.sleep(delay)
    raise last_exc

# ─── EXPORT LOGIC ───────────────────────────────────────────────────────────────
def export_project_to_zip(project_key: str, local_zip: str):
    proj = dev_client.get_project(project_key)
    stream = proj.get_export_stream(EXPORT_OPTIONS)
    try:
        with open(local_zip, "wb") as out_f:
            while True:
                chunk = stream.read(4 * 1024 * 1024)
                if not chunk:
                    break
                out_f.write(chunk)
    finally:
        try:
            stream.close()
        except Exception:
            pass

# ─── S3 UPLOAD (ATOMIC OVERWRITE + OPTIONAL HISTORY) ───────────────────────────
def upload_overwrite_atomic(local_zip: str, bucket: str, final_key: str):
    """
    Upload to a temporary key, then promote via server-side copy to the final key.
    This prevents any reader from ever fetching a partially uploaded object.
    """
    tmp_key = f"{final_key}.uploading"
    # 1) Upload to temp key
    s3.upload_file(
        local_zip,
        bucket,
        tmp_key,
        ExtraArgs={"ContentType": "application/zip"}
    )
    # 2) Promote atomically
    s3.copy_object(
        Bucket=bucket,
        CopySource={"Bucket": bucket, "Key": tmp_key},
        Key=final_key,
        MetadataDirective="COPY"
    )
    # 3) Clean temp key
    s3.delete_object(Bucket=bucket, Key=tmp_key)

def upload_history_copy(local_zip: str, bucket: str, history_key: str):
    s3.upload_file(
        local_zip,
        bucket,
        history_key,
        ExtraArgs={"ContentType": "application/zip"}
    )

# ─── ORCHESTRATION ─────────────────────────────────────────────────────────────
def export_and_upload(project_key: str, keep_history: bool = True) -> bool:
    print("\n" + "=" * 60)
    print(f"EXPORTING PROJECT: {project_key}")
    print("=" * 60)

    ts = datetime.utcnow().strftime("%Y%m%dT%H%M%SZ")
    local_zip   = f"/tmp/{project_key}-{ts}.zip"

    # Stable "latest" artifact → will be overwritten each run
    final_key   = f"{S3_PREFIX}/{project_key}/{project_key}.zip"

    # Optional history copy for traceability
    history_key = f"{S3_PREFIX}/{project_key}/history/{project_key}-{ts}.zip"

    try:
        print(f"[→] Exporting {project_key} to local file {local_zip}")
        with_retries(export_project_to_zip, project_key, local_zip)
        print(f"[✓] Export complete")

        print(f"[→] Uploading atomically to s3://{S3_BUCKET}/{final_key} (will overwrite)")
        with_retries(upload_overwrite_atomic, local_zip, S3_BUCKET, final_key)
        print(f"[✓] Final artifact uploaded")

        if keep_history:
            print(f"[→] Writing history copy s3://{S3_BUCKET}/{history_key}")
            with_retries(upload_history_copy, local_zip, S3_BUCKET, history_key)
            print(f"[✓] History copy uploaded")

        return True
    except (BotoCoreError, ClientError, Exception) as e:
        print(f"[✗] Error exporting/uploading {project_key}: {e}")
        return False
    finally:
        try:
            if os.path.exists(local_zip):
                os.remove(local_zip)
                print(f"[✓] Cleaned up local file {local_zip}")
        except Exception as ce:
            print(f"[!] Cleanup warning: {ce}")

# ─── MAIN ──────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    ok, nok = [], []
    for key in PROJECT_KEYS:
        (ok if export_and_upload(key, keep_history=True) else nok).append(key)

    print("\n" + "=" * 60)
    print("EXPORT TO S3 COMPLETE")
    print("=" * 60)
    print(f"Successful exports ({len(ok)}): {ok}")
    if nok:
        print(f"Failed exports     ({len(nok)}): {nok}")
    print("=" * 60)
