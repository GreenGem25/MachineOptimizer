import json
import random


def generate_test_data(n, m, filename=None):
    """
    Генерирует тестовые данные для задачи оптимизации

    Args:
        n: количество переменных
        m: количество ограничений
        filename: имя файла для сохранения (если None, возвращает dict)
    """

    # Генерируем данные
    test_data = {
        "n": n,
        "m": m,
        "b": [random.randint(5, 15) for _ in range(m)],
        "c": [random.randint(10, 100) for _ in range(n)],
        "a": [],
        "d": []
    }

    # Генерируем матрицы a и d
    for i in range(m):
        row_a = [random.randint(1, 10) for _ in range(n)]
        row_d = [random.randint(10, 100) for _ in range(n)]
        test_data["a"].append(row_a)
        test_data["d"].append(row_d)

    if filename:
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(test_data, f, indent=2, ensure_ascii=False)
        print(f"Данные сохранены в {filename}")

    return test_data


def generate_specific_sizes():
    """Генерирует тестовые данные разных размеров"""

    sizes = [
        (10, 8),  # маленькая задача
        (15, 12),  # средняя задача
        (20, 15),  # большая задача
        (25, 20),  # очень большая задача
    ]

    for n, m in sizes:
        filename = f"test_{n}_{m}.json"
        generate_test_data(n, m, filename)

        # Проверяем, что данные корректны
        with open(filename, 'r') as f:
            data = json.load(f)
            print(f"Сгенерирован файл: {filename}")
            print(f"  n={data['n']}, m={data['m']}")
            print(f"  Размер матрицы a: {len(data['a'])}x{len(data['a'][0])}")


def generate_realistic_data(n, m, filename=None):
    """
    Генерирует более реалистичные данные, где есть зависимость между a и d
    (обычно большие a соответствуют большим d)
    """

    test_data = {
        "n": n,
        "m": m,
        "b": [random.randint(n * 2, n * 4) for _ in range(m)],  # b зависит от n
        "c": [random.randint(20, 200) for _ in range(n)],
        "a": [],
        "d": []
    }

    for i in range(m):
        row_a = [random.randint(1, 15) for _ in range(n)]
        # d зависит от a - обычно большие a дают большие d
        row_d = [a_val * random.randint(5, 15) for a_val in row_a]
        test_data["a"].append(row_a)
        test_data["d"].append(row_d)

    if filename:
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(test_data, f, indent=2, ensure_ascii=False)
        print(f"Реалистичные данные сохранены в {filename}")

    return test_data


# Пример использования
if __name__ == "__main__":
    # Генерируем данные разных размеров
    print("Генерация тестовых данных...")

    # 1. Маленькая задача (быстрая для отладки)
    small_data = generate_test_data(8, 6, "test_small.json")

    # 2. Средняя задача (для сравнения производительности)
    medium_data = generate_test_data(15, 10, "test_medium.json")

    # 3. Большая задача (где ветви и границы должны показать преимущество)
    large_data = generate_test_data(20, 15, "test_large.json")

    # 4. Очень большая задача (перебор будет очень медленным)
    xlarge_data = generate_test_data(25, 18, "test_xlarge.json")

    # 5. Реалистичные данные
    realistic_data = generate_realistic_data(20, 15, "test_realistic.json")

    print("\nВсе файлы сгенерированы!")
    print("Размеры задач:")
    print("- test_small.json: 8 переменных, 6 ограничений")
    print("- test_medium.json: 15 переменных, 10 ограничений")
    print("- test_large.json: 20 переменных, 15 ограничений")
    print("- test_xlarge.json: 25 переменных, 18 ограничений")
    print("- test_realistic.json: 20 переменных, 15 ограничений (реалистичные данные)")