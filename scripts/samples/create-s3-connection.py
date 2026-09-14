import dataikuapi

host = "https://your-dataiku-instance.com"
api_key = "your_admin_api_key"
client = dataikuapi.DSSClient(host, api_key)

s3_params = {
    "credentialsMode": "KEYS", # Options: KEYS, ASSUME_ROLE, INSTANCE_PROFILE, etc.
    "accessKey": "YOUR_AWS_ACCESS_KEY",
    "secretKey": "YOUR_AWS_SECRET_KEY",
    "defaultBucket": "your-default-bucket-name",
    "chroot": "/optional/path/restriction", # Leave blank or omit for free selection mode
    "metastoreSynchronizationMode": "NONE"
}

new_connection = client.create_connection(
    name="my_s3_api_connection",
    type="S3",
    params=s3_params,
    usable_by="ALL"  # Use 'ALLOWED' if restricting access to specific groups
)

print("S3 connection created successfully!")
