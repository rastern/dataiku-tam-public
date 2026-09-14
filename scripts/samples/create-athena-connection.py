import dataiku

client = dataiku.api_client()

connection_name = "my_athena_connection"
connection_type = "Athena"

connection_params = {
    "s3Connection": "my_s3_connection_name",  # Name of your existing S3 connection
    "credentialMode": "S3",                   # Use credentials "From S3 connection"
    "database": "default",                    # Default Athena database name
    "region": "us-east-1",                    # AWS Region
    "s3StagingDirectory": "s3://your-athena-staging-bucket/path/" # S3 query results location
}

athena_conn = client.create_connection(
    name=connection_name,
    type=connection_type,
    params=connection_params,
    usable_by="ALL"
)

print(f"Successfully created Athena connection: {connection_name}")
