import subprocess

# Ищем и выводим количество упавших сервисов
failed_systemd = subprocess.run(['systemctl', 'list-units', '--type=service', '--state=failed'],capture_output=True, text=True)

error_count = 0

for err_line in failed_systemd.stdout.splitlines():
    if 'failed' in err_line.lower():
        error_count += 1
        print(f"Содержимое: {err_line.strip()}")

if error_count == 0:
    print("Нет упавших сервисов")
else:
    print(f"Количество упавших: {error_count}")


# Выводоим активные сервисы
active_service = ["nginx", "docker", "sshd", "postgresql", "cron", "ufw"]

for active in active_service:
    active_systemd = subprocess.run(
        ['systemctl', 'is-active', active], capture_output=True, text=True)
    print(f"{active}: {active_systemd.stdout.strip()}")


# Выводим инфу о контейнерах
containers_docker = subprocess.run(
    ['docker', 'ps', '-a', '--format', '{{.Names}}\t{{.Status}}\t{{.Ports}}'],
    capture_output=True, text=True)

for container_line in containers_docker.stdout.splitlines():
    name, status, ports = container_line.split('\t')
    print(f"Name: {name} | Status: {status} | Ports: {ports}")
    if 'Exited' in status or 'Restarting' in status:
        print(f"Упавший контейнер: {name} — {status}")
