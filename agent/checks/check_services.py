import subprocess
from utils import print_output

# Упавшие systemd-сервисы
failed_services = []
failed_result = subprocess.run(
    ['systemctl', 'list-units', '--type=service', '--state=failed'],
    capture_output=True, text=True)

for line in failed_result.stdout.splitlines():
    if 'failed' in line.lower():
        failed_services.append(line.strip())

# Критичные сервисы
critical_services = ["nginx", "docker", "sshd", "postgresql", "cron", "ufw"]
services_status = []

for service in critical_services:
    result = subprocess.run(
        ['systemctl', 'is-active', service], capture_output=True, text=True)
    services_status.append({
        "name": service,
        "status": result.stdout.strip()
    })

# Docker-контейнеры
containers_list = []
containers_result = subprocess.run(
    ['docker', 'ps', '-a', '--format', '{{.Names}}\t{{.Status}}\t{{.Ports}}'],
    capture_output=True, text=True)

for line in containers_result.stdout.splitlines():
    name, status, ports = line.split('\t')
    containers_list.append({
        "name": name,
        "status": status,
        "ports": ports,
        "failed": 'Exited' in status or 'Restarting' in status
    })

# Собираем словарь
data = {
    "systemd": {
        "failed_services": failed_services,
        "critical_services": services_status
    },
    "docker": {
        "containers": containers_list
    }
}

print_output(data)
