import dataiku
from dataiku import pandasutils as pdu
import pandas as pd


# Use the public API client (preferred)
client = dataiku.api_client()


# List all project IDs if necessary, else skip this section
# projects = client.list_projects()
#
# for p in projects:
#     print(p["projectKey"])


project = client.get_project("DKU_TUT_APIS_1")

# if you want to set a *project level* code environment, do so here
#project.set_python_code_env('code_env_name')

recipes = project.list_recipes(as_type='objects')

for r in recipes:
    settings = r.get_settings()
    
    if settings.type != 'python':
        continue
    
    print(f"Updating code env for {r.name} in {r.project_key}")
    
    # use ONE of:
    #settings.set_code_env('code_env_name') # set code env to named environment
    #settings.set_code_env(inherit=True) # set code env to use project's default code environment
