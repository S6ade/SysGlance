import psutil
from utils import print_output

# CPU
cpu_load = psutil.cpu_percent(interval=1)
cpu_count = psutil.cpu_count()

top_cpu = []
for proc in psutil.process_iter(['name', 'cpu_percent']):
    top_cpu.append({
        "name": proc.name(),
        "pid": proc.pid,
        "cpu_percent": proc.info['cpu_percent']
    })
top_cpu.sort(key=lambda x: x['cpu_percent'], reverse=True)
top_cpu = top_cpu[:5]

# RAM
ram = psutil.virtual_memory()

top_ram = []
for proc in psutil.process_iter(['name', 'memory_percent']):
    top_ram.append({
        "name": proc.name(),
        "pid": proc.pid,
        "memory_percent": proc.info['memory_percent']
    })
top_ram.sort(key=lambda x: x['memory_percent'], reverse=True)
top_ram = top_ram[:5]

# Диски
disks_list = []
for partition in psutil.disk_partitions():
    try:
        usage = psutil.disk_usage(partition.mountpoint)
        disks_list.append({
            "device": partition.device,
            "mountpoint": partition.mountpoint,
            "total_gb": round(usage.total / (1024**3), 2),
            "used_gb": round(usage.used / (1024**3), 2),
            "percent": usage.percent
        })
    except PermissionError:
        continue

# Собираем словарь
data = {
    "cpu": {
        "percent": cpu_load,
        "cores": cpu_count,
        "top_processes": top_cpu
    },
    "ram": {
        "total_gb": round(ram.total / (1024**3), 2),
        "used_gb": round(ram.used / (1024**3), 2),
        "percent": ram.percent,
        "top_processes": top_ram
    },
    "disks": disks_list
}

print_output(data)
