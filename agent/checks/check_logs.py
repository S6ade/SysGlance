import subprocess
from utils import print_output

# Ошибки journalctl
journal_data = []
journal_result = subprocess.run(
    ['journalctl', '-p', '3'], capture_output=True, text=True)

for line in journal_result.stdout.splitlines():
    if 'error' in line.lower():
        journal_data.append(line.strip())
        if len(journal_data) >= 20:
            break

# Ошибки syslog
syslog_data = []
syslog_result = subprocess.run(
    ['grep', '-iE', 'error|fail|critical', '/var/log/syslog'],
    capture_output=True, text=True)

for line in syslog_result.stdout.splitlines()[-20:]:
    syslog_data.append(line.strip())

# OOM-убийства
oom_data = []
oom_result = subprocess.run(
    ['journalctl', '-k'], capture_output=True, text=True)

for line in oom_result.stdout.splitlines():
    if 'oom' in line.lower():
        oom_data.append(line.strip())

# Ошибки ядра
kernel_data = []
kernel_result = subprocess.run(
    ['dmesg', '-l'], capture_output=True, text=True)

for line in kernel_result.stdout.splitlines():
    if 'error' in line.lower():
        kernel_data.append(line.strip())

# Собираем словарь
data = {
    "journalctl_errors": {
        "count": len(journal_data),
        "lines": journal_data
    },
    "syslog_errors": {
        "count": len(syslog_data),
        "lines": syslog_data
    },
    "oom_kills": {
        "count": len(oom_data),
        "lines": oom_data
    },
    "kernel_errors": {
        "count": len(kernel_data),
        "lines": kernel_data
    }
}

print_output(data)
