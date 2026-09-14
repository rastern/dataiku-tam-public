import dataiku

client = dataiku.api_client()

# (optionally) fetch all connection names
#dss_connections = client.list_connections()

connection_handle = client.get_connection('your_connection_name')

connection_definition = connection_handle.get_definition()

print(connection_definition)
