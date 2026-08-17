import os
import psutil
import datetime
from utils import print_output

# Название ОС и имя хоста
os_name = os.uname().sysname
hostname = os.uname().nodename

# Время работы сервера
uptime = datetime.datetime.now() - datetime.datetime.fromtimestamp(psutil.boot_time())
uptime_str = str(uptime).split('.')[0]

# Средняя загрузка
load1, load5, load15 = os.getloadavg()

# CPU и RAM
cpu_usage = psutil.cpu_percent(interval=1)
ram_usage = psutil.virtual_memory()

# Диск
hdd = psutil.disk_usage('/')
total_gib = hdd.total / (1024 ** 3)
used_gib = hdd.used / (1024 ** 3)
free_gib = hdd.free / (1024 ** 3)
percent = hdd.percent

# Разделы диска
partitions_list = []
for partition in psutil.disk_partitions():
    partitions_list.append({
        "device": partition.device,
        "mountpoint": partition.mountpoint
    })

# Температура
temperatures_list = []
temperatures = psutil.sensors_temperatures()
if temperatures:
    for name, entries in temperatures.items():
        for entry in entries:
            temperatures_list.append({
                "sensor": entry.label or name,
                "current": entry.current,
                "high": entry.high,
                "critical": entry.critical
            })

# Процессы
number_of_processes = len(psutil.pids())

# Собираем всё в словарь
data = {
    "os": os_name,
    "hostname": hostname,
    "uptime": uptime_str,
    "load_average": {
        "1min": round(load1, 2),
        "5min": round(load5, 2),
        "15min": round(load15, 2)
    },
    "cpu": {
        "percent": cpu_usage
    },
    "ram": {
        "percent": ram_usage.percent,
        "used_gb": round(used_gib, 2),
        "total_gb": round(total_gib, 2)
    },
    "disk": {
        "percent": percent,
        "used_gb": round(used_gib, 2),
        "total_gb": round(total_gib, 2),
        "free_gb": round(free_gib, 2)
    },
    "partitions": partitions_list,
    "temperatures": temperatures_list,
    "processes": number_of_processes
}

print_output(data)
