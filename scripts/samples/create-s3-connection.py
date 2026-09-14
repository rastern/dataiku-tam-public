import dataiku

client = dataiku.api_client()

s3_params = {
    "credentialsMode": "KEY_PAIR", # Options: KEY_PAIR, INSTANCE_PROFILE, ASSUME_ROLE, etc.
    "accessKey": "YOUR_AWS_ACCESS_KEY",
    "secretKey": "YOUR_AWS_SECRET_KEY",
    "chroot": "/my-default-folder", # Optional: Root path inside the bucket
    "defaultBucket": "my-target-s3-bucket", # Optional: Default bucket for this connection
    "encryptionMode": "NONE"
}

new_connection = client.create_connection(
    name="my_new_s3_connection",
    type="S3",
    params=s3_params,
    usable_by="ALLOWED", # Options: 'ALL' or 'ALLOWED'
    allowed_groups=["data_team_group"] # If usable_by='ALLOWED', specify the target DSS groups
)

print("S3 connection created successfully!")
