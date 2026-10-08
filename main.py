import time
import statistics
import threading
import multiprocessing
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor
from urllib.request import urlopen, Request


# ============================================================
# НАСТРОЙКИ
# ============================================================

RUNS = 3
THREADS = 4
PROCESSES = 4

# 20 URL для сетевого теста
URLS = [
    "https://example.com",
    "https://www.python.org",
    "https://www.wikipedia.org",
    "https://www.github.com",
    "https://www.google.com",
    "https://www.microsoft.com",
    "https://www.mozilla.org",
    "https://www.reddit.com",
    "https://www.apple.com",
    "https://www.nasa.gov",
    "https://www.bbc.com",
    "https://www.cnn.com",
    "https://www.ibm.com",
    "https://www.oracle.com",
    "https://www.intel.com",
    "https://www.adobe.com",
    "https://www.nvidia.com",
    "https://www.samsung.com",
    "https://www.spotify.com",
    "https://www.tesla.com",
]


# ============================================================
# ОБЩИЕ ФУНКЦИИ
# ============================================================

def print_line(char="=", length=75):
    print(char * length)


def median_time(times):
    return statistics.median(times)


def print_results(title, results):
    print()
    print_line()
    print(title)
    print_line()

    print(
        f"{'Метод':<28}"
        f"{'Запуск 1':>12}"
        f"{'Запуск 2':>12}"
        f"{'Запуск 3':>12}"
        f"{'Медиана':>12}"
    )

    print_line("-")

    for method, times in results.items():
        print(
            f"{method:<28}"
            f"{times[0]:>12.6f}"
            f"{times[1]:>12.6f}"
            f"{times[2]:>12.6f}"
            f"{median_time(times):>12.6f}"
        )

    print_line("-")
    print("Время указано в секундах.")


# ============================================================
# ЧАСТЬ 1. РАБОТА С NUMBERS.TXT
# ============================================================

def load_numbers():
    try:
        with open("numbers.txt", "r", encoding="utf-8") as file:
            numbers = []

            for line in file:
                line = line.strip()

                if line:
                    numbers.append(int(line))

            return numbers

    except FileNotFoundError:
        print("ОШИБКА: файл numbers.txt не найден!")
        print("Положи numbers.txt рядом с main.py.")
        exit()


# ---------- Обычное суммирование ----------

def sum_one_thread(numbers):
    total = 0

    for number in numbers:
        total += number

    return total


# ---------- Функция для одного участка ----------

def sum_part(numbers_part):
    total = 0

    for number in numbers_part:
        total += number

    return total


# ---------- 4 потока ----------

def sum_four_threads(numbers):
    parts = split_into_parts(numbers, THREADS)

    results = [0] * THREADS

    def worker(index):
        results[index] = sum_part(parts[index])

    threads = []

    for i in range(THREADS):
        thread = threading.Thread(
            target=worker,
            args=(i,)
        )

        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

    return sum(results)


# ---------- 4 процесса ----------

def sum_four_processes(numbers):
    parts = split_into_parts(numbers, PROCESSES)

    with multiprocessing.Pool(PROCESSES) as pool:
        results = pool.map(sum_part, parts)

    return sum(results)


# ---------- Разделение списка ----------

def split_into_parts(data, count):
    length = len(data)
    part_size = length // count

    parts = []

    for i in range(count):
        start = i * part_size

        if i == count - 1:
            end = length
        else:
            end = (i + 1) * part_size

        parts.append(data[start:end])

    return parts


# ---------- Измерение суммы ----------

def benchmark_sum(numbers, function):
    times = []
    answer = None

    for _ in range(RUNS):
        start = time.perf_counter()

        answer = function(numbers)

        end = time.perf_counter()

        times.append(end - start)

    return times, answer


def run_sum_test(numbers):
    print()
    print_line()
    print("ЧАСТЬ 1 — СУММИРОВАНИЕ ЧИСЕЛ")
    print_line()

    print(f"Количество чисел: {len(numbers)}")

    results = {}

    # 1 поток
    times, answer1 = benchmark_sum(
        numbers,
        sum_one_thread
    )

    results["1 поток"] = times

    # 4 потока
    times, answer2 = benchmark_sum(
        numbers,
        sum_four_threads
    )

    results["4 потока (threading)"] = times

    # 4 процесса
    times, answer3 = benchmark_sum(
        numbers,
        sum_four_processes
    )

    results["4 процесса (multiprocessing)"] = times

    # Проверяем, одинаковая ли сумма
    if answer1 == answer2 == answer3:
        print(f"\nСумма чисел: {answer1}")
        print("Все три метода дали одинаковый результат.")
    else:
        print("\nОШИБКА: результаты отличаются!")

    print_results(
        "РЕЗУЛЬТАТЫ СУММИРОВАНИЯ",
        results
    )

    return results


# ============================================================
# ЧАСТЬ 2. СЕТЕВАЯ ЗАДАЧА
# ============================================================

def download_url(url):
    """
    Загружает URL и возвращает размер полученных данных.
    """

    try:
        request = Request(
            url,
            headers={
                "User-Agent": "Mozilla/5.0"
            }
        )

        with urlopen(request, timeout=10) as response:
            data = response.read()

            return len(data)

    except Exception:
        return 0


# ---------- Последовательная загрузка ----------

def download_sequential(urls):
    results = []

    for url in urls:
        results.append(download_url(url))

    return results


