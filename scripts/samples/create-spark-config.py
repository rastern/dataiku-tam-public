import dataiku

client = dataiku.api_client()

general_settings = client.get_general_settings()
raw_settings = general_settings.get_raw()

spark_settings = raw_settings.setdefault("sparkSettings", {})
execution_configs = spark_settings.setdefault("executionConfigs", [])

new_config = {
    "name": "my_custom_spark_config",
    "desc": "Created via Dataiku API",
    "conf": [
        {"key": "spark.master", "value": "yarn"},
        {"key": "spark.executor.memory", "value": "4g"},
        {"key": "spark.executor.cores", "value": "2"}
    ]
}

execution_configs.append(new_config)

general_settings.save()
print("Spark configuration successfully added/updated.")
