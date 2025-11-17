import json

from lexloop import main

openapi_schema = json.dumps(main.app.openapi(), indent=2)
with open("openapi.json", "w") as f:
    f.write(openapi_schema)