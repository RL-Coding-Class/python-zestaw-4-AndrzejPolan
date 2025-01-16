from abc import ABC, abstractmethod

class Pojazd(ABC):
    def __init__(self, model: str, rok: int):
        self._model = model
        if not FabrykaPojazdow.sprawdz_rok(rok):
            raise ValueError(f"Rok produkcji {rok} jest nieprawidłowy.")
        self._rok = rok
        self._predkosc = 0.0

    @property
    def predkosc(self) -> float:
        """Getter dla prędkości."""
        return self._predkosc

    @predkosc.setter
    def predkosc(self, wartość: float):
        """Setter dla prędkości z walidacją."""
        if wartość < 0:
            raise ValueError("Prędkość nie może być ujemna.")
        self._predkosc = wartość

    @predkosc.deleter
    def predkosc(self):
        """Deleter dla prędkości, resetuje prędkość na 0."""
        self._predkosc = 0.0

    @abstractmethod
    def opis(self):
        """Metoda abstrakcyjna do opisania pojazdu."""
        pass


class Samochod(Pojazd):
    def __init__(self, model: str, rok: int, liczba_drzwi: int):
        super().__init__(model, rok)
        self.liczba_drzwi = liczba_drzwi

    def opis(self):
        return (f"Samochód: model {self._model}, rok produkcji {self._rok}, "
                f"liczba drzwi {self.liczba_drzwi}, prędkość {self._predkosc} km/h")


class Autobus(Pojazd):
    def __init__(self, model: str, rok: int, liczba_miejsc: int):
        super().__init__(model, rok)
        self.liczba_miejsc = liczba_miejsc

    def opis(self):
        return (f"Autobus: model {self._model}, rok produkcji {self._rok}, "
                f"liczba miejsc {self.liczba_miejsc}, prędkość {self._predkosc} km/h")


class FabrykaPojazdow(ABC):
    def __init__(self, nazwa: str):
        self._nazwa = nazwa
        self._liczba_wyprodukowanych = 0

    @property
    def nazwa(self) -> str:
        """Getter dla nazwy fabryki (tylko odczyt)."""
        return self._nazwa

    @abstractmethod
    def stworz_pojazd(self, model: str, rok: int, dodatkowy_param: int) -> Pojazd:
        """Metoda abstrakcyjna do tworzenia pojazdu."""
        pass

    @classmethod
    def utworz_fabryke(cls, typ_fabryki: str, nazwa: str):
        """Tworzy instancję odpowiedniej klasy fabryki na podstawie typu."""
        if typ_fabryki.lower() == 'samochodow':
            return FabrykaSamochodow(nazwa)
        elif typ_fabryki.lower() == 'autobusow':
            return FabrykaAutobusow(nazwa)
        else:
            raise ValueError(f"Nieznany typ fabryki: {typ_fabryki}")

    @staticmethod
    def sprawdz_rok(rok: int) -> bool:
        """Waliduje rok produkcji (1900-2024)."""
        return 1900 <= rok <= 2024

    def _zwieksz_licznik(self):
        """Prywatna metoda zwiększająca licznik wyprodukowanych pojazdów."""
        self._liczba_wyprodukowanych += 1

    def ile_wyprodukowano(self) -> int:
        """Zwraca liczbę wyprodukowanych pojazdów."""
        return self._liczba_wyprodukowanych


class FabrykaSamochodow(FabrykaPojazdow):
    def stworz_pojazd(self, model: str, rok: int, liczba_drzwi: int) -> Samochod:
        """Tworzy obiekt klasy Samochod."""
        samochod = Samochod(model, rok, liczba_drzwi)
        self._zwieksz_licznik()
        return samochod


class FabrykaAutobusow(FabrykaPojazdow):
    def stworz_pojazd(self, model: str, rok: int, liczba_miejsc: int) -> Autobus:
        """Tworzy obiekt klasy Autobus."""
        autobus = Autobus(model, rok, liczba_miejsc)
        self._zwieksz_licznik()
        return autobus


def main():
    # Tworzenie fabryk
    fabryka_samochodow = FabrykaPojazdow.utworz_fabryke('samochodow', 'Fabryka Samochodów XYZ')
    fabryka_autobusow = FabrykaPojazdow.utworz_fabryke('autobusow', 'Fabryka Autobusów ABC')

    # Wypisanie nazw fabryk
    print(f"Nazwa fabryki samochodów: {fabryka_samochodow.nazwa}")
    print(f"Nazwa fabryki autobusów: {fabryka_autobusow.nazwa}\n")

    # Produkcja pojazdów
    samochod = fabryka_samochodow.stworz_pojazd(model="Fiat", rok=2023, liczba_drzwi=5)
    autobus = fabryka_autobusow.stworz_pojazd(model="Solaris", rok=2023, liczba_miejsc=60)

    # Wyświetlenie opisów pojazdów
    print(samochod.opis())
    print(autobus.opis(), "\n")

    # Demonstracja getterów, setterów i deleterów dla prędkości
    print("Ustawianie prędkości pojazdów:")
    samochod.predkosc = 120.5
    autobus.predkosc = 80.0
    print(f"Prędkość samochodu: {samochod.predkosc} km/h")
    print(f"Prędkość autobusu: {autobus.predkosc} km/h\n")

    print("Resetowanie prędkości pojazdów:")
    del samochod.predkosc
    del autobus.predkosc
    print(f"Prędkość samochodu po resetowaniu: {samochod.predkosc} km/h")
    print(f"Prędkość autobusu po resetowaniu: {autobus.predkosc} km/h\n")

    # Liczenie wyprodukowanych pojazdów
    print(f"Liczba wyprodukowanych samochodów: {fabryka_samochodow.ile_wyprodukowano()}")
    print(f"Liczba wyprodukowanych autobusów: {fabryka_autobusow.ile_wyprodukowano()}")

if __name__ == "__main__":
    main()
