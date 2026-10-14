import json
import sys
from pathlib import Path

from lexloop import main

default_out = Path(__file__).resolve().parent.parent / "openapi.json"
out_path = Path(sys.argv[1]) if len(sys.argv) > 1 else default_out

openapi_schema = json.dumps(main.app.openapi(), indent=2)
out_path.parent.mkdir(parents=True, exist_ok=True)
out_path.write_text(openapi_schema + "\n")
