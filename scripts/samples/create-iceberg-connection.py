import dataiku

client = dataiku.api_client()

connection_name = "aws_iceberg_glue_conn"
connection_type = "Iceberg"

connection_params = {
    "catalogType": "Glue",             # Options: 'Glue', 'REST', etc.
    "glueId": "123456789012",          # Your AWS Account ID
    "warehouse": "s3://my-iceberg-warehouse-bucket/path",
    "region": "us-east-1",             # Your AWS Region
    "authType": "default"              # Or explicit AWS keys/profile if needed
}

new_connection = client.create_connection(
    name=connection_name,
    type=connection_type,
    params=connection_params,
    usable_by="ALL"                    # Or use 'ALLOWED' with 'allowed_groups'
)

print(f"Successfully created Iceberg connection: {connection_name}")
