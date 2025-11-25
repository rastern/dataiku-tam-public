import dataiku


# Use the public API client (preferred)
client = dataiku.api_client()


# List all project IDs
projects = client.list_projects()

for p in projects:
    print(p["projectKey"])
