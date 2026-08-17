import subprocess

# Выводим ошибки journalctl, с выводом номера строки,содержимого и количество ошибок
print("\n=== Ошибки journalctl ===")
process = subprocess.run(['journalctl', '-p', '3'],
                         capture_output=True, text=True)

error_count = 0

for line in process.stdout.splitlines():
    if "error" in line.lower():
        error_count += 1
        print(f"Ошибка найдена в строке: {error_count}")
        print(f"Содержимое: {line.strip()}")
        if error_count >= 20:
            break
print(f"Колличество ошибок: {error_count}")

# Выводим строк ошибок из системного лога
error_log = subprocess.run(
    ['grep', '-iE', "error|fail|critical", '/var/log/syslog'], capture_output=True, text=True)

lines = error_log.stdout.splitlines()
for line in lines[-20:]:
    print(line)

# Выводим Сообщение о нехватке памяти и "убийстве" процессов
print("\n=== OOM-убийства ===")
journal_message_count = 0
journal_message = subprocess.run(
    ['journalctl', '-k'], capture_output=True, text=True)

for line_journal in journal_message.stdout.splitlines():
    if 'oom' in line_journal.lower():
        journal_message_count += 1
        print(f"Ошибка найдена в строке: {journal_message_count}")
        print(f"Содержимое: {line_journal.strip()}")
print(f"Колличество ошибок: {journal_message_count}")
if journal_message_count == 0:
    print("Ошибок не найдено")
else:
    print(f"Количество ошибок: {journal_message_count}")


# Выводим ошибки ядра и оборудования
print("\n=== Ошибки ядра ===")

error_cor_count = 0
error_cor = subprocess.run(['dmesg', '-l'], capture_output=True, text=True)
for line_cor in error_cor.stdout.splitlines():
    if 'error' in line_cor.lower():
        error_cor_count += 1
        print(f"Ошибка найдена в строке: {error_cor_count}")
        print(f"Содержимое: {line_cor.strip()}")
print(f"Колличество ошибок: {error_cor_count}")
if error_cor_count == 0:
    print("Ошибок не найдено")
else:
    print(f"Количество ошибок: {error_cor_count}")
