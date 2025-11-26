import json
import sys
import time
import argparse


def checkRestrictions(x_, a_, b_, c_, d_, n_, m_):
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


def minimizeBranchAndBound(a_, b_, c_, d_, n_, m_, detailed=False):
    """
    Минимизация с помощью метода ветвей и границ
    """
    best_x = None
    best_value = float('inf')

    def backtrack(current_idx, partial_solution, current_value):
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
            print("Глубина:", current_idx)
            print("Текущее решение:", partial_solution)
            print("Текущее значение:", current_value)
            print("Лучшее значение:", best_value)

        # Отсечение, если нижняя граница хуже лучшего решения
        if current_value >= best_value:
            if detailed: print("Отсечение.\n")
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
        contribution = c_[current_idx]
        for i in range(m_):
            contribution += a_[i][current_idx] * d_[i][current_idx]
        new_value_1 = current_value + contribution
        backtrack(current_idx + 1, partial_solution, new_value_1)

        # Backtrack
        partial_solution[current_idx] = 0

    # Запускаем с начальным приближением 0
    backtrack(0, [0] * n_, 0)
    return best_x, best_value


def readJson(filename):
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


def generateAnswer(machines, value):
    """
    Генерация красивого ответа для консоли
    """
    answer = []
    answer.append("=== Решение ===\n")
    for i in range(len(machines)):
        answer.append(f"Станок №{i + 1} ")
        answer.append("включен\n" if machines[i] == 1 else "отключен\n")
    answer.append(f"Итоговая цена: {value}\n")
    return ''.join(answer)


if __name__ == '__main__':
    try:
        filename = ""
        showcase_mode = None
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
        test_data = readJson(filename)
        print("=== Метод ветвей и границ ===")
        start_time = time.perf_counter()
        print(generateAnswer(*minimizeBranchAndBound(*test_data, showcase_mode)))
        end_time = time.perf_counter()
        print(f"Время работы: {(end_time - start_time):.9f} секунд")

    except Exception as e:
        print(e)
