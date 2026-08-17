import psutil
import socket
import subprocess


print("\n=== Сетевые интерфейсы ===")
addrs_dict = psutil.net_if_addrs()


for interface_name, addresses in addrs_dict.items():
    print(f"Интерфейс: {interface_name}")
    for item in addresses:
        print(f"  Адрес: {item.address}, Семейство: {item.family}")


print("\n=== Открытые порты ===")
for port in psutil.net_connections(kind='inet'):
    if port.status == 'LISTEN':
        print(f"Port: {port.laddr.port} — PID: {port.pid}")


print("\n=== Активные соединения ===")
active_con_count = 0
active_con = psutil.net_connections(kind='inet')
remote_ip_count = {}
for established in active_con:
    if established.status == 'ESTABLISHED':
        active_con_count += 1
        print(
            f"Local: {established.laddr.ip}:{established.laddr.port} → Remote: {established.raddr.ip}:{established.raddr.port}")
        remote_ip = established.raddr.ip
        remote_ip_count[remote_ip] = remote_ip_count.get(remote_ip, 0) + 1
print(
    f"Топ-5 удаленных IP: {sorted(remote_ip_count.items(), key=lambda x: x[1], reverse=True)[:5]}")
print(f"Активных соединений: {active_con_count}")

print("\n=== DNS ===")
dns_socket = socket.getaddrinfo('google.com', 443, proto=socket.IPPROTO_TCP)
if dns_socket:
    print("DNS работает")
else:
    print("DNS не работает")

dns_server_count = 0
dns_server = subprocess.run(
    ['grep', '-iE', 'nameserver', '/etc/resolv.conf'], capture_output=True, text=True)

for dns_server_line in dns_server.stdout.splitlines():
    if 'nameserver' in dns_server_line.lower():
        dns_server_count += 1
        print(f"DNS-сервер {dns_server_count}: {dns_server_line.strip()}")
print(f"Количество: {dns_server_count}")
if dns_server_count == 0:
    print("Не найдено")

print("\n=== Основной шлюз ===")
gateway = subprocess.run(
    ["ip", "route", "show", "default"],
    capture_output=True,
    text=True
)
gateway_res = gateway.stdout.split()[2]
print(f"Основной шлюз: {gateway_res}")
