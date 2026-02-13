import random
import math


def f(arg: float) -> float:
    """
    Вычисление функции в точке arg

    Параметры:
    x - аргумент для функции

    Возвращает:
    Значение функции в точке arg
    """

    return math.sin(arg)


def gen(num: int, limit_left: float, limit_right: float) -> list:
    """
    Генерирует случайных пар(отрезков) в диапазоне [a, b], в кол-ве num
    
    Параметры:
    num — количество чисел
    a — нижняя граница диапазона
    b — верхняя граница диапазона
    
    Возвращает:
    Список случайных пар(отрезков) в диапазоне [a, b], в кол-ве num
    """
    result = []
    for i in range(num):
        iterator = {'first': random.uniform(limit_left, limit_right),
                    'second': random.uniform(limit_left, limit_right)
                    }
        result.append(iterator)
    return result


def rectangle(interval_left: float , interval_right: float, func) -> float:
    """
    Вычисляет площадь прямоугольника
    под функцией на отрезке 

    Параметры:
    interval_left - левый край отрезка
    interval_right - правый край отрезка

    Возвращает:
    Площадь прямоугольника
    """
    if func(interval_left) < func(interval_right):
        return func(interval_left) * abs((interval_left - interval_right))
    else:
        return func(interval_right) * abs((interval_left - interval_right))


def optimization_integral(pairs: list, func) -> float:
    """
    Вычисляет приближенно интеграл, 
    через n-ое кол-во прямоугольников
    """
    number_size = len(pairs)
    result = 0
    for pair in pairs:
        result += func(interval_left=pair.get('first'), interval_right=pair.get('second'), func=f)
    return result/number_size

print(optimization_integral(pairs=gen(num=100, limit_left=0, limit_right=math.pi), func=rectangle))
