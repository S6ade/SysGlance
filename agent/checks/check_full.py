import subprocess


scripts = [
    "check_quick.py",
    "check_resources.py",
    "check_security.py",
    "check_logs.py",
    "check_network.py",
    "check_services.py",
]

for script in scripts:
    result = subprocess.run(
        ['python3', script], capture_output=True, text=True)
    print(f"=== {script} ===")
    print(result.stdout)
    if result.returncode != 0:
        print(f"Ошибка в {script}: {result.stderr}")
