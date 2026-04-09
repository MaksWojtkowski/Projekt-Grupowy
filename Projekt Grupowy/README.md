# 🍕 Symulator Zarządzania Pizzerią

## 📋 Spis Treści

1. [Opis Gry](#opis-gry)
2. [Zasady Gry](#zasady-gry)
3. [Komendy](#komendy)
4. [Przebieg Dnia](#przebieg-dnia)
5. [System Stolików](#system-stolików)
6. [Menu Pizz](#menu-pizz)
7. [Ulepszenia](#ulepszenia)
8. [Zdarzenia Losowe](#zdarzenia-losowe)
9. [Pracownicy](#pracownicy)
10. [System Finansowy](#system-finansowy)
11. [Struktura Projektu](#struktura-projektu)
12. [Paradygmaty Programowania Obiektowego](#paradygmaty-programowania-obiektowego)
13. [Opis Klas](#opis-klas)

---

## 🎮 Opis Gry

Symulator Zarządzania Pizzerią to gra konsolowa, w której gracz wciela się w właściciela pizzerii. Celem jest rozwinięcie biznesu poprzez:
- Obsługę klientów i realizację zamówień
- Inwestowanie w ulepszenia (szkolenia pracowników, sprzęt, marketing)
- Zarządzanie stolikami i przepustowością lokalu
- Radzenie sobie z losowymi zdarzeniami

Gra kończy się **wygraną** gdy stan konta przekroczy 5000 zł lub **przegraną** w przypadku bankructwa.

---

## 📜 Zasady Gry

| Element | Wartość |
|---------|---------|
| **Kapitał początkowy** | 500 zł |
| **Cel (wygrana)** | Stan konta ≥ 5000 zł |
| **Przegrana** | Stan konta ≤ 0 zł (bankructwo) |
| **Bazowa liczba klientów** | 10 dziennie |
| **Bazowa liczba stolików** | 5 |

---

## ⌨️ Komendy

| Komenda | Alias | Opis |
|---------|-------|------|
| `start` | - | Rozpoczyna nowy dzień - klienci przychodzą i są automatycznie obsługiwani |
| `sklep` | - | Otwiera sklep ulepszeń gdzie można kupować ulepszenia za zarobione pieniądze |
| `status` | - | Wyświetla aktualny stan pizzerii (pieniądze, poziomy ulepszeń, dzień) |
| `pomoc` | `help` | Wyświetla listę dostępnych komend |
| `wyjdz` | `quit` | Kończy grę |

---

## 📅 Przebieg Dnia

### 1. Otwarcie Dnia
- Synchronizacja poziomów ulepszeń z modelami pracowników
- Usunięcie efektów zdarzeń z poprzedniego dnia
- Obliczenie liczby klientów na podstawie poziomu marketingu

### 2. Zdarzenia Losowe
Na początku dnia mogą wystąpić zdarzenia losowe:
- **Inspekcja Sanitarna** (10% szans) - kara finansowa
- **Awaria Pieca** (8% szans) - spadek efektywności pieczenia

### 3. Obsługa Klientów
Klienci przychodzą dynamicznie i:
- Zajmują wolny stolik (jeśli dostępny)
- Składają zamówienie (1-3 pizze)
- Czekają na realizację zamówienia
- Zwalniają stolik po obsłużeniu

### 4. Realizacja Zamówień
Dla każdego klienta:
- Obliczany jest czas przygotowania (zależy od pizz, kucharza i pieca)
- Obliczany jest czas obsługi (zależy od kelnera)
- Sprawdzana jest szansa na pomyłkę kucharza
- Klient płaci lub odchodzi (jeśli obsługa trwa zbyt długo)

### 5. Zamknięcie Dnia
- Podsumowanie: obsłużeni klienci, zarobki, napiwki, kary
- Pobranie rachunków (czynsz, media, składniki)
- Sprawdzenie warunku wygranej/przegranej

---

## 🪑 System Stolików

System stolików symuluje realistyczną przepustowość pizzerii:

### Jak działa:
1. **Klient przychodzi** → sprawdzane jest czy jest wolny stolik
2. **Stolik wolny** → klient zajmuje stolik i składa zamówienie
3. **Brak stolików** → klient odchodzi (odrzucony)
4. **Po obsłużeniu** → klient zwalnia stolik

### Parametry:
| Poziom Stolików | Liczba Stolików |
|-----------------|-----------------|
| 1 | 5 |
| 2 | 8 |
| 3 | 11 |
| 4 | 14 |
| 5 | 17 |

**Formuła:** `stoliki = 5 + (poziom - 1) × 3`

---

## 🍕 Menu Pizz

| Pizza | Cena Bazowa | Cena Końcowa | Koszt Składników | Czas Przygotowania | Zysk |
|-------|-------------|--------------|------------------|-------------------|------|
| Margherita | 24.00 zł | 24.00 zł | 8.00 zł | 5s | 16.00 zł |
| Pepperoni | 32.00 zł | 35.20 zł (+10%) | 12.00 zł | 6s | 23.20 zł |
| Hawaiian | 30.00 zł | 35.00 zł (+5zł) | 11.00 zł | 7s | 24.00 zł |
| Prosciutto | 38.00 zł | 43.70 zł (+15%) | 15.00 zł | 8s | 28.70 zł |

Każda pizza ma unikatową metodę `calculate_price()` demonstrującą polimorfizm.

---

## ⬆️ Ulepszenia

### Szkolenie Kucharza
| Poziom | Koszt | Efekt |
|--------|-------|-------|
| 1 | - | Bazowy (25% szans na pomyłkę) |
| 2 | 150 zł | +15% szybkości, 20% pomyłek |
| 3 | 225 zł | +30% szybkości, 15% pomyłek |
| 4 | 337 zł | +45% szybkości, 10% pomyłek |
| 5 | 506 zł | +60% szybkości, 5% pomyłek (max) |

**Formuła szybkości:** `modifier = 1 / (1 + (poziom - 1) × 0.15)`
**Formuła pomyłek:** `szansa = max(0.02, 0.25 - (poziom - 1) × 0.05)`

### Szkolenie Kelnera
| Poziom | Koszt | Efekt |
|--------|-------|-------|
| 1 | - | Bazowy czas obsługi: 3s |
| 2 | 120 zł | +20% szybkości (2.5s) |
| 3 | 180 zł | +40% szybkości (2.14s) |
| 4 | 270 zł | +60% szybkości (1.87s) |
| 5 | 405 zł | +80% szybkości (1.67s) |

**Formuła:** `czas_obsługi = 3.0 × (1 / (1 + (poziom - 1) × 0.2))`

### Piec
| Poziom | Koszt | Efekt |
|--------|-------|-------|
| 1 | - | Bazowa szybkość pieczenia |
| 2 | 200 zł | +20% szybkości |
| 3 | 300 zł | +40% szybkości |
| 4 | 450 zł | +60% szybkości |
| 5 | 675 zł | +80% szybkości (max) |

**Formuła:** `modifier = 1 / (1 + (poziom - 1) × 0.2)`

### Jakość Składników
| Poziom | Koszt | Efekt |
|--------|-------|-------|
| 1 | - | Bazowe ceny pizz |
| 2 | 120 zł | +10% do cen |
| 3 | 180 zł | +20% do cen |
| 4 | 270 zł | +30% do cen |
| 5 | 405 zł | +40% do cen (max) |

**Formuła:** `bonus_ceny = 1.0 + (poziom - 1) × 0.1`

### Marketing
| Poziom | Koszt | Efekt |
|--------|-------|-------|
| 1 | - | 10 klientów bazowo |
| 2 | 180 zł | +25% klientów (12-13) |
| 3 | 270 zł | +50% klientów (15) |
| 4 | 405 zł | +75% klientów (17-18) |
| 5 | 607 zł | +100% klientów (20) |

**Formuła:** `klienci = 10 × (1 + (poziom - 1) × 0.25) + random(-2, 3)`

### Stoliki
| Poziom | Koszt | Liczba Stolików |
|--------|-------|-----------------|
| 1 | - | 5 |
| 2 | 250 zł | 8 |
| 3 | 375 zł | 11 |
| 4 | 562 zł | 14 |
| 5 | 843 zł | 17 |

**Formuła:** `stoliki = 5 + (poziom - 1) × 3`

---

## 🎲 Zdarzenia Losowe

### Inspekcja Sanitarna
| Parametr | Wartość |
|----------|---------|
| Szansa wystąpienia | 10% na dzień |
| Kara | 50-150 zł (losowo) |
| Czas trwania | Natychmiastowa |

Inspektor sanitarny odwiedza pizzerię i nakłada karę finansową.

### Awaria Pieca
| Parametr | Wartość |
|----------|---------|
| Szansa wystąpienia | 8% na dzień |
| Efekt | Poziom pieca spada do 1 |
| Czas trwania | Do końca dnia |

Piec ulega awarii - szybkość pieczenia spada do bazowej wartości na cały dzień. Następnego dnia piec wraca do normalnego poziomu.

---

## 👨‍🍳 Pracownicy

### Kucharz (Chef)
Odpowiada za przygotowywanie pizz.

| Właściwość | Opis |
|------------|------|
| Imię | Marco (domyślnie) |
| Poziom | 1-5 |
| Szybkość | Zależy od poziomu szkolenia |
| Pomyłki | 25% → 2% (zależnie od poziomu) |

**Pomyłka kucharza:** Gdy kucharz pomyli zamówienie, klient nie płaci i naliczana jest kara równa wartości zamówienia.

### Kelner (Waiter)
Odpowiada za obsługę klientów przy stolikach.

| Właściwość | Opis |
|------------|------|
| Imię | Luigi (domyślnie) |
| Poziom | 1-5 |
| Czas obsługi | 3s → 1.67s (zależnie od poziomu) |

---

## 💰 System Finansowy

### Przychody
| Źródło | Opis |
|--------|------|
| Sprzedaż pizz | Cena × bonus jakości składników |
| Napiwki | 5-15% wartości zamówienia (zależy od szybkości obsługi) |

### Napiwki
| Szybkość obsługi | Napiwek |
|------------------|---------|
| ≤ 50% cierpliwości | 15% wartości |
| ≤ 75% cierpliwości | 10% wartości |
| ≤ 100% cierpliwości | 5% wartości |
| > cierpliwości | 0% (klient odchodzi) |

### Wydatki
| Typ | Bazowa wartość | Modyfikator |
|-----|----------------|-------------|
| Czynsz | 50 zł | +20% za każdy poziom stolików |
| Media | 30 zł | +15% za każdy poziom pieca |
| Składniki | 20 zł | +10% za każdy poziom marketingu |

### Kary
| Typ | Wartość |
|-----|---------|
| Pomyłka kucharza | Wartość zamówienia |
| Inspekcja sanitarna | 50-150 zł |

---

## 📁 Struktura Projektu

```
Projekt Grupowy/
│
├── main.py                      # Punkt wejścia - główna pętla gry
│
├── models/                      # Modele danych
│   ├── __init__.py             # Eksporty modeli
│   ├── pizza.py                # Klasa abstrakcyjna Pizza (ISellable, IPreparable)
│   ├── margherita.py           # Pizza Margherita
│   ├── pepperoni.py            # Pizza Pepperoni (+10% ceny)
│   ├── hawaiian.py             # Pizza Hawaiian (+5 zł)
│   ├── prosciutto.py           # Pizza Prosciutto (+15% ceny)
│   ├── customer.py             # Klasa Customer (cierpliwość, napiwki)
│   ├── order.py                # Klasa Order (lista pizz, cena)
│   └── kitchen.py              # Modele kuchni: Chef, Waiter, Oven, Tables, Ingredients, Marketing
│
├── interfaces/                  # Interfejsy (ABC)
│   ├── __init__.py             # Eksporty interfejsów
│   ├── sellable.py             # ISellable - calculate_price()
│   ├── upgradeable.py          # IUpgradeable - upgrade(), get_upgrade_cost(), get_level()
│   └── preparable.py           # IPreparable - get_preparation_time()
│
├── exceptions/                  # Wyjątki
│   └── __init__.py             # Hierarchia wyjątków (PizzeriaException → ...)
│
├── services/                    # Serwisy (logika biznesowa)
│   ├── __init__.py             # Eksporty serwisów
│   ├── game_engine.py          # Silnik gry - główna logika
│   ├── day_manager.py          # Zarządzanie dniem - obsługa klientów, stoliki
│   ├── upgrade_shop.py         # Sklep ulepszeń - refleksja do ładowania ulepszeń
│   ├── customer_generator.py   # Generator klientów - lambdy do tworzenia zamówień
│   └── display_service.py      # Wyświetlanie - formatowanie komunikatów
│
├── actions/                     # Akcje (komendy gracza)
│   ├── __init__.py             # Eksporty akcji
│   ├── base_action.py          # Klasa abstrakcyjna BaseAction
│   ├── start_day_action.py     # Rozpoczęcie dnia
│   ├── shop_action.py          # Otwarcie sklepu
│   ├── status_action.py        # Wyświetlenie statusu
│   ├── help_action.py          # Wyświetlenie pomocy
│   └── quit_action.py          # Wyjście z gry
│
├── upgrades/                    # Ulepszenia
│   ├── __init__.py             # Eksporty ulepszeń
│   ├── base_upgrade.py         # Klasa abstrakcyjna BaseUpgrade (IUpgradeable)
│   ├── chef_training.py        # Szkolenie kucharza
│   ├── waiter_training.py      # Szkolenie kelnera
│   ├── oven.py                 # Ulepszenie pieca
│   ├── tables_upgrade.py       # Ulepszenie stolików
│   ├── ingredient_quality.py   # Jakość składników
│   └── marketing.py            # Marketing
│
├── events/                      # Zdarzenia losowe
│   ├── __init__.py             # Eksporty zdarzeń
│   ├── random_event.py         # Klasa abstrakcyjna RandomEvent
│   ├── event_system.py         # System zarządzania zdarzeniami
│   ├── sanitary_inspection.py  # Inspekcja sanitarna
│   └── oven_breakdown.py       # Awaria pieca
│
├── routing/                     # Routing (wzorzec Command z refleksją)
│   ├── __init__.py             # Eksporty routingu
│   ├── route.py                # Klasa Route (command → action)
│   └── router.py               # Router - refleksja do ładowania akcji
│
└── README.md                    # Dokumentacja
```

---

## 🎯 Paradygmaty Programowania Obiektowego

### 1. Klasy i Obiekty
Każdy element gry jest reprezentowany przez klasę:
- `Pizza`, `Customer`, `Order` - modele danych
- `GameEngine`, `DayManager` - logika gry
- `Chef`, `Waiter`, `Oven` - modele kuchni

### 2. Hermetyzacja
Prywatne pola z kontrolowanym dostępem:
```python
class Customer:
    def __init__(self):
        self.__name = name        # Prywatne pole
        self.__patience = patience
    
    @property
    def name(self) -> str:        # Getter przez @property
        return self.__name
```

### 3. Konstruktory
Inicjalizacja z walidacją parametrów:
```python
class Pizza:
    def __init__(self, name: str, base_price: float, ingredient_cost: float, preparation_time: float):
        self.__name = name
        self.__base_price = base_price
        # ...
```

### 4. Dziedziczenie
Hierarchia klas:
```
Pizza (abstrakcyjna)
├── Margherita
├── Pepperoni
├── Hawaiian
└── Prosciutto

BaseUpgrade (abstrakcyjna)
├── ChefTraining
├── WaiterTraining
├── Oven
├── TablesUpgrade
├── IngredientQuality
└── Marketing

KitchenElement (abstrakcyjna)
├── Chef
├── Waiter
├── Oven
├── Tables
├── Ingredients
└── Marketing
```

### 5. Interfejsy (ABC)
Abstrakcyjne klasy bazowe definiujące kontrakty:
```python
class ISellable(ABC):
    @abstractmethod
    def calculate_price(self) -> float:
        pass

class IUpgradeable(ABC):
    @abstractmethod
    def upgrade(self) -> None:
        pass
    @abstractmethod
    def get_upgrade_cost(self) -> float:
        pass
```

### 6. Klasy Abstrakcyjne
Klasy z metodami abstrakcyjnymi i implementacją bazową:
- `Pizza` - abstrakcyjna `calculate_price()`
- `BaseUpgrade` - abstrakcyjna `get_effect_description()`, `get_bonus()`
- `RandomEvent` - abstrakcyjna `trigger()`, `apply_effect()`, `remove_effect()`
- `BaseAction` - abstrakcyjna `execute()`
- `KitchenElement` - abstrakcyjna `get_modifier()`

### 7. Funkcje Anonimowe (Lambdy)
Używane w generatorze klientów:
```python
class CustomerGenerator:
    def generate_customers(self, count: int) -> List[Customer]:
        generate_single: Callable[[int], Customer] = lambda i: self._create_customer()
        return list(map(generate_single, range(count)))
    
    def _generate_order(self) -> Order:
        pizza_selector: Callable[[], Pizza] = lambda: random.choice(self._pizza_classes)()
        pizzas = [pizza_selector() for _ in range(pizza_count)]
```

### 8. Wyjątki
Hierarchia wyjątków:
```
PizzeriaException (bazowy)
├── InsufficientFundsException  # Brak środków
├── BankruptcyException         # Bankructwo
├── OutOfStockException         # Brak towaru
├── CustomerLeftException       # Klient odszedł
├── InvalidActionException      # Nieprawidłowa akcja
├── RouteNotFoundException      # Nieznana komenda
└── ReflectionException         # Błąd refleksji
```

### 9. Refleksja
Dynamiczne ładowanie klas przez `importlib` i `inspect`:
```python
class Router:
    def _get_action_class(self, class_name: str) -> Type:
        module = importlib.import_module('actions')
        action_class = getattr(module, class_name)
        return action_class
    
    def _create_instance(self, action_class: Type) -> Any:
        signature = inspect.signature(action_class.__init__)
        # Analiza parametrów konstruktora
```

---

## 📚 Opis Klas

### Modele (`models/`)

| Klasa | Opis |
|-------|------|
| `Pizza` | Abstrakcyjna klasa bazowa dla wszystkich pizz. Implementuje `ISellable` i `IPreparable`. |
| `Margherita` | Pizza Margherita - podstawowa pizza, cena = cena bazowa. |
| `Pepperoni` | Pizza Pepperoni - cena = cena bazowa × 1.1. |
| `Hawaiian` | Pizza Hawaiian - cena = cena bazowa + 5 zł. |
| `Prosciutto` | Pizza Prosciutto - cena = cena bazowa × 1.15. |
| `Customer` | Reprezentuje klienta z cierpliwością i zamówieniem. Oblicza napiwki. |
| `Order` | Zamówienie zawierające listę pizz. Oblicza łączną cenę i czas. |
| `KitchenElement` | Abstrakcyjna klasa bazowa dla elementów kuchni. |
| `Chef` | Model kucharza - modyfikator szybkości i szansa pomyłki. |
| `Waiter` | Model kelnera - modyfikator czasu obsługi. |
| `Oven` | Model pieca - modyfikator szybkości pieczenia. |
| `Tables` | Model stolików - liczba stolików. |
| `Ingredients` | Model składników - bonus do cen. |
| `Marketing` | Model marketingu - bonus do liczby klientów. |

### Serwisy (`services/`)

| Klasa | Opis |
|-------|------|
| `GameEngine` | Główny silnik gry. Zarządza stanem gry, ulepszeniami, dniami. |
| `DayManager` | Zarządza przebiegiem dnia - obsługa klientów, stoliki, statystyki. |
| `UpgradeShop` | Sklep ulepszeń. Używa refleksji do dynamicznego ładowania ulepszeń. |
| `CustomerGenerator` | Generuje klientów z losowymi zamówieniami. Używa lambd. |
| `DisplayService` | Formatuje i wyświetla komunikaty dla gracza. |

### Akcje (`actions/`)

| Klasa | Opis |
|-------|------|
| `BaseAction` | Abstrakcyjna klasa bazowa dla wszystkich akcji. |
| `StartDayAction` | Rozpoczyna nowy dzień w grze. |
| `ShopAction` | Otwiera sklep ulepszeń. |
| `StatusAction` | Wyświetla status pizzerii. |
| `HelpAction` | Wyświetla pomoc. |
| `QuitAction` | Kończy grę. |

### Ulepszenia (`upgrades/`)

| Klasa | Opis |
|-------|------|
| `BaseUpgrade` | Abstrakcyjna klasa bazowa dla ulepszeń. Implementuje `IUpgradeable`. |
| `ChefTraining` | Szkolenie kucharza - szybkość i redukcja pomyłek. |
| `WaiterTraining` | Szkolenie kelnera - szybkość obsługi. |
| `Oven` | Ulepszenie pieca - szybkość pieczenia. |
| `TablesUpgrade` | Dodatkowe stoliki - większa przepustowość. |
| `IngredientQuality` | Jakość składników - wyższe ceny pizz. |
| `Marketing` | Marketing - więcej klientów. |

### Zdarzenia (`events/`)

| Klasa | Opis |
|-------|------|
| `RandomEvent` | Abstrakcyjna klasa bazowa dla zdarzeń losowych. |
| `EventSystem` | Zarządza zdarzeniami - wyzwalanie i usuwanie efektów. |
| `SanitaryInspection` | Inspekcja sanitarna - kara finansowa. |
| `OvenBreakdown` | Awaria pieca - tymczasowy spadek efektywności. |

### Routing (`routing/`)

| Klasa | Opis |
|-------|------|
| `Route` | Mapowanie komendy na klasę akcji i metodę. |
| `Router` | Dispatcher komend. Używa refleksji do tworzenia instancji akcji. |

---

## 👨‍💻 Autorzy

- Maciej Nowak
- Maksymilian Wojtkowski
- Jakub Tamioła

---
