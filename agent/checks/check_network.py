import psutil
import socket
import subprocess
from utils import print_output

# Сетевые интерфейсы
interfaces_list = []
for interface_name, addresses in psutil.net_if_addrs().items():
    interfaces_list.append({
        "name": interface_name,
        "addresses": [{"address": a.address, "family": str(a.family)} for a in addresses]
    })

# Открытые порты
open_ports_list = []
for port in psutil.net_connections(kind='inet'):
    if port.status == 'LISTEN':
        open_ports_list.append({
            "port": port.laddr.port,
            "pid": port.pid
        })

# Активные соединения
active_connections = []
remote_ip_count = {}
for conn in psutil.net_connections(kind='inet'):
    if conn.status == 'ESTABLISHED':
        active_connections.append({
            "local": f"{conn.laddr.ip}:{conn.laddr.port}",
            "remote": f"{conn.raddr.ip}:{conn.raddr.port}"
        })
        remote_ip = conn.raddr.ip
        remote_ip_count[remote_ip] = remote_ip_count.get(remote_ip, 0) + 1

top_remote_ips = sorted(
    remote_ip_count.items(), key=lambda x: x[1], reverse=True)[:5]

# DNS
dns_works = bool(socket.getaddrinfo(
    'google.com', 443, proto=socket.IPPROTO_TCP))

dns_servers = []
dns_result = subprocess.run(
    ['grep', '-iE', 'nameserver', '/etc/resolv.conf'],
    capture_output=True, text=True)
for line in dns_result.stdout.splitlines():
    if 'nameserver' in line.lower():
        dns_servers.append(line.split()[-1])

# Основной шлюз
gateway = ""
gateway_result = subprocess.run(
    ["ip", "route", "show", "default"], capture_output=True, text=True)
if gateway_result.stdout:
    gateway = gateway_result.stdout.split()[2]

# Собираем словарь
data = {
    "interfaces": interfaces_list,
    "open_ports": open_ports_list,
    "active_connections": {
        "count": len(active_connections),
        "top_remote_ips": top_remote_ips
    },
    "dns": {
        "works": dns_works,
        "servers": dns_servers
    },
    "gateway": gateway
}

print_output(data)
