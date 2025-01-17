"""
.
"""

import math
from multipledispatch import dispatch


class Figura:  # pylint: disable=too-few-public-methods
    """."""

    def __init__(self):
        print("Figura init")


class Prostokat(Figura):  # pylint: disable=too-few-public-methods
    """."""

    def __init__(self, x: int, y: int):
        super().__init__()
        self.x = x
        self.y = y
        print(f"Prostokat init: x={x}, y={y}")


class Kwadrat(Prostokat):  # pylint: disable=too-few-public-methods
    """."""

    def __init__(self, x: int):
        super().__init__(x, x)
        print(f"Kwadrat init: x={x}")


class Kolo(Figura):  # pylint: disable=too-few-public-methods
    """."""

    def __init__(self, r: float):
        super().__init__()
        self.r = r
        print(f"Kolo init: r={r}")


@dispatch(Figura)
def pole(instance: Figura) -> float:  # pylint: disable=function-redefined,unused-argument
    """
    .
    """
    print("Pole: Figura")
    return 0.0


@dispatch(Prostokat)
def pole(instance: Prostokat) -> float:  # pylint: disable=function-redefined,unused-argument
    """
    .
    """
    print("Pole: Prostokat bez podania boków")
    return float(instance.x * instance.y)


@dispatch(Prostokat, int, int)
def pole(instance: Prostokat, x: int, y: int) -> float:  # pylint: disable=function-redefined,unused-argument
    """
    .
    """
    print("Pole: Prostokat z podaniem boków")
    instance.x = x
    instance.y = y
    return float(instance.x * instance.y)


@dispatch(Kwadrat)
def pole(instance: Kwadrat) -> float:  # pylint: disable=function-redefined,unused-argument
    """
    .
    """
    print("Pole: Kwadrat bez podania boku")
    return float(instance.x ** 2)


@dispatch(Kwadrat, int)
def pole(instance: Kwadrat, x: int) -> float:  # pylint: disable=function-redefined,unused-argument
    """
    .
    """
    print("Pole: Kwadrat z podaniem boku")
    instance.x = x
    return float(instance.x ** 2)


@dispatch(Kolo)
def pole(instance: Kolo) -> float:  # pylint: disable=function-redefined,unused-argument
    """
    .
    """
    print("Pole: Kolo bez podania promienia")
    return math.pi * instance.r ** 2


@dispatch(Kolo, float)
def pole(instance: Kolo, r: float) -> float:  # pylint: disable=function-redefined,unused-argument
    """
    .
    """
    print("Pole: Kolo z podaniem promienia")
    instance.r = r
    return math.pi * instance.r ** 2


def polaPowierzchni(listaFigur: list):
    """
    .
    """
    for figura in listaFigur:
        print(f"Pole obiektu: {pole(figura)}")


if __name__ == "__main__":
    print("=== Tworzenie obiektów ===")
    a = Figura()
    b = Prostokat(2, 4)
    c = Kwadrat(2)
    d = Kolo(3.0)

    print("\n=== Wywołania funkcji pole ===")
    print(f"Pole prostokąta (2x4): {pole(b)}")
    print(f"Pole kwadratu (bok=2): {pole(c)}")
    print(f"Pole koła (r=3.0): {pole(d)}")

    print("\n=== Zmiana wymiarów ===")
    print(f"Pole prostokąta po zmianie na 5x6: {pole(b, 5, 6)}")
    print(f"Pole kwadratu po zmianie boku na 7: {pole(c, 7)}")
    print(f"Pole koła po zmianie promienia na 4.0: {pole(d, 4.0)}")

    print("\n=== Polimorfizm w czasie wykonywania ===")
    polaPowierzchni([a, b, c, d])
