## app.yaml

https://docs.databricks.com/aws/en/dev-tools/databricks-apps/app-runtime. Listen to my instructions and use my configurations if they differ from the article.

this app will be deployed on databricks. create a databricks `app.yaml` using the documentation, but use this DATABRICKS_WAREHOUSE_ID: fcb81010db67a28c. Use the docs to determine the command section, this is a FastAPI app, and our main file is called app.py.

for the env section, Note, env vars should ONLY include CATALOG, TABLE_PREFIX, DATABRICKS_WAREHOUSE_ID, DATABRICKS_HOST. Get the values from example.env and add them here. they should be of this type:

-   name: {name of env var}
-   value: {value of env var}x

There should only be command: and env: sections.