# ---------- ThreadPoolExecutor ----------

def download_threads(urls):
    with ThreadPoolExecutor(
        max_workers=THREADS
    ) as executor:

        results = list(
            executor.map(download_url, urls)
        )

    return results


# ---------- ProcessPoolExecutor ----------

def download_processes(urls):
    with ProcessPoolExecutor(
        max_workers=PROCESSES
    ) as executor:

        results = list(
            executor.map(download_url, urls)
        )

    return results


# ---------- Benchmark сети ----------

def benchmark_network(function, urls):
    times = []

    for _ in range(RUNS):
        start = time.perf_counter()

        function(urls)

        end = time.perf_counter()

        times.append(end - start)

    return times


def run_network_test():
    print()
    print_line()
    print("ЧАСТЬ 2 — СЕТЕВАЯ ЗАДАЧА")
    print_line()

    print(f"Количество URL: {len(URLS)}")
    print("Загрузка 20 веб-страниц...")

    results = {}

    # Последовательно
    results["Последовательно"] = benchmark_network(
        download_sequential,
        URLS
    )

    # 4 потока
    results["ThreadPoolExecutor (4)"] = benchmark_network(
        download_threads,
        URLS
    )

    # 4 процесса
    results["ProcessPoolExecutor (4)"] = benchmark_network(
        download_processes,
        URLS
    )

    print_results(
        "РЕЗУЛЬТАТЫ СЕТЕВОЙ ЗАДАЧИ",
        results
    )

    return results


# ============================================================
# ЧАСТЬ 4. РАЗДЕЛЕНИЕ ПАМЯТИ
# ============================================================

shared_list = []


def thread_memory_test():
    global shared_list

    shared_list.append("Изменение из потока")


def process_memory_test():
    global shared_list

    shared_list.append("Изменение из процесса")


def run_memory_test():
    print()
    print_line()
    print("ЧАСТЬ 4 — РАЗДЕЛЕНИЕ ПАМЯТИ")
    print_line()

    global shared_list

    # -------------------------
    # ТЕСТ ПОТОКА
    # -------------------------

    shared_list = []

    print("\nДо запуска потока:")
    print("Родитель:", shared_list)

    thread = threading.Thread(
        target=thread_memory_test
    )

    thread.start()
    thread.join()

    print("После запуска потока:")
    print("Родитель:", shared_list)

    # -------------------------
    # ТЕСТ ПРОЦЕССА
    # -------------------------

    shared_list = []

    print("\nДо запуска процесса:")
    print("Родитель:", shared_list)

    process = multiprocessing.Process(
        target=process_memory_test
    )

    process.start()
    process.join()

    print("После запуска процесса:")
    print("Родитель:", shared_list)

    print()
    print("ВЫВОД:")
    print("Поток изменил общий список → память общая.")
    print("Процесс не изменил список родителя → память отдельная.")


# ============================================================
# ЧАСТЬ 3. ОБЪЯСНЕНИЕ GIL
# ============================================================

def print_explanation():
    print()
    print_line()
    print("ЧАСТЬ 3 — ОБЪЯСНЕНИЕ РЕЗУЛЬТАТОВ")
    print_line()

    print("""
1. СУММИРОВАНИЕ ЧИСЕЛ — CPU-bound задача

Подсчёт суммы требует работы процессора.

В CPython существует GIL (Global Interpreter Lock).
Он не позволяет нескольким потокам одновременно выполнять
Python-код на нескольких ядрах процессора.

Поэтому 4 потока обычно НЕ дают ускорения при вычислениях.
Иногда 4 потока даже медленнее одного из-за дополнительных
затрат на создание и переключение потоков.

Процессы имеют отдельные интерпретаторы Python и отдельные GIL.
Поэтому несколько процессов могут использовать несколько ядер
процессора одновременно.

Однако процессы требуют больше ресурсов и времени на создание
и передачу данных между ними.


2. ЗАГРУЗКА URL — I/O-bound задача

При загрузке сайта программа большую часть времени ждёт:
ответа сервера, сети и получения данных.

Пока один поток ждёт, другой поток может выполнять работу.

Поэтому ThreadPoolExecutor обычно значительно быстрее
последовательной загрузки URL.

Процессы также могут выполнять такую работу параллельно,
но для простой сетевой задачи их дополнительные расходы
обычно не дают преимущества перед потоками.


3. ПАМЯТЬ

Потоки одного процесса используют общую память.
Поэтому изменение глобального списка внутри потока
видно родительскому коду.

Процессы имеют отдельные адресные пространства.
Поэтому изменение списка внутри дочернего процесса
не изменяет список родительского процесса.
""")


# ============================================================
# MAIN
# ============================================================

if __name__ == "__main__":

    # Необходимо для Windows
    multiprocessing.freeze_support()

    print_line("=")
    print("ЛАБОРАТОРНАЯ РАБОТА — ПОТОКИ И ПРОЦЕССЫ")
    print_line("=")

    print("\nЗагрузка numbers.txt...")

    numbers = load_numbers()

    if len(numbers) == 0:
        print("ОШИБКА: numbers.txt пустой!")
        exit()

    # Часть 1
    run_sum_test(numbers)

    # Часть 2
    run_network_test()

    # Часть 4
    run_memory_test()

    # Часть 3
    print_explanation()

    print()
    print_line("=")
    print("ЛАБОРАТОРНАЯ РАБОТА ЗАВЕРШЕНА")
    print_line("=")