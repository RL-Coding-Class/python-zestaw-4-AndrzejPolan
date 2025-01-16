from abc import ABC, abstractmethod

# Klasa abstrakcyjna dla pojazdów
class Pojazd(ABC):
    """Klasa abstrakcyjna reprezentująca pojazd."""

    def __init__(self, model: str, rok: int):
        self._model = model
        if not FabrykaPojazdow.sprawdz_rok(rok):
            raise ValueError("Nieprawidłowy rok produkcji!")
        self._rok = rok
        self._predkosc = 0

    @property
    def predkosc(self) -> float:
        """Zwraca aktualną prędkość pojazdu."""
        return self._predkosc

    @predkosc.setter
    def predkosc(self, wartosc: float):
        """Ustawia prędkość pojazdu z walidacją, że nie może być ujemna."""
        if wartosc < 0:
            raise ValueError("Prędkość nie może być ujemna!")
        self._predkosc = wartosc

    @predkosc.deleter
    def predkosc(self):
        """Resetuje prędkość pojazdu na 0."""
        self._predkosc = 0

    @abstractmethod
    def opis(self):
        """Metoda abstrakcyjna do opisania pojazdu."""
        pass

# Klasa dla samochodów
class Samochod(Pojazd):
    """Klasa reprezentująca samochód."""

    def __init__(self, model: str, rok: int, liczba_drzwi: int):
        super().__init__(model, rok)
        self.liczba_drzwi = liczba_drzwi

    def opis(self):
        return (f"Samochód: model {self._model}, rok produkcji {self._rok}, "
                f"liczba drzwi {self.liczba_drzwi}, prędkość {self._predkosc} km/h")

# Klasa dla autobusów
class Autobus(Pojazd):
    """Klasa reprezentująca autobus."""

    def __init__(self, model: str, rok: int, liczba_miejsc: int):
        super().__init__(model, rok)
        self.liczba_miejsc = liczba_miejsc

    def opis(self):
        return (f"Autobus: model {self._model}, rok produkcji {self._rok}, "
                f"liczba miejsc {self.liczba_miejsc}, prędkość {self._predkosc} km/h")

# Klasa abstrakcyjna dla fabryk pojazdów
class FabrykaPojazdow(ABC):
    """Abstrakcyjna klasa bazowa dla fabryk pojazdów."""

    def __init__(self, nazwa: str):
        self._nazwa = nazwa
        self._liczba_wyprodukowanych = 0

    @property
    def nazwa(self) -> str:
        """Zwraca nazwę fabryki."""
        return self._nazwa

    @abstractmethod
    def stworz_pojazd(self, model: str, rok: int, liczba_drzwi: int = 0, liczba_miejsc: int = 0):
        """Metoda abstrakcyjna do tworzenia pojazdu."""
        pass

    @classmethod
    def utworz_fabryke(cls, typ_fabryki: str, nazwa: str):
        """Tworzy instancję odpowiedniej klasy fabryki."""
        if typ_fabryki.lower() == 'samochod':
            return FabrykaSamochodow(nazwa)
        if typ_fabryki.lower() == 'autobus':
            return FabrykaAutobusow(nazwa)
        raise ValueError(f"Nieznany typ fabryki: {typ_fabryki}")

    @staticmethod
    def sprawdz_rok(rok: int) -> bool:
        """Waliduje rok produkcji."""
        return 1900 <= rok <= 2024

    def _zwieksz_licznik(self):
        """Zwiększa licznik wyprodukowanych pojazdów."""
        self._liczba_wyprodukowanych += 1

    def ile_wyprodukowano(self) -> int:
        """Zwraca liczbę wyprodukowanych pojazdów."""
        return self._liczba_wyprodukowanych

# Fabryka samochodów
class FabrykaSamochodow(FabrykaPojazdow):
    """Klasa reprezentująca fabrykę samochodów."""

    def stworz_pojazd(self, model: str, rok: int, liczba_drzwi: int = 4) -> Samochod:
        samochod = Samochod(model, rok, liczba_drzwi)
        self._zwieksz_licznik()
        return samochod

# Fabryka autobusów
class FabrykaAutobusow(FabrykaPojazdow):
    """Klasa reprezentująca fabrykę autobusów."""

    def stworz_pojazd(self, model: str, rok: int, liczba_miejsc: int = 50) -> Autobus:
        autobus = Autobus(model, rok, liczba_miejsc)
        self._zwieksz_licznik()
        return autobus

# Funkcja główna

def main():
    """Główna funkcja programu."""
    fabryka_samochodow = FabrykaPojazdow.utworz_fabryke('samochod', "Fabryka Samochodów Warszawa")
    fabryka_autobusow = FabrykaPojazdow.utworz_fabryke('autobus', "Fabryka Autobusów Kraków")

    print(f"Nazwa fabryki: {fabryka_samochodow.nazwa}")
    print(f"Nazwa fabryki: {fabryka_autobusow.nazwa}")

    samochod = fabryka_samochodow.stworz_pojazd("Fiat", 2023, liczba_drzwi=5)
    autobus = fabryka_autobusow.stworz_pojazd("Solaris", 2023, liczba_miejsc=60)

    samochod.predkosc = 50
    print(f"Prędkość samochodu: {samochod.predkosc}")
    del samochod.predkosc
    print(f"Prędkość po reset: {samochod.predkosc}")

    print(f"Wyprodukowano samochodów: {fabryka_samochodow.ile_wyprodukowano()}")
    print(f"Wyprodukowano autobusów: {fabryka_autobusow.ile_wyprodukowano()}")

if __name__ == "__main__":
    main()
