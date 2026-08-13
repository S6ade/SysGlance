# Проверка на ресурсы сервера

# Импортируем моудль
import psutil

# Выводи информацию о загрузки CPU и количество ядер и Выводим ТОП-5 процессов (имя, pid, загрузка CPU)


def cpu_info():
    cpu_load = psutil.cpu_percent()
    cpu_count = psutil.cpu_count()
    print(
        "==========INFO CPU========== \n"
        f"Loading: {cpu_load}% \n"
        f"Number of cores: {cpu_count}"
    )
    print("==========TOP-5 procces CPU==========")

    procs_cpu = []

    for proc in psutil.process_iter(['name', 'cpu_percent']):
        procs_cpu.append(proc)

    procs_cpu.sort(key=lambda p: p.info['cpu_percent'], reverse=True)

    for proc in procs_cpu[:5]:
        print(
            f"Name: {proc.name()} PID: {proc.pid} CPU: {proc.cpu_percent()}%")
    # count += 1


# Выводи информацию RAM и Выводим ТОП-5 процессов памяти (имя, pid, загрузка CPU)


def mem_info():
    memory = psutil.virtual_memory()
    total_gb = memory.total / (1024 ** 3)
    used_gb = memory.used / (1024 ** 3)
    free_gb = memory.free / (1024 ** 3)
    print(
        f"Всего: {total_gb:.2f}GB \n"
        f"Used: {used_gb:.2f}GB \n"
        f"Free: {free_gb:.2f}GB \n"
        f"Used as %: {memory.percent}%"
    )

    proces_mem = []
    print("==========TOP-5 procces memory==========")
    for proc_mem in psutil.process_iter(['name', 'memory_percent']):
        proces_mem.append(proc_mem)

    proces_mem.sort(key=lambda p: p.info['memory_percent'], reverse=True)

    for proc_mem in proces_mem[:5]:
        print(
            f"Name: {proc_mem.name()} PID: {proc_mem.pid} Memory: {proc_mem.info['memory_percent']:.2f}%")


def disk_info():
    for disk_sections in psutil.disk_partitions():
        disk_used = psutil.disk_usage(disk_sections.mountpoint)
        print(
            f"Раздел: {disk_sections.device} ({disk_sections.mountpoint}) — Used: {disk_used.percent}%")


cpu_info()
print("=========================================")
mem_info()
print("=========================================")
disk_info()
