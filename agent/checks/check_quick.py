# Проект 1.
# Быстрая проверка сервера


# Подключаем модули
import os
import psutil
import datetime

# Сбор информации и ее вывод

# Название ОС
os_name = os.uname().sysname
print(f"ОС: {os_name}")

# Имя хоста
hostname = os.uname().nodename
print(f"HOSTNAME: {hostname}")

# Время работы сервера
boot_time = datetime.datetime.fromtimestamp(
    psutil.boot_time()).strftime("%Y-%m-%d %H:%M:%S")
print(f"Operating time: {boot_time}")
uptime = datetime.datetime.now() - datetime.datetime.fromtimestamp(psutil.boot_time())
print(f"Uptime: {uptime}")

# Средняя загрузка 1м. 5м. 15.
load1, load5, load15 = os.getloadavg()
print(
    f"Load average over the last 1 minute: {load1} \n"
    f"Load average over the last 5 minute: {load5} \n"
    f"Load average over the last 15 minute: {load15}"
)

# Использование процессора и оперативной памяти
cpu_usage = psutil.cpu_percent(interval=1)
ram_usage = psutil.virtual_memory()
print(f"CPU usage(%): {cpu_usage} \n"
      f"RAM usage(%): {ram_usage.percent} \n"
      f"RAM used(GB): {round(ram_usage.used / 1e9, 2)}"
      )

# ИСпользование диска

hdd = psutil.disk_usage('/')
total_gib = hdd.total / (1024 ** 3)
used_gib = hdd.used / (1024 ** 3)
free_gib = hdd.free / (1024 ** 3)
percent = hdd.percent
for partition in psutil.disk_partitions():
    print(
        f"Device: {partition.device}, Mounting point: {partition.mountpoint}")
print(
    f"Total: {total_gib:.2f} GiB \n"
    f"Used: {used_gib:.2f} GiB ({percent}%) \n"
    f"Freely: {free_gib:.2f} GiB"
)

# Выводим информацию о температуре(если поддерживается) (Текущая, Высокий и Критический порог)
temperatures = psutil.sensors_temperatures()
if temperatures:
    for name, entries in temperatures.items():
        for entry in entries:
            print(f"{entry.label or name}: "
                  f"Current: {entry.current} °C, "
                  f"High threshold: {entry.high} °C, "
                  f"Critical threshold: {entry.critical} °C")
else:
    print("Temperature sensors are not supported.")


# Выводим колличество запущеных процессов
number_of_processes = len(psutil.pids())
print(f"Running processes: {number_of_processes}")
