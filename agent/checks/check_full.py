import subprocess
import json
from utils import print_output

scripts = [
    "check_quick.py",
    "check_resources.py",
    "check_security.py",
    "check_logs.py",
    "check_network.py",
    "check_services.py",
]

results = {}

for script in scripts:
    result = subprocess.run(
        ['python3', script, '--json'], capture_output=True, text=True)
    try:
        results[script.replace('.py', '')] = json.loads(result.stdout)
    except json.JSONDecodeError:
        results[script.replace('.py', '')] = {
            "error": result.stderr.strip() or "Скрипт не выполнен"
        }

data = {"full_report": results}

print_output(data)
