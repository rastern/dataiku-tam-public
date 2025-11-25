from typing import Optional

import dataiku
from dataiku import pandasutils as pdu
import pandas as pd


# Map of code envs to update
CODE_ENV_MAP = {
    'py38': 'py311',
    'py39': 'py312'
}

PROJECT_ID = 'DKU_TUT_APIS_1'       # specify the project ID to update
UPDATE_PROJECT_ENV = False          # if True, update the project level ENV
INHERIT_PROJECT_ENV = False         # set all code recipes to inherit the project ENV
USE_STATIC_ENV = False              # use a static ENV mode, not the CODE_ENV_MAP
STATIC_NAME = None                  # static ENV name to use in static mode

# Use the public API client (preferred)
client = dataiku.api_client()
project = client.get_project(PROJECT_ID)


def resolve_env_name(cur: str, default=None: Optional[str]) -> str:
    default = cur if not default else default
    ret = None

    if USE_STATIC_ENV:
        ret = STATIC_NAME
    else:
        try:
            ret = CODE_ENV_MAP[cur]
        except KeyError:
            pass

    if ret is None:
        return default

    return ret


# if you want to set a *project level* code environment, do so here
if UPDATE_PROJECT_ENV:
    settings = project.get_settings()
    cur_env = settings.settings.get('settings',{}).get('codeEnvs',{}).get('python',{}).get('envName')
    new_env = resolve_env_name(cur_env)
    
    if new_env != cur_env:
        print(f"Updating project code env from [{cur_env}] => [{new_env}]")
        settings.set_python_code_env(new_env)
        settings.save()
    else:
        print('No update required, skipping')

recipes = project.list_recipes(as_type='objects')

for r in recipes:
    settings = r.get_settings()
    
    if settings.type != 'python':
        continue

    if INHERIT_PROJECT_ENV:
        print(f"Updating code env for recipe [{r.name}] to inherit project env")
        settings.set_code_env(inherit=True)
        settings.save()
    else:
        # Don't forget to set a default on resolve_env_name() if you want to override project level inheritance
        cur_env = settings.get_code_env_settings().get('envName')
        #new_env = resolve_env_name(cur_env, default='py312')
        new_env = resolve_env_name(cur_env)

        if new_env != cur_env:
            # if cur_env is None it was using INHERIT mode previously
            print(f"Updating code env for recipe [{r.name}] from [{cur_env}] => [{new_env}]")
            settings.set_code_env(code_env=new_env)
            settings.save()
        else:
            print(f"No update required or no mapping found, skipping [{r.name}]")
