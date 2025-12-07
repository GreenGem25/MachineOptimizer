import json
import sys
import time
import argparse


def checkRestrictions(x_: list[int],
                      a_: list[list[int]],
                      b_: list[int],
                      c_: list[int],
                      d_: list[list[int]],
                      n_: int,
                      m_: int, ) -> bool:
    """
    Функция проверки ограничений задачи
    """
    for i in range(m_):
        sum_ = 0
        for j in range(n_):
            sum_ += x_[j] * a_[i][j]
        if sum_ < b_[i]:
            return False

    for j in range(n_):
        if x_[j] != 1 and x_[j] != 0:
            return False

    for i in range(m_):
        for j in range(n_):
            if a_[i][j] < 0 or d_[i][j] < 0 or c_[j] < 0 or b_[i] < 0:
                return False

    return True


def minimizeBranchAndBound(a_: list[list[int]],
                           b_: list[int],
                           c_: list[int],
                           d_: list[list[int]],
                           n_: int,
                           m_: int,
                           detailed: bool = False):
    """
    Минимизация с помощью метода ветвей и границ
    """
    best_x = None
    best_value = float('inf')

    def backtrack(current_idx: int, partial_solution: list[int], current_value: int) -> None:
        """
        Рекурсивная функция ветвления
        """
        nonlocal best_x, best_value

        # Базовый случай: рассмотрены все переменные
        if current_idx == n_:
            if checkRestrictions(partial_solution, a_, b_, c_, d_, n_, m_):
                if current_value < best_value:
                    best_value = current_value
                    best_x = partial_solution.copy()
            return

        if detailed:
            print("Глубина:", current_idx, end=', ')
            print("Решение:", partial_solution, end=', ')
            print("Значение:", current_value, end=', ')
            print("Лучшее:", best_value, end='')

        # Отсечение, если текущее значение хуже лучшего
        if current_value >= best_value:
            if detailed: print(", Отсечение.")
            return

        if detailed: print()

        # Ветвление: x_j = 0
        partial_solution[current_idx] = 0
        # Так как x_j = 0, ее вклад так же равен 0
        new_value_0 = current_value
        backtrack(current_idx + 1, partial_solution, new_value_0)

        # Ветвление: x_j = 1
        partial_solution[current_idx] = 1
        # Вычисляем вклад переменной j как в целевой функции
        contribution = c_[current_idx]  # xj * cj
        for i in range(m_):
            contribution += a_[i][current_idx] * d_[i][current_idx]  # xj * aij * dij
        new_value_1 = current_value + contribution
        backtrack(current_idx + 1, partial_solution, new_value_1)

        # Возвращение к изначальному решению
        partial_solution[current_idx] = 0

    # Запускаем с начальным приближением 0
    backtrack(0, [0] * n_, 0)
    return best_x, best_value


def readJson(filename: str) -> (list[list[int]], list[int], list[int], list[list[int]], int, int):
    """
    Чтение данных из файла json
    """
    with open(filename) as f:
        jsonFile = json.load(f)
    n = jsonFile["n"]
    m = jsonFile["m"]
    b = jsonFile["b"]
    c = jsonFile["c"]
    a = jsonFile["a"]
    d = jsonFile["d"]

    if n <= 0:
        raise ValueError('"n" must be > 0')
    if m <= 0:
        raise ValueError('"m" must be > 0')
    if len(b) != m:
        raise ValueError('"b" must be size of "m"')
    for item in b:
        if item < 0:
            raise ValueError('Elements in "b" must be >= 0')
    if len(c) != n:
        raise ValueError('"c" must be size of "n"')
    for item in c:
        if item < 0:
            raise ValueError('Elements in "c" must be >= 0')
    if len(a) != m:
        raise ValueError('"a" must be size of "m"')
    for item in a:
        if len(item) != n:
            raise ValueError('Elements in "a" must be size of "n"')
        for item_ in item:
            if item_ < 0:
                raise ValueError('Elements in "a[i]" must be >= 0')
    if len(d) != m:
        raise ValueError('"d" must be size of "m"')
    for item in d:
        if len(item) != n:
            raise ValueError('Elements in "d" must be size of "n"')
        for item_ in item:
            if item_ < 0:
                raise ValueError('Elements in "d[i]" must be >= 0')

    return a, b, c, d, n, m


def generateAnswer(machines: list[int], value: int) -> str:
    """
    Генерация красивого ответа для консоли
    """
    answer = ["=== Решение ===\n"]
    for i in range(len(machines)):
        answer.append(f"Станок №{i + 1} ")
        answer.append("включен\n" if machines[i] == 1 else "отключен\n")
    answer.append(f"Итоговая цена: {value}\n")
    return ''.join(answer)


def parseArgs() -> (str, int):
    """
    Парсинг аргументов приложения
    """
    if len(sys.argv) > 1:
        argParser = argparse.ArgumentParser("Machine Optimizer")
        argParser.add_argument("-f", dest="filename", type=str, help="Path to file with task data",
                               required=True)
        argParser.add_argument("-m", dest="showcase_mode", type=str, help="Use 'advanced' output or"
                                                                          " 'normal' output", required=True)
        args = argParser.parse_args()
        showcase_mode = 1 if args.showcase_mode == "advanced" else 0 if args.showcase_mode == "normal" else -1
        if showcase_mode == -1:
            print("No such showcase mode")
            exit(1)
        filename = args.filename
    else:
        exit(1)

    return filename, showcase_mode


def main() -> None:
    """
    Основная функция, запускающая все процессы приложения
    """
    try:
        filename, showcase_mode = parseArgs()
        test_data = readJson(filename)
        print("=== Метод ветвей и границ ===")
        print("С разбиением на две ветки:")
        start_time = time.perf_counter()
        print(generateAnswer(*minimizeBranchAndBound(*test_data, showcase_mode)))
        end_time = time.perf_counter()
        print(f"Время работы: {(end_time - start_time):.9f} секунд")

    except Exception as e:
        print(e)


if __name__ == '__main__':
    main()
