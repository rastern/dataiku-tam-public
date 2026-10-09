import json
import dataiku

client = dataiku.api_client()
config = client.get_general_settings().settings

# get container settings
container_config = config['containerSettings']

print(container_config)

# make changes


# save
config.save()
