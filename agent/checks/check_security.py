# Пороверка на безопастность сервера
#Подключаем модули
import subprocess
import psutil

# Выполняет проверку статуса UFW
status_ufw = subprocess.run(
    ["sudo", "ufw", "status"], capture_output=True, text=True)

if "Status: active" in status_ufw.stdout:
    print("Active")
else:
    print("Inactive")


# Выполняет какие порты слушаются
for port in psutil.net_connections(kind='inet'):
    if port.status == 'LISTEN':
        print(f"Port: {port.laddr.port} — PID: {port.pid}")


# Выполняем проверку на SSh-попытки
# Проверяем на права входа
# Выводим из логов Колличество "Удачных" и "Ошибочных входов"
# После извлекаем и строк 'Failed password' и считаем количество попыток и Топ 5 попыток
file_auth_log = subprocess.run(
    ['sudo', 'cat', '/var/log/auth.log'], capture_output=True, text=True)
if "Permission denied" in file_auth_log.stderr or file_auth_log.returncode != 0:
    print("У вас нету прав на чтение /var/log/auth.log")
else:
    count_accepted= 0
    count_failed= 0
    ip_count: dict[str, int] = {}
    for line in file_auth_log.stdout.splitlines():
        if 'Accepted' in line:
            count_accepted += 1
        elif 'Failed password' in line:
            count_failed += 1
            parts_failed = line.split('from')
            parts = parts_failed[1]
            remove_parts = parts.strip()
            split_parts = remove_parts.split()
            ip = split_parts[0]
            ip_count[ip] = ip_count.get(ip, 0) + 1
    print(f"Колличество Accepted: {count_accepted}")
    print(f"Колличество Failed: {count_failed}")
    print(f"Количество неудачных попыток: {sum(ip_count.values())}")
    print(
            f"Топ-5 IP с неудачными попытками: {sorted(ip_count.items(), key=lambda x: x[1], reverse=True)[:5]}")
