import dataiku


dss_client = dataiku.api_client()
users = dss_client.list_users(as_objects=True)
dry_run = False

profiles_to_migrate = {
    "DESIGNER": "FULL_DESIGNER",
    "PLATFORM_ADMIN": "TECHNICAL_ACCOUNT",
    "VISUAL_DESIGNER" : "DATA_DESIGNER",
    "READER" : "AI_CONSUMER",
    "EXPLORER": "GOVERNANCE_MANAGER"
}


for user in users:
    settings = user.get_settings()
    properties = settings.get_raw()
    profile = properties["userProfile"]
    
    if profile in profiles_to_migrate:
        print(f"Migrate {properties['login']} from {profile} to {profiles_to_migrate[profile]}")
        
        if not dry_run:
            properties["userProfile"] = profiles_to_migrate[profile]
            settings.save()
