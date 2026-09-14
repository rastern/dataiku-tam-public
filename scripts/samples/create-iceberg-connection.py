import dataiku

client = dataiku.api_client()

iceberg_params = {
    "catalogType": "REST",                   # Options include: REST, GLUE, SNOWFLAKE, NESSIE, HIVE, HADOOP
    "catalogUri": "https://your-iceberg-catalog-uri/v1",
    "warehouse": "s3a://your-bucket/path/to/warehouse",
    
    # Example of nested authentication or storage properties if required by your setup
    "properties": [
        {"name": "header.X-Catalog-Auth", "value": "your-auth-token"}
    ]
}

new_connection = client.create_connection(
    name="my_iceberg_connection",
    type="Iceberg",
    params=iceberg_params,
    usable_by="ALL" # Can also be 'ALLOWED' if restricting to 'allowed_groups'
)

print("Iceberg connection created successfully!")
