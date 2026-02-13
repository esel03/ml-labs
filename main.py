import random
import math
from typing import List, Tuple

def f(x: float) -> float:
    """Функция sin(x)"""
    return math.sin(x)

def integral_rectangular(n: int, a: float = 0, b: float = math.pi) -> float:
    """Метод прямоугольников (по центру)"""
    h = (b - a) / n
    total = 0.0
    for i in range(n):
        x_mid = a + (i + 0.5) * h
        total += f(x_mid)
    return total * h

def monte_carlo_mean(n: int, a: float = 0, b: float = math.pi) -> float:
    """Метод Монте-Карло: усреднение значений функции"""
    total = 0.0
    for _ in range(n):
        x = random.uniform(a, b)
        total += f(x)
    return total * (b - a) / n

def monte_carlo_dart(n: int, a: float = 0, b: float = math.pi) -> float:
    """Метод Монте-Карло: бросание дротиков (в пределах прямоугольника [a,b]×[0,1])"""
    count_under = 0
    for _ in range(n):
        x = random.uniform(a, b)
        y = random.uniform(0, 1)
        if y <= f(x):
            count_under += 1
    area_rect = (b - a) * 1  # высота = 1, так как max(sin(x)) = 1
    return area_rect * count_under / n

def compute_with_confidence(method, target_accuracy: float, true_value: float = 2.0,
                            confidence: float = 0.95, max_iter: int = 1000000) -> Tuple[int, float]:
    """
    Подбирает минимальное n такое, что оценка метода попадает в точность с надежностью 95%
    Использует повторные прогоны для построения доверительного интервала.
    """
    n_min = 100
    n_max = max_iter
    half_interval = (n_min + n_max) // 2
    required_z = 1.96  # z-оценка для 95% ДИ

    while n_min < n_max:
        n = half_interval
        estimates = []
        num_runs = 30 if n < 10000 else 20  # Уменьшаем число запусков для больших n

        for _ in range(num_runs):
            estimates.append(method(n))

        mean_est = sum(estimates) / len(estimates)
        std_err = (sum((x - mean_est)**2 for x in estimates) / (len(estimates) - 1))**0.5 / len(estimates)**0.5
        margin = required_z * std_err

        if abs(mean_est - true_value) + margin < target_accuracy:
            n_max = n
        else:
            n_min = n + 1
        half_interval = (n_min + n_max) // 2

    # Финальная проверка
    estimates = [method(half_interval) for _ in range(30)]
    mean_est = sum(estimates) / len(estimates)
    std_err = (sum((x - mean_est)**2 for x in estimates) / 29)**0.5 / 30**0.5
    margin = required_z * std_err

    if abs(mean_est - true_value) + margin < target_accuracy:
        return half_interval, margin
    else:
        # Увеличиваем, пока не достигнем
        while half_interval < max_iter:
            half_interval += 100
            estimates = [method(half_interval) for _ in range(20)]
            mean_est = sum(estimates) / len(estimates)
            std_err = (sum((x - mean_est)**2 for x in estimates) / 19)**0.5 / 20**0.5
            margin = required_z * std_err
            if abs(mean_est - true_value) + margin < target_accuracy:
                return half_interval, margin
    return max_iter, margin

def find_n_for_accuracy(target_rel_accuracy: float):
    """Находит n для всех трёх методов при заданной относительной точности"""
    true_value = 2.0
    abs_accuracy = (1 - target_rel_accuracy) * true_value

    print(f"\n Точность: {target_rel_accuracy} (абсолютная погрешность < {abs_accuracy:.6f})")

    # 1. Метод прямоугольников
    n_rect = 1
    while True:
        approx = integral_rectangular(n_rect)
        if abs(approx - true_value) < abs_accuracy:
            break
        n_rect += 1

    # 2. Монте-Карло (усреднение)
    n_mc_mean, _ = compute_with_confidence(monte_carlo_mean, abs_accuracy)

    # 3. Монте-Карло (дротик)
    n_mc_dart, _ = compute_with_confidence(monte_carlo_dart, abs_accuracy)

    print(f"   Прямоугольники: {n_rect}")
    print(f"   МК (усреднение): {n_mc_mean}")
    print(f"   МК (дротик): {n_mc_dart}")

    return n_rect, n_mc_mean, n_mc_dart

# === Запуск для всех требуемых точностей ===
accuracies = [0.9, 0.99, 0.999, 0.99999]
results = []

for acc in accuracies:
    res = find_n_for_accuracy(acc)
    results.append(res)

# Вывод таблицы
print("\n" + "="*60)
print("Сводка:")
print("Точность     | Прямоуг. | МК-усредн. | МК-дротик")
print("-"*60)
for acc, (r, m, d) in zip(accuracies, results):
    print(f"{acc:8.5f}     | {r:8} | {m:10} | {d:9}")