import math
import threading
import shutil
import os
import sys
import time
import platform
import subprocess
import hashlib
import random
import string
import json
import psutil

# ─────────────────────────────────────────
#   ЦВЕТА ДЛЯ КОНСОЛИ
# ─────────────────────────────────────────
class C:
    CYAN   = "\033[96m"
    GREEN  = "\033[92m"
    YELLOW = "\033[93m"
    RED    = "\033[91m"
    MAGENTA= "\033[95m"
    BOLD   = "\033[1m"
    DIM    = "\033[2m"
    RESET  = "\033[0m"

def clr(text, color):
    return f"{color}{text}{C.RESET}"

# ─────────────────────────────────────────
#   ТЕКУЩАЯ ДИРЕКТОРИЯ
# ─────────────────────────────────────────
current_dir = os.path.expanduser("~")

# ─────────────────────────────────────────
#   ФАЙЛ ДЛЯ ПАРОЛЕЙ
# ─────────────────────────────────────────
PASS_FILE = os.path.join(os.path.expanduser("~"), ".console_passwords.json")

def load_passwords():
    if os.path.exists(PASS_FILE):
        with open(PASS_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}

def save_passwords(data):
    with open(PASS_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

# ─────────────────────────────────────────
#   ШАПКА
# ─────────────────────────────────────────
def print_banner():
    os.system("cls" if os.name == "nt" else "clear")
    print(clr("╔══════════════════════════════════════════╗", C.CYAN))
    print(clr("║         CUSTOM CONSOLE  v3.0             ║", C.CYAN))
    print(clr("╚══════════════════════════════════════════╝", C.CYAN))
    print(clr("  Введи 'help' чтобы увидеть команды\n", C.DIM))

# ─────────────────────────────────────────
#   HELP
# ─────────────────────────────────────────
def cmd_help():
    cmds = [
        ("taskmng",              "Диспетчер задач"),
        ("regedit",              "Редактор реестра"),
        ("plan.zadach",          "Планировщик задач"),
        ("zelezo",               "Характеристики ПК"),
        ("test_cp",              "Тест производительности CPU"),
        ("stress_test",          "Стресс тест CPU (low/normal/high)"),
        ("─" * 20,               ""),
        ("cd <путь>",            "Сменить директорию"),
        ("ls",                   "Содержимое текущей папки"),
        ("back",                 "Назад (cd ..)"),
        ("pwd",                  "Показать текущую папку"),
        ("open <файл>",          "Открыть файл"),
        ("find <имя>",           "Найти файл в текущей папке"),
        ("del <файл>",           "Удалить файл"),
        ("size <файл>",          "Размер файла"),
        ("─" * 20,               ""),
        ("top5 ram",              "Топ 5 процессов по памяти"),
        ("top5 cpu",              "Топ 5 процессов по процессору"),
        ("kill <имя>",           "Завершить процесс по имени"),
        ("─" * 20,               ""),
        ("where <файл>",         "Найти файл + путь ярлыка"),
        ("hash <файл>",          "MD5 / SHA256 хэш файла"),
        ("passgen <сайт> <дл>",  "Сгенерировать пароль"),
        ("passgen list",         "Список всех паролей"),
        ("─" * 20,               ""),
        ("repeat",                "Повторить последнюю команду"),
        ("history",               "Последние 10 команд"),
        ("info",                  "Информация о скрипте"),
        ("update_show",           "Проверить обновления"),
        ("─" * 20,               ""),
        ("block_show",            "Проверка файла hosts"),
        ("─" * 20,               ""),
        ("passgen_del <№>",       "Удалить пароль по номеру"),
        ("passgen_edit <№> <имя>","Переименовать сайт"),
        ("─" * 20,               ""),
        ("copy <файл> <куда>",    "Скопировать файл"),
        ("─" * 20,               ""),
        ("custom_command_add",    "Создать свою команду"),
        ("custom_command_list",   "Список своих команд"),
        ("custom_command_delete", "Удалить свою команду"),
        ("custom_command_edit",   "Изменить свою команду"),
        ("─" * 20,               ""),
        ("clear",                "Очистить консоль"),
        ("exit",                 "Выйти"),
    ]
    print(clr("\n  ┌─ КОМАНДЫ ─────────────────────────────────────┐", C.CYAN))
    for name, desc in cmds:
        if name.startswith("─"):
            print(f"  │  {clr(name, C.DIM)}")
        else:
            print(f"  │  {clr(name.ljust(22), C.GREEN)} {clr('→', C.DIM)} {desc}")
    print(clr("  └───────────────────────────────────────────────┘\n", C.CYAN))

# ─────────────────────────────────────────
#   1. TASKMNG
# ─────────────────────────────────────────
def cmd_taskmng():
    print(clr("\n[taskmng] Запуск диспетчера задач...\n", C.YELLOW))
    if os.name == "nt":
        subprocess.Popen("taskmgr")
    elif sys.platform == "darwin":
        subprocess.Popen(["open", "-a", "Activity Monitor"])
    else:
        for app in ["gnome-system-monitor", "xfce4-taskmanager", "htop"]:
            if subprocess.call(["which", app],
                               stdout=subprocess.DEVNULL,
                               stderr=subprocess.DEVNULL) == 0:
                subprocess.Popen([app])
                print(clr(f"  Открыт: {app}", C.GREEN))
                return
        print(clr("  Не найден GUI-диспетчер. Установи gnome-system-monitor.", C.RED))

# ─────────────────────────────────────────
#   2. REGEDIT
# ─────────────────────────────────────────
def cmd_regedit():
    print(clr("\n[regedit] Запуск редактора реестра...\n", C.YELLOW))
    if os.name == "nt":
        subprocess.Popen("regedit")
    else:
        print(clr("  Реестр доступен только на Windows.", C.RED))

# ─────────────────────────────────────────
#   3. PLAN.ZADACH
# ─────────────────────────────────────────
def cmd_plan_zadach():
    print(clr("\n[plan.zadach] Запуск планировщика задач...\n", C.YELLOW))
    if os.name == "nt":
        subprocess.Popen("taskschd.msc", shell=True)
    elif sys.platform == "darwin":
        print(clr("  macOS: используй LaunchAgent / cron.", C.DIM))
        subprocess.Popen(["open", "-a", "Terminal"])
    else:
        for app in ["gnome-schedule", "kcron"]:
            if subprocess.call(["which", app],
                               stdout=subprocess.DEVNULL,
                               stderr=subprocess.DEVNULL) == 0:
                subprocess.Popen([app])
                print(clr(f"  Открыт: {app}", C.GREEN))
                return
        print(clr("  Попробуй: gnome-schedule или crontab -e в терминале.", C.RED))

# ─────────────────────────────────────────
#   4. ZELEZO
# ─────────────────────────────────────────
def cmd_zelezo():
    print(clr("\n[zelezo] Характеристики ПК\n", C.YELLOW))
    print(clr("  ┌─────────────────────────────────────┐", C.CYAN))

    os_info = f"{platform.system()} {platform.release()}"
    print(f"  │  {clr('ОС      :', C.DIM)} {os_info}")

    cpu = platform.processor() or platform.machine()
    try:
        if os.name == "nt":
            out = subprocess.check_output(
                "wmic cpu get Name", shell=True).decode().strip().split("\n")
            cpu = out[1].strip() if len(out) > 1 else cpu
        elif sys.platform == "darwin":
            cpu = subprocess.check_output(
                ["sysctl", "-n", "machdep.cpu.brand_string"]).decode().strip()
        else:
            with open("/proc/cpuinfo") as f:
                for line in f:
                    if "model name" in line:
                        cpu = line.split(":")[1].strip()
                        break
    except Exception:
        pass
    print(f"  │  {clr('CPU     :', C.DIM)} {cpu}")

    try:
        import ctypes
        if os.name == "nt":
            class MEMSTATUS(ctypes.Structure):
                _fields_ = [
                    ("dwLength",                ctypes.c_ulong),
                    ("dwMemoryLoad",            ctypes.c_ulong),
                    ("ullTotalPhys",            ctypes.c_ulonglong),
                    ("ullAvailPhys",            ctypes.c_ulonglong),
                    ("ullTotalPageFile",        ctypes.c_ulonglong),
                    ("ullAvailPageFile",        ctypes.c_ulonglong),
                    ("ullTotalVirtual",         ctypes.c_ulonglong),
                    ("ullAvailVirtual",         ctypes.c_ulonglong),
                    ("sullAvailExtendedVirtual",ctypes.c_ulonglong),
                ]
            ms = MEMSTATUS()
            ms.dwLength = ctypes.sizeof(ms)
            ctypes.windll.kernel32.GlobalMemoryStatusEx(ctypes.byref(ms))
            total_gb = ms.ullTotalPhys / (1024**3)
            avail_gb = ms.ullAvailPhys / (1024**3)
            ram_str = f"{total_gb:.1f} GB  (свободно: {avail_gb:.1f} GB)"
        else:
            with open("/proc/meminfo") as f:
                lines = f.readlines()
            total = int(lines[0].split()[1])
            free  = int(lines[2].split()[1])
            ram_str = f"{total/1024/1024:.1f} GB  (свободно: {free/1024/1024:.1f} GB)"
    except Exception:
        ram_str = "Нет данных"
    print(f"  │  {clr('RAM     :', C.DIM)} {ram_str}")

    gpu = "Нет данных"
    try:
        if os.name == "nt":
            out = subprocess.check_output(
                "wmic path win32_VideoController get Name",
                shell=True).decode().strip().split("\n")
            gpu = out[1].strip() if len(out) > 1 else gpu
        elif sys.platform == "darwin":
            out = subprocess.check_output(
                ["system_profiler", "SPDisplaysDataType"]).decode()
            for line in out.split("\n"):
                if "Chipset Model" in line:
                    gpu = line.split(":")[1].strip()
                    break
        else:
            out = subprocess.check_output(
                ["lspci"], stderr=subprocess.DEVNULL).decode()
            for line in out.split("\n"):
                if "VGA" in line or "3D" in line:
                    gpu = line.split(":")[-1].strip()
                    break
    except Exception:
        pass
    print(f"  │  {clr('GPU     :', C.DIM)} {gpu}")
    print(clr("  └─────────────────────────────────────┘\n", C.CYAN))

# ─────────────────────────────────────────
#   5. TEST_CP  (баг с C.PURPLE исправлен)
# ─────────────────────────────────────────
def cmd_test_cp():
    print(clr(f"\n[!] Запуск теста CP-Score (3 секунды)...", C.YELLOW))
    start_time = time.time()
    score = 0
    while time.time() - start_time < 3:
        _ = (1.2345 * 6.789) / 0.123
        score += 1
    final_score = score // 3

    print(clr("-" * 40, C.DIM))
    print(clr(f" >>> ТВОЙ CP-SCORE: {final_score:,} <<<", C.BOLD))

    if final_score > 7_200_000:
        status = clr(" СТАТУС: [мощна]", C.MAGENTA)   # исправлено
    elif final_score > 6_000_000:
        status = clr(" СТАТУС: [ultra]", C.GREEN)
    elif final_score > 3_000_000:
        status = clr(" СТАТУС: [normal]", C.YELLOW)
    else:
        status = clr(" СТАТУС: [low]", C.RED)

    print(status)
    print(clr("-" * 40, C.DIM))
    print()

# ─────────────────────────────────────────
#   6. CD — смена директории
# ─────────────────────────────────────────
def cmd_cd(args):
    global current_dir
    if not args:
        print(clr("\n  Укажи путь. Пример: cd D:\\\n", C.RED))
        return
    path = " ".join(args)
    if os.path.isdir(path):
        current_dir = os.path.abspath(path)
        print(clr(f"\n  Перешёл в: {current_dir}\n", C.GREEN))
    else:
        print(clr(f"\n  Папка не найдена: {path}\n", C.RED))

# ─────────────────────────────────────────
#   7. LS — содержимое папки
# ─────────────────────────────────────────
def cmd_ls():
    print(clr(f"\n  Папка: {current_dir}\n", C.YELLOW))
    try:
        items = os.listdir(current_dir)
        if not items:
            print(clr("  (пусто)\n", C.DIM))
            return
        for item in sorted(items):
            full = os.path.join(current_dir, item)
            if os.path.isdir(full):
                print(f"  {clr('[папка]', C.CYAN)}  {item}")
            else:
                size = os.path.getsize(full)
                if size > 1024**2:
                    size_str = f"{size/1024**2:.1f} МБ"
                elif size > 1024:
                    size_str = f"{size/1024:.1f} КБ"
                else:
                    size_str = f"{size:,} байт"
                print(f"  {clr('[файл] ', C.GREEN)}  {item}  {clr(size_str, C.DIM)}")
        print()
    except PermissionError:
        print(clr("  Нет доступа к этой папке.\n", C.RED))

# ─────────────────────────────────────────
#   8. BACK — назад
# ─────────────────────────────────────────
def cmd_back():
    global current_dir
    parent = os.path.dirname(current_dir)
    if parent == current_dir:
        print(clr("\n  Ты уже в корне диска.\n", C.RED))
    else:
        current_dir = parent
        print(clr(f"\n  Перешёл в: {current_dir}\n", C.GREEN))

# ─────────────────────────────────────────
#   9. PWD — текущая папка
# ─────────────────────────────────────────
def cmd_pwd():
    print(clr(f"\n  Текущая папка: {current_dir}\n", C.GREEN))

# ─────────────────────────────────────────
#   10. OPEN — открыть файл
# ─────────────────────────────────────────
def cmd_open(args):
    if not args:
        print(clr("\n  Укажи файл. Пример: open котик.png\n", C.RED))
        return
    filename = " ".join(args)
    path = os.path.join(current_dir, filename) if not os.path.isabs(filename) else filename
    if not os.path.exists(path):
        print(clr(f"\n  Файл не найден: {path}\n", C.RED))
        return
    try:
        if os.name == "nt":
            os.startfile(path)
        elif sys.platform == "darwin":
            subprocess.Popen(["open", path])
        else:
            subprocess.Popen(["xdg-open", path])
        print(clr(f"\n  Открываю: {path}\n", C.GREEN))
    except Exception as e:
        print(clr(f"\n  Ошибка: {e}\n", C.RED))

# ─────────────────────────────────────────
#   11. FIND — найти файл
# ─────────────────────────────────────────
def cmd_find(args):
    if not args:
        print(clr("\n  Укажи имя файла. Пример: find котик.png\n", C.RED))
        return
    name = " ".join(args).lower()
    print(clr(f"\n  Ищу '{name}' в {current_dir}...\n", C.YELLOW))
    found = []
    for root, dirs, files in os.walk(current_dir):
        for f in files:
            if name in f.lower():
                found.append(os.path.join(root, f))
    if found:
        for p in found:
            print(f"  {clr('→', C.GREEN)} {p}")
        print(clr(f"\n  Найдено: {len(found)} файл(ов)\n", C.DIM))
    else:
        print(clr("  Ничего не найдено.\n", C.RED))

# ─────────────────────────────────────────
#   12. DEL — удалить файл
# ─────────────────────────────────────────
def cmd_del(args):
    if not args:
        print(clr("\n  Укажи файл. Пример: del test.txt\n", C.RED))
        return
    filename = " ".join(args)
    path = os.path.join(current_dir, filename) if not os.path.isabs(filename) else filename
    if not os.path.exists(path):
        print(clr(f"\n  Файл не найден: {path}\n", C.RED))
        return
    confirm = input(clr(f"\n  Удалить '{path}'? (да/нет): ", C.YELLOW)).strip().lower()
    if confirm in ("да", "y", "yes", "д"):
        try:
            os.remove(path)
            print(clr(f"  Удалено: {path}\n", C.GREEN))
        except PermissionError:
            print(clr("  Файл занят или нет доступа. Закрой его и попробуй снова.\n", C.RED))
        except Exception as e:
            print(clr(f"  Ошибка: {e}\n", C.RED))
    else:
        print(clr("  Отменено.\n", C.DIM))

# ─────────────────────────────────────────
#   13. SIZE — размер файла
# ─────────────────────────────────────────
def cmd_size(args):
    if not args:
        print(clr("\n  Укажи файл. Пример: size video.mp4\n", C.RED))
        return
    filename = " ".join(args)
    path = os.path.join(current_dir, filename) if not os.path.isabs(filename) else filename
    if not os.path.exists(path):
        print(clr(f"\n  Файл не найден: {path}\n", C.RED))
        return
    size = os.path.getsize(path)
    kb = size / 1024
    mb = kb / 1024
    gb = mb / 1024
    print(clr(f"\n  Файл: {path}", C.YELLOW))
    print(f"  Размер: {clr(f'{size:,} байт', C.GREEN)}  /  {kb:.2f} КБ  /  {mb:.2f} МБ  /  {gb:.3f} ГБ\n")

# ─────────────────────────────────────────
#   14. TOP5 — топ процессов по RAM / CPU
# ─────────────────────────────────────────
def cmd_top5(args):
    mode = args[0].lower() if args else None

    if mode not in ("ram", "cpu"):
        print(clr("\n  Укажи режим: top5 ram  или  top5 cpu\n", C.RED))
        return

    try:
        # Первый проход чтобы cpu_percent дал реальные данные
        procs_raw = list(psutil.process_iter(['pid', 'name', 'memory_info', 'cpu_percent']))
        time.sleep(0.5)

        procs = []
        for p in procs_raw:
            try:
                mem = p.info['memory_info'].rss
                cpu = p.cpu_percent(interval=None)
                procs.append((p.info['pid'], p.info['name'], mem, cpu))
            except Exception:
                pass

        if mode == "ram":
            print(clr("\n  [top5 ram] Топ 5 процессов по памяти\n", C.YELLOW))
            procs.sort(key=lambda x: x[2], reverse=True)
            print(f"  {clr('PID'.ljust(8), C.DIM)}{clr('Процесс'.ljust(30), C.DIM)}{clr('RAM', C.DIM)}")
            print(clr("  " + "─" * 50, C.DIM))
            for pid, name, mem, cpu in procs[:5]:
                mem_mb = mem / 1024 / 1024
                print(f"  {str(pid).ljust(8)}{clr(name[:28].ljust(30), C.GREEN)}{clr(f'{mem_mb:.1f} МБ', C.CYAN)}")

        elif mode == "cpu":
            print(clr("\n  [top5 cpu] Топ 5 процессов по процессору\n", C.YELLOW))
            procs.sort(key=lambda x: x[3], reverse=True)
            print(f"  {clr('PID'.ljust(8), C.DIM)}{clr('Процесс'.ljust(30), C.DIM)}{clr('CPU %', C.DIM)}")
            print(clr("  " + "─" * 50, C.DIM))
            for pid, name, mem, cpu in procs[:5]:
                print(f"  {str(pid).ljust(8)}{clr(name[:28].ljust(30), C.GREEN)}{clr(f'{cpu:.1f}%', C.YELLOW)}")

        print()
    except Exception as e:
        print(clr(f"  Ошибка: {e}\n  Установи psutil: pip install psutil\n", C.RED))

# ─────────────────────────────────────────
#   18. STRESS_TEST — стресс тест CPU
# ─────────────────────────────────────────
def cmd_stress_test():
    import threading

    print(clr("\n  Какой режим?", C.YELLOW))
    print(f"  {clr('1', C.GREEN)} → low    (2 потока,  5 сек)")
    print(f"  {clr('2', C.GREEN)} → normal (4 потока, 10 сек)")
    print(f"  {clr('3', C.GREEN)} → high   (8 потоков, 15 сек)\n")

    choice = input(clr("  Выбери режим (low/normal/high): ", C.CYAN)).strip().lower()

    if choice == "low":
        threads_count, duration = 4, 10
    elif choice == "normal":
        threads_count, duration = 8, 15
    elif choice == "high":
        threads_count, duration = 16, 20
    else:
        print(clr("\n  Неизвестный режим. Введи low, normal или high.\n", C.RED))
        return

    print(clr(f"\n  Запускаю stress_test [{choice}] — {duration} сек, {threads_count} потоков...\n", C.YELLOW))

    scores = [0] * threads_count
    stop_flag = threading.Event()

    def worker(idx):
        while not stop_flag.is_set():
            _ = (1.2345 * 6.789) / 0.123
            scores[idx] += 1

    # Запускаем потоки
    thread_list = []
    for i in range(threads_count):
        t = threading.Thread(target=worker, args=(i,))
        t.daemon = True
        t.start()
        thread_list.append(t)

    # Таймер с прогрессом
    for i in range(duration):
        time.sleep(1)
        bar = clr("█" * (i + 1), C.GREEN) + clr("░" * (duration - i - 1), C.DIM)
        print(f"\r  [{bar}] {i+1}/{duration} сек", end="", flush=True)

    stop_flag.set()
    for t in thread_list:
        t.join()

    total_score = sum(scores) // duration

    print(f"\n\n{clr('  ─' * 25, C.DIM)}")
    print(clr(f"  >>> STRESS SCORE: {total_score:,} <<<", C.BOLD))

    if total_score > 25_000_000:
        status = clr("  СТАТУС: [зверь]", C.MAGENTA)
    elif total_score > 15_000_000:
        status = clr("  СТАТУС: [мощно]", C.GREEN)
    elif total_score > 8_000_000:
        status = clr("  СТАТУС: [нормально]", C.YELLOW)
    else:
        status = clr("  СТАТУС: [слабовато]", C.RED)

    print(status)
    print(clr(f"  Потоков: {threads_count}  |  Время: {duration} сек", C.DIM))
    print(f"{clr('  ─' * 25, C.DIM)}\n")


def cmd_kill(args):
    if not args:
        print(clr("\n  Укажи имя процесса. Пример: kill brave.exe\n", C.RED))
        return

    name = " ".join(args).lower()
    found = []

    for p in psutil.process_iter(['pid', 'name']):
        try:
            if p.info['name'].lower() == name:
                found.append(p)
        except Exception:
            pass

    if not found:
        print(clr(f"\n  Процесс '{name}' не найден.\n", C.RED))
        return

    print(clr(f"\n  Найдено процессов: {len(found)}", C.YELLOW))
    for p in found:
        print(f"  {clr('PID:', C.DIM)} {p.info['pid']}  {clr(p.info['name'], C.GREEN)}")

    confirm = input(clr(f"\n  Завершить все? (да/нет): ", C.YELLOW)).strip().lower()
    if confirm in ("да", "y", "yes", "д"):
        killed = 0
        for p in found:
            try:
                p.kill()
                killed += 1
            except psutil.AccessDenied:
                print(clr(f"  Нет доступа к PID {p.info['pid']} — запусти от администратора.", C.RED))
            except Exception as e:
                print(clr(f"  Ошибка PID {p.info['pid']}: {e}", C.RED))
        if killed:
            print(clr(f"  Завершено: {killed} процесс(ов)\n", C.GREEN))
    else:
        print(clr("  Отменено.\n", C.DIM))

# ─────────────────────────────────────────
#   18. WHERE — найти файл / путь ярлыка
# ─────────────────────────────────────────
def cmd_where(args):
    if not args:
        print(clr("\n  Укажи имя файла. Пример: where brave.exe\n", C.RED))
        return

    name = " ".join(args).lower()
    print(clr(f"\n  Ищу '{name}' по всему ПК...\n", C.YELLOW))

    # Места где искать
    search_roots = []
    if os.name == "nt":
        for drive in ["C:\\", "D:\\", "E:\\"]:
            if os.path.exists(drive):
                search_roots.append(drive)
    else:
        search_roots = ["/"]

    found = []
    for root in search_roots:
        for dirpath, dirs, files in os.walk(root):
            # Пропускаем системные папки которые точно не нужны
            dirs[:] = [d for d in dirs if d not in [
                "Windows\\WinSxS", "WinSxS", "$Recycle.Bin", "System Volume Information"
            ]]
            for f in files:
                if f.lower() == name:
                    found.append(os.path.join(dirpath, f))

    if not found:
        print(clr("  Файл не найден.\n", C.RED))
        return

    for path in found:
        print(f"  {clr('Найдено:', C.GREEN)} {path}")

        # Если это ярлык .lnk — раскрываем куда ведёт
        if path.lower().endswith(".lnk") and os.name == "nt":
            try:
                import winreg
                ps_cmd = (
                    f'(New-Object -ComObject WScript.Shell)'
                    f'.CreateShortcut("{path}").TargetPath'
                )
                result = subprocess.check_output(
                    ["powershell", "-Command", ps_cmd],
                    stderr=subprocess.DEVNULL
                ).decode().strip()
                if result:
                    print(f"  {clr('Ведёт к:', C.CYAN)} {result}")
            except Exception:
                print(clr("  (не удалось прочитать ярлык)", C.DIM))

    print()

# ─────────────────────────────────────────
#   15. HASH — хэш файла
# ─────────────────────────────────────────
def cmd_hash(args):
    if not args:
        print(clr("\n  Укажи файл. Пример: hash setup.exe\n", C.RED))
        return
    filename = " ".join(args)
    path = os.path.join(current_dir, filename) if not os.path.isabs(filename) else filename
    if not os.path.exists(path):
        print(clr(f"\n  Файл не найден: {path}\n", C.RED))
        return
    print(clr(f"\n  Считаю хэш: {path}\n", C.YELLOW))
    try:
        md5    = hashlib.md5()
        sha256 = hashlib.sha256()
        with open(path, "rb") as f:
            while chunk := f.read(8192):
                md5.update(chunk)
                sha256.update(chunk)
        print(f"  {clr('MD5   :', C.DIM)} {clr(md5.hexdigest(), C.GREEN)}")
        print(f"  {clr('SHA256:', C.DIM)} {clr(sha256.hexdigest(), C.CYAN)}\n")
    except PermissionError:
        print(clr("  Нет доступа к файлу.\n", C.RED))

# ─────────────────────────────────────────
#   16. PASSGEN — генератор паролей
# ─────────────────────────────────────────
def cmd_passgen(args):
    passwords = load_passwords()

    # passgen list
    if args and args[0].lower() == "list":
        if not passwords:
            print(clr("\n  Паролей нет. Создай: passgen сайт длина\n", C.DIM))
            return
        print(clr("\n  ┌─ ПАРОЛИ ──────────────────────────────────┐", C.CYAN))
        for site, pwd in passwords.items():
            print(f"  │  {clr(site.ljust(20), C.GREEN)} {clr('→', C.DIM)} {pwd}")
        print(clr("  └───────────────────────────────────────────┘\n", C.CYAN))
        return

    # passgen <сайт> <длина>
    if len(args) < 2:
        print(clr("\n  Использование: passgen <сайт> <длина>  или  passgen list\n", C.RED))
        return

    site = args[0]
    try:
        length = int(args[1])
        if length < 4:
            print(clr("\n  Минимальная длина — 4 символа.\n", C.RED))
            return
    except ValueError:
        print(clr("\n  Длина должна быть числом. Пример: passgen google 16\n", C.RED))
        return

    chars = string.ascii_letters + string.digits + "!@#$%^&*"
    password = "".join(random.choices(chars, k=length))

    passwords[site] = password
    save_passwords(passwords)

    print(clr(f"\n  Сайт   : {site}", C.YELLOW))
    print(f"  Пароль : {clr(password, C.GREEN)}")
    print(clr("  Сохранено в список паролей.\n", C.DIM))

# ─────────────────────────────────────────
#   ИСТОРИЯ КОМАНД
# ─────────────────────────────────────────
command_history = []
last_command = None

# ─────────────────────────────────────────
#   ФАЙЛ ДЛЯ КАСТОМНЫХ КОМАНД
# ─────────────────────────────────────────
CUSTOM_CMD_FILE = os.path.join(os.path.expanduser("~"), ".console_custom_commands.json")

def load_custom_commands():
    if os.path.exists(CUSTOM_CMD_FILE):
        with open(CUSTOM_CMD_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}

def save_custom_commands(data):
    with open(CUSTOM_CMD_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

# ─────────────────────────────────────────
#   25. REPEAT — повторить последнюю команду
# ─────────────────────────────────────────
def cmd_repeat():
    global last_command
    if not last_command or last_command == "repeat":
        print(clr("\n  Нет команды для повтора.\n", C.RED))
        return
    print(clr(f"\n  Повторяю: {last_command}\n", C.DIM))
    route(last_command)

# ─────────────────────────────────────────
#   26. HISTORY — история команд
# ─────────────────────────────────────────
def cmd_history():
    if not command_history:
        print(clr("\n  История пуста.\n", C.DIM))
        return
    print(clr("\n  ┌─ ИСТОРИЯ ─────────────────────────────┐", C.CYAN))
    for i, cmd in enumerate(command_history[-10:], 1):
        print(f"  │  {clr(str(i).ljust(3), C.DIM)} {clr(cmd, C.GREEN)}")
    print(clr("  └───────────────────────────────────────┘\n", C.CYAN))

# ─────────────────────────────────────────
#   27. PASSGEN_DEL — удалить пароль
# ─────────────────────────────────────────
def cmd_passgen_del(args):
    passwords = load_passwords()
    if not passwords:
        print(clr("\n  Паролей нет.\n", C.RED))
        return
    if not args:
        print(clr("\n  Укажи номер. Пример: passgen_del 2\n", C.RED))
        return
    try:
        idx = int(args[0]) - 1
        keys = list(passwords.keys())
        if idx < 0 or idx >= len(keys):
            print(clr("\n  Неверный номер.\n", C.RED))
            return
        site = keys[idx]
        confirm = input(clr(f"\n  Удалить пароль для '{site}'? (да/нет): ", C.YELLOW)).strip().lower()
        if confirm in ("да", "y", "yes", "д"):
            del passwords[site]
            save_passwords(passwords)
            print(clr(f"  Удалено: {site}\n", C.GREEN))
        else:
            print(clr("  Отменено.\n", C.DIM))
    except ValueError:
        print(clr("\n  Укажи число. Пример: passgen_del 2\n", C.RED))

# ─────────────────────────────────────────
#   28. PASSGEN_EDIT — переименовать сайт
# ─────────────────────────────────────────
def cmd_passgen_edit(args):
    passwords = load_passwords()
    if not passwords:
        print(clr("\n  Паролей нет.\n", C.RED))
        return
    if len(args) < 2:
        print(clr("\n  Использование: passgen_edit <номер> <новое имя>\n", C.RED))
        return
    try:
        idx = int(args[0]) - 1
        keys = list(passwords.keys())
        if idx < 0 or idx >= len(keys):
            print(clr("\n  Неверный номер.\n", C.RED))
            return
        old_site = keys[idx]
        new_site = args[1]
        pwd = passwords[old_site]
        del passwords[old_site]
        passwords[new_site] = pwd
        save_passwords(passwords)
        print(clr(f"\n  Переименовано: {old_site} → {new_site}\n", C.GREEN))
    except ValueError:
        print(clr("\n  Укажи число. Пример: passgen_edit 2 новоеимя\n", C.RED))

# ─────────────────────────────────────────
#   29. COPY — скопировать файл
# ─────────────────────────────────────────
def cmd_copy(args):
    if len(args) < 2:
        print(clr("\n  Использование: copy <файл> <куда>\n", C.RED))
        return
    src = args[0]
    dst = args[1]
    src_path = os.path.join(current_dir, src) if not os.path.isabs(src) else src
    dst_path = os.path.join(current_dir, dst) if not os.path.isabs(dst) else dst
    if not os.path.exists(src_path):
        print(clr(f"\n  Файл не найден: {src_path}\n", C.RED))
        return
    try:
        shutil.copy2(src_path, dst_path)
        print(clr(f"\n  Скопировано: {src_path} → {dst_path}\n", C.GREEN))
    except Exception as e:
        print(clr(f"\n  Ошибка: {e}\n", C.RED))

# ─────────────────────────────────────────
#   30. INFO — информация о скрипте
# ─────────────────────────────────────────
def cmd_info():
    print(clr("\n  ┌─ INFO ────────────────────────────────┐", C.CYAN))
    print(f"  │  {clr('Название :', C.DIM)} Custom Console")
    print(f"  │  {clr('Версия   :', C.DIM)} 3.0")
    print(f"  │  {clr('Команд   :', C.DIM)} 35")
    print(f"  │  {clr('Создан   :', C.DIM)} 2026")
    print(f"  │  {clr('Автор    :', C.DIM)} ты 😄")
    print(clr("  └───────────────────────────────────────┘\n", C.CYAN))

# ─────────────────────────────────────────
#   31. BLOCK_SHOW — проверка файла hosts
# ─────────────────────────────────────────
def cmd_block_show():
    print(clr("\n  [block_show] Проверка файла hosts\n", C.YELLOW))
    if os.name == "nt":
        hosts_path = r"C:\Windows\System32\drivers\etc\hosts"
    else:
        hosts_path = "/etc/hosts"

    try:
        with open(hosts_path, "r", encoding="utf-8", errors="ignore") as f:
            lines = f.readlines()

        blocked = []
        suspicious = []
        sus_keywords = ["google", "youtube", "vk", "facebook", "microsoft", "windows", "update"]

        for line in lines:
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            parts = line.split()
            if len(parts) >= 2 and parts[0] in ("0.0.0.0", "127.0.0.1"):
                site = parts[1]
                if site == "localhost":
                    continue
                blocked.append(site)
                if any(kw in site.lower() for kw in sus_keywords):
                    suspicious.append(site)

        if not blocked:
            print(clr("  Заблокированных сайтов нет. Всё чисто!\n", C.GREEN))
            return

        print(clr(f"  Найдено заблокированных: {len(blocked)}\n", C.DIM))
        for site in blocked:
            if site in suspicious:
                print(f"  {clr('[!]', C.RED)} {clr(site, C.RED)}  ← подозрительно!")
            else:
                print(f"  {clr('→', C.GREEN)} {site}")

        if suspicious:
            print(clr(f"\n  Подозрительных: {len(suspicious)} — возможно вирус менял hosts!\n", C.RED))
        else:
            print(clr("\n  Подозрительных записей нет.\n", C.GREEN))

    except PermissionError:
        print(clr("  Нет доступа. Запусти от администратора.\n", C.RED))
    except Exception as e:
        print(clr(f"  Ошибка: {e}\n", C.RED))

# ─────────────────────────────────────────
#   32. UPDATE_SHOW — проверка обновлений
# ─────────────────────────────────────────
CURRENT_VERSION = "3.0"
VERSION_URL = "https://raw.githubusercontent.com/cmdplusmade/theHelp.py/main/version.json"

def cmd_update_show():
    print(clr("\n  [update_show] Проверка обновлений...\n", C.YELLOW))
    try:
        import urllib.request
        with urllib.request.urlopen(VERSION_URL, timeout=5) as r:
            data = json.loads(r.read().decode())

        latest = data.get("version", "?")
        date   = data.get("date", "?")
        changes = data.get("changes", [])

        print(f"  {clr('Текущая версия :', C.DIM)} {CURRENT_VERSION}")
        print(f"  {clr('Последняя версия:', C.DIM)} {latest}")
        print(f"  {clr('Дата           :', C.DIM)} {date}\n")

        if latest == CURRENT_VERSION:
            print(clr("  У тебя последняя версия!\n", C.GREEN))
        else:
            print(clr(f"  Доступно обновление {latest}!\n", C.YELLOW))

        if changes:
            print(clr("  Что нового:", C.CYAN))
            for c in changes:
                print(f"  {clr('→', C.GREEN)} {c}")
        print()

    except Exception as e:
        print(clr(f"  Не удалось проверить обновления. Нет интернета?\n  {e}\n", C.RED))

# ─────────────────────────────────────────
#   33-36. CUSTOM_COMMAND
# ─────────────────────────────────────────
def cmd_custom_command_add():
    print(clr("\n  [custom_command_add] Создание своей команды\n", C.YELLOW))

    name = input(clr("  Название команды: ", C.CYAN)).strip().lower()
    if not name:
        print(clr("  Отменено.\n", C.DIM))
        return

    print(clr("\n  Что делает команда?", C.YELLOW))
    print(f"  {clr('1', C.GREEN)} → open   (открыть файл/программу)")
    print(f"  {clr('2', C.GREEN)} → kill   (завершить процесс)")
    print(f"  {clr('3', C.GREEN)} → find   (найти файл)")
    print(f"  {clr('4', C.GREEN)} → where  (найти файл по всему ПК)")
    action = input(clr("\n  Выбери (open/kill/find/where): ", C.CYAN)).strip().lower()
    if action not in ("open", "kill", "find", "where"):
        print(clr("  Неверное действие.\n", C.RED))
        return

    print(clr("\n  Как работает?", C.YELLOW))
    print(f"  {clr('1', C.GREEN)} → pathTF    (выполнить сразу по пути)")
    print(f"  {clr('2', C.GREEN)} → ifOpen    (когда процесс открыт)")
    print(f"  {clr('3', C.GREEN)} → ifClosed  (когда процесс был открыт но закрыли)")
    print(f"  {clr('4', C.GREEN)} → ifPressed (по нажатию Enter)")
    trigger = input(clr("\n  Выбери (pathTF/ifOpen/ifClosed/ifPressed): ", C.CYAN)).strip().lower()
    if trigger not in ("pathtf", "ifopen", "ifclosed", "ifpressed"):
        print(clr("  Неверный триггер.\n", C.RED))
        return

    extra = {}

    # ── pathTF ──────────────────────────────
    if trigger == "pathtf":
        if action == "open":
            path = input(clr("  Путь до файла: ", C.CYAN)).strip()
            extra["path"] = path
        elif action == "kill":
            proc = input(clr("  Имя процесса для завершения: ", C.CYAN)).strip()
            extra["process"] = proc
        elif action in ("find", "where"):
            fname = input(clr("  Что ищем?: ", C.CYAN)).strip()
            extra["filename"] = fname

    # ── ifOpen ──────────────────────────────
    elif trigger == "ifopen":
        proc = input(clr("  Какой процесс проверяем? (пример: chrome.exe): ", C.CYAN)).strip()
        extra["process"] = proc
        if action == "open":
            path = input(clr(f"  Что открыть если {proc} запущен?: ", C.CYAN)).strip()
            extra["path"] = path
        elif action == "kill":
            proc2 = input(clr(f"  Какой процесс убить если {proc} запущен?: ", C.CYAN)).strip()
            extra["process2"] = proc2
        elif action in ("find", "where"):
            fname = input(clr(f"  Что найти если {proc} запущен?: ", C.CYAN)).strip()
            extra["filename"] = fname

    # ── ifClosed ────────────────────────────
    elif trigger == "ifclosed":
        proc = input(clr("  Какой процесс отслеживаем? (пример: chrome.exe): ", C.CYAN)).strip()
        extra["process"] = proc
        if action == "open":
            path = input(clr(f"  Что открыть когда {proc} закроют?: ", C.CYAN)).strip()
            extra["path"] = path
        elif action == "kill":
            proc2 = input(clr(f"  Какой процесс убить когда {proc} закроют?: ", C.CYAN)).strip()
            extra["process2"] = proc2
        elif action in ("find", "where"):
            fname = input(clr(f"  Что найти когда {proc} закроют?: ", C.CYAN)).strip()
            extra["filename"] = fname

    # ── ifPressed ───────────────────────────
    elif trigger == "ifpressed":
        key = input(clr("  Клавиша (пример: F5): ", C.CYAN)).strip()
        extra["key"] = key
        if action == "open":
            path = input(clr(f"  Что открыть при нажатии {key}?: ", C.CYAN)).strip()
            extra["path"] = path
        elif action == "kill":
            proc = input(clr(f"  Какой процесс убить при нажатии {key}?: ", C.CYAN)).strip()
            extra["process"] = proc
        elif action in ("find", "where"):
            fname = input(clr(f"  Что найти при нажатии {key}?: ", C.CYAN)).strip()
            extra["filename"] = fname

    custom_cmds = load_custom_commands()
    custom_cmds[name] = {
        "action": action,
        "trigger": trigger,
        **extra
    }
    save_custom_commands(custom_cmds)
    print(clr(f"\n  Команда '{name}' создана!\n", C.GREEN))


def cmd_custom_command_list():
    custom_cmds = load_custom_commands()
    if not custom_cmds:
        print(clr("\n  Кастомных команд нет. Создай: custom_command_add\n", C.DIM))
        return
    print(clr("\n  ┌─ КАСТОМНЫЕ КОМАНДЫ ───────────────────────────┐", C.CYAN))
    for i, (name, data) in enumerate(custom_cmds.items(), 1):
        action  = data.get("action", "?")
        trigger = data.get("trigger", "?")
        path    = data.get("path", "")
        process = data.get("process", "")
        process2= data.get("process2", "")
        filename= data.get("filename", "")
        key     = data.get("key", "")

        detail = ""
        if trigger == "pathtf":
            detail = path or process or filename
        elif trigger in ("ifopen", "ifclosed"):
            state = "открыт" if trigger == "ifopen" else "закрыт"
            detail = f"{process} {state} → {path or process2 or filename}"
        elif trigger == "ifpressed":
            detail = f"клавиша {key} → {path or process or filename}"

        print(f"  │  {clr(str(i).ljust(3), C.DIM)}{clr(name.ljust(18), C.GREEN)}{clr(action.ljust(7), C.YELLOW)}{clr(detail, C.DIM)}")
    print(clr("  └───────────────────────────────────────────────┘\n", C.CYAN))


def cmd_custom_command_delete(args):
    custom_cmds = load_custom_commands()
    if not custom_cmds:
        print(clr("\n  Кастомных команд нет.\n", C.RED))
        return
    if not args:
        print(clr("\n  Укажи название. Пример: custom_command_delete моякоманда\n", C.RED))
        return
    name = args[0].lower()
    if name not in custom_cmds:
        print(clr(f"\n  Команда '{name}' не найдена.\n", C.RED))
        return
    confirm = input(clr(f"\n  Удалить команду '{name}'? (да/нет): ", C.YELLOW)).strip().lower()
    if confirm in ("да", "y", "yes", "д"):
        del custom_cmds[name]
        save_custom_commands(custom_cmds)
        print(clr(f"  Удалено: {name}\n", C.GREEN))
    else:
        print(clr("  Отменено.\n", C.DIM))


def cmd_custom_command_edit(args):
    custom_cmds = load_custom_commands()
    if not custom_cmds:
        print(clr("\n  Кастомных команд нет.\n", C.RED))
        return
    if not args:
        print(clr("\n  Укажи название. Пример: custom_command_edit моякоманда\n", C.RED))
        return
    name = args[0].lower()
    if name not in custom_cmds:
        print(clr(f"\n  Команда '{name}' не найдена.\n", C.RED))
        return
    print(clr(f"\n  Редактирую '{name}'. Пересоздаю...\n", C.YELLOW))
    del custom_cmds[name]
    save_custom_commands(custom_cmds)
    cmd_custom_command_add()


def run_custom_command(name):
    custom_cmds = load_custom_commands()
    cmd = custom_cmds[name]
    action   = cmd.get("action")
    trigger  = cmd.get("trigger")
    path     = cmd.get("path", "")
    process  = cmd.get("process", "")
    process2 = cmd.get("process2", "")
    filename = cmd.get("filename", "")
    key      = cmd.get("key", "")

    def do_action(act, target):
        if act == "open":   cmd_open([target])
        elif act == "kill": cmd_kill([target])
        elif act == "find": cmd_find([target])
        elif act == "where":cmd_where([target])

    if trigger == "pathtf":
        target = path or process or filename
        do_action(action, target)

    elif trigger == "ifopen":
        found = any(p.info['name'].lower() == process.lower()
                    for p in psutil.process_iter(['name']))
        if found:
            target = path or process2 or filename
            do_action(action, target)
        else:
            print(clr(f"\n  Процесс '{process}' не запущен — команда не выполнена.\n", C.DIM))

    elif trigger == "ifclosed":
        print(clr(f"\n  Слежу за '{process}'... закрой его чтобы выполнить команду.\n", C.YELLOW))
        # Ждём пока процесс был открыт
        was_open = any(p.info['name'].lower() == process.lower()
                       for p in psutil.process_iter(['name']))
        if not was_open:
            print(clr(f"  Процесс '{process}' не был открыт.\n", C.RED))
            return
        # Ждём закрытия
        while True:
            time.sleep(1)
            still_open = any(p.info['name'].lower() == process.lower()
                             for p in psutil.process_iter(['name']))
            if not still_open:
                break
        target = path or process2 or filename
        do_action(action, target)

    elif trigger == "ifpressed":
        input(clr(f"\n  Нажми Enter (клавиша {key}) для выполнения...", C.YELLOW))
        target = path or process or filename
        do_action(action, target)


# ─────────────────────────────────────────
#   РОУТЕР КОМАНД
# ─────────────────────────────────────────
def route(raw):
    global last_command
    parts = raw.strip().split()
    if not parts:
        return
    cmd = parts[0].lower()
    args = parts[1:]

    simple = {
        "help":                   cmd_help,
        "taskmng":                cmd_taskmng,
        "regedit":                cmd_regedit,
        "plan.zadach":            cmd_plan_zadach,
        "zelezo":                 cmd_zelezo,
        "test_cp":                cmd_test_cp,
        "stress_test":            cmd_stress_test,
        "ls":                     cmd_ls,
        "back":                   cmd_back,
        "pwd":                    cmd_pwd,
        "top5":                   lambda: cmd_top5(args),
        "repeat":                 cmd_repeat,
        "history":                cmd_history,
        "info":                   cmd_info,
        "block_show":             cmd_block_show,
        "update_show":            cmd_update_show,
        "custom_command_add":     cmd_custom_command_add,
        "custom_command_list":    cmd_custom_command_list,
    }

    if cmd != "repeat":
        last_command = raw
        if raw not in command_history:
            command_history.append(raw)

    if cmd in simple:
        simple[cmd]()
    elif cmd == "cd":
        cmd_cd(args)
    elif cmd == "open":
        cmd_open(args)
    elif cmd == "find":
        cmd_find(args)
    elif cmd == "del":
        cmd_del(args)
    elif cmd == "size":
        cmd_size(args)
    elif cmd == "kill":
        cmd_kill(args)
    elif cmd == "where":
        cmd_where(args)
    elif cmd == "hash":
        cmd_hash(args)
    elif cmd == "copy":
        cmd_copy(args)
    elif cmd == "passgen":
        cmd_passgen(args)
    elif cmd == "passgen_del":
        cmd_passgen_del(args)
    elif cmd == "passgen_edit":
        cmd_passgen_edit(args)
    elif cmd == "custom_command_delete":
        cmd_custom_command_delete(args)
    elif cmd == "custom_command_edit":
        cmd_custom_command_edit(args)
    else:
        # Проверяем кастомные команды
        custom_cmds = load_custom_commands()
        if cmd in custom_cmds:
            run_custom_command(cmd)
        else:
            print(clr(f"\n  Неизвестная команда: '{raw}'. Введи 'help'.\n", C.RED))

# ─────────────────────────────────────────
#   ГЛАВНЫЙ ЦИКЛ
# ─────────────────────────────────────────
def main():
    print_banner()
    while True:
        try:
            prompt = clr(f"[{os.path.basename(current_dir)}]", C.DIM) + clr(" >> ", C.GREEN)
            raw = input(prompt).strip()
        except (KeyboardInterrupt, EOFError):
            print(clr("\n  Выход. Пока!", C.DIM))
            break

        if not raw:
            continue

        if raw.lower() in ("exit", "quit", "q"):
            print(clr("\n  Выход. Пока!\n", C.DIM))
            break
        elif raw.lower() == "clear":
            print_banner()
        else:
            route(raw)

if __name__ == "__main__":
    main()