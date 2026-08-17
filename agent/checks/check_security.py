import subprocess
import psutil
from utils import print_output

# UFW статус
ufw_status = subprocess.run(
    ["sudo", "ufw", "status"], capture_output=True, text=True)
ufw_active = "Status: active" in ufw_status.stdout

# Открытые порты
open_ports = []
for port in psutil.net_connections(kind='inet'):
    if port.status == 'LISTEN':
        open_ports.append({
            "port": port.laddr.port,
            "pid": port.pid
        })

# SSH-попытки
auth_log = subprocess.run(
    ['sudo', 'cat', '/var/log/auth.log'], capture_output=True, text=True)

ssh_data = {
    "accepted": 0,
    "failed": 0,
    "top_failed_ips": []
}

if "Permission denied" not in auth_log.stderr and auth_log.returncode == 0:
    ip_count = {}
    for line in auth_log.stdout.splitlines():
        if 'Accepted' in line:
            ssh_data['accepted'] += 1
        elif 'Failed password' in line:
            ssh_data['failed'] += 1
            parts = line.split('from')
            if len(parts) > 1:
                ip = parts[1].strip().split()[0]
                ip_count[ip] = ip_count.get(ip, 0) + 1

    ssh_data['top_failed_ips'] = sorted(
        ip_count.items(), key=lambda x: x[1], reverse=True)[:5]
else:
    ssh_data['error'] = "Нет доступа к /var/log/auth.log"

# Собираем словарь
data = {
    "ufw": {
        "active": ufw_active
    },
    "open_ports": open_ports,
    "ssh": ssh_data
}

print_output(data)
