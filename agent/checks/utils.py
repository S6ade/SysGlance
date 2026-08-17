# Утилиты для вывода данных в текстовом или JSON-формате
import json
import sys


# Рекурсивно форматирует словари и списки в читаемый текст
def _format_text(data, indent=0):
    lines = []
    prefix = "  " * indent

    if isinstance(data, dict):
        for key, value in data.items():
            if isinstance(value, (dict, list)):
                lines.append(f"{prefix}{key}:")
                lines.extend(_format_text(value, indent + 1))
            else:
                lines.append(f"{prefix}{key}: {value}")
    elif isinstance(data, list):
        for item in data:
            if isinstance(item, (dict, list)):
                lines.extend(_format_text(item, indent + 1))
            else:
                lines.append(f"{prefix}- {item}")
    else:
        lines.append(f"{prefix}{data}")

    return lines


# Выводит данные: JSON при --json, иначе читаемый текст
def print_output(data: dict):
    if '--json' in sys.argv:
        print(json.dumps(data, indent=2, ensure_ascii=False))
    else:
        for line in _format_text(data):
            print(line)
