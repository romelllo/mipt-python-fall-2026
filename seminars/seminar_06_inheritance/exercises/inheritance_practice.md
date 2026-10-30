# Практические задания: Наследование

## Подготовка

Для большинства задач есть **заготовка** в папке [`starter/`](starter/).

```bash
python seminars/seminar_06_inheritance/exercises/starter/task_1_1.py
```

Примеры кода к каждой части — в папке [`../examples/`](../examples/).

> **Как работать с заданиями:** прочитайте условие, напишите и **запустите** свою версию,
> и только потом раскройте решение для сверки. Если ваш код работает правильно,
> он тоже верный — решение здесь не единственное.

---

## Часть 1: Наследование

> **Теория:** [README.md — Блок 1](../README.md#блок-1-наследование-10-мин) | **Примеры:** [`examples/01_inheritance.py`](../examples/01_inheritance.py)

### Задание 1.1

Заготовка: [`starter/task_1_1.py`](starter/task_1_1.py)

Опишите класс `Vehicle` с конструктором (марка и год выпуска) и методом `describe()`,
возвращающим строку `Toyota, 2020 год`. Затем опишите класс `Bicycle`, который
наследует `Vehicle` и ничего к нему не добавляет. Создайте велосипед и выведите
его описание.

<details>
<summary>Подсказка</summary>

Класс-наследник записывается как `class Bicycle(Vehicle):`. Если добавлять нечего,
в теле достаточно одного докстринга.

</details>

<details>
<summary>Решение</summary>

```python
class Vehicle:
    """Транспортное средство."""

    def __init__(self, brand, year):
        self.brand = brand
        self.year = year

    def describe(self):
        return f"{self.brand}, {self.year} год"


class Bicycle(Vehicle):
    """Велосипед."""


bicycle = Bicycle("Stels", 2021)
print(bicycle.describe())  # Stels, 2021 год
```

Ни конструктора, ни метода в `Bicycle` нет — он получил их от базового класса.

</details>

### Задание 1.2

Заготовка: [`starter/task_1_2.py`](starter/task_1_2.py)

Опишите класс `Car` — наследника `Vehicle`, у которого кроме марки и года есть
количество дверей. Конструктор базового класса переиспользуйте, а не повторяйте.

<details>
<summary>Подсказка</summary>

Обратиться к базовому классу из наследника позволяет `super()`.

</details>

<details>
<summary>Решение</summary>

```python
class Car(Vehicle):
    """Автомобиль."""

    def __init__(self, brand, year, doors):
        super().__init__(brand, year)  # марку и год заполнит базовый класс
        self.doors = doors


car = Car("Toyota", 2020, 5)
print(car.describe())  # Toyota, 2020 год
print("Дверей:", car.doors)  # 5
```

Без `super()` пришлось бы повторять `self.brand = brand` и `self.year = year`.

</details>

### Задание 1.3

Заготовка: [`starter/task_1_3.py`](starter/task_1_3.py)

Опишите класс `ElectricCar` — наследника `Car`, который переопределяет `describe()`
так, чтобы к описанию добавлялась пометка: `Tesla, 2023 год (электромобиль)`.
Описание базового класса не дублируйте. Затем проверьте через `isinstance()`,
что электромобиль является и `ElectricCar`, и `Car`, и `Vehicle`, а обычный
автомобиль электромобилем не является.

<details>
<summary>Подсказка</summary>

`super()` работает не только в конструкторе: из переопределённого метода можно
вызвать версию базового класса и дополнить её результат.

</details>

<details>
<summary>Решение</summary>

```python
class ElectricCar(Car):
    """Электромобиль."""

    def describe(self):
        return super().describe() + " (электромобиль)"


tesla = ElectricCar("Tesla", 2023, 5)
toyota = Car("Toyota", 2020, 5)

print(tesla.describe())  # Tesla, 2023 год (электромобиль)

print(isinstance(tesla, ElectricCar))  # True
print(isinstance(tesla, Car))  # True
print(isinstance(tesla, Vehicle))  # True
print(isinstance(toyota, ElectricCar))  # False
```

Наследник «является» каждым классом своей цепочки, а базовый класс наследником — нет.

</details>

---

## Часть 2: Полиморфизм

> **Теория:** [README.md — Блок 2](../README.md#блок-2-полиморфизм-и-утиная-типизация-10-мин) | **Примеры:** [`examples/02_polymorphism.py`](../examples/02_polymorphism.py)

### Задание 2.1

Заготовка: [`starter/task_2_1.py`](starter/task_2_1.py)

Опишите классы `Car`, `Bicycle` и `Boat` с общим базовым классом `Vehicle`,
у каждого своя версия метода `move()`:

```
Toyota едет по дороге
Stels едет по велодорожке
Yamaha плывёт по воде
```

Сложите по одному объекту каждого класса в список и выведите результат `move()`
для всех в одном цикле.

<details>
<summary>Решение</summary>

```python
class Vehicle:
    def __init__(self, brand):
        self.brand = brand

    def move(self):
        return f"{self.brand} движется"


class Car(Vehicle):
    def move(self):
        return f"{self.brand} едет по дороге"


class Bicycle(Vehicle):
    def move(self):
        return f"{self.brand} едет по велодорожке"


class Boat(Vehicle):
    def move(self):
        return f"{self.brand} плывёт по воде"


vehicles = [Car("Toyota"), Bicycle("Stels"), Boat("Yamaha")]

for vehicle in vehicles:
    print(vehicle.move())
```

Цикл одинаковый для всех, а поведение разное: Python сам выбирает версию метода
по классу объекта.

</details>

### Задание 2.2

Заготовка: [`starter/task_2_2.py`](starter/task_2_2.py)

Напишите функцию `show_movement(items)`, которая печатает результат `move()`
для каждого объекта списка. Опишите класс `Horse`, который **не наследует**
`Vehicle`, но тоже имеет метод `move()`. Передайте в функцию список из автомобиля
и лошади и объясните в комментарии, почему это работает.

<details>
<summary>Решение</summary>

```python
def show_movement(items):
    """Напечатать, как движется каждый объект списка."""
    for item in items:
        print(item.move())


class Horse:
    """Лошадь: к транспорту отношения не имеет, но двигаться умеет."""

    def move(self):
        return "Лошадь скачет по полю"


show_movement([Car("Toyota"), Horse()])

# Функции неважно, от какого класса произошёл объект: она вызывает move(),
# и этого достаточно. Это утиная типизация — интерфейс важнее родословной.
```

</details>

### Задание 2.3

Заготовка: [`starter/task_2_3.py`](starter/task_2_3.py)

Функция считает стоимость обслуживания и разрастается с каждым новым классом:

```python
def service_price(vehicle):
    if isinstance(vehicle, Car):
        return 5000
    elif isinstance(vehicle, Bicycle):
        return 500
    elif isinstance(vehicle, Boat):
        return 12000
```

Перепишите программу так, чтобы цепочка проверок исчезла, а цену знал сам объект.
Посчитайте общую стоимость обслуживания для списка транспорта.

<details>
<summary>Подсказка</summary>

Перенесите знание о цене внутрь классов: пусть у каждого будет метод
`service_price()`. Тогда вызывающему коду не нужно знать, кто перед ним.

</details>

<details>
<summary>Решение</summary>

```python
class Vehicle:
    def __init__(self, brand):
        self.brand = brand

    def service_price(self):
        return 0


class Car(Vehicle):
    def service_price(self):
        return 5000


class Bicycle(Vehicle):
    def service_price(self):
        return 500


class Boat(Vehicle):
    def service_price(self):
        return 12000


vehicles = [Car("Toyota"), Bicycle("Stels"), Boat("Yamaha")]

total = 0
for vehicle in vehicles:
    total += vehicle.service_price()

print("Обслуживание всего парка:", total)  # 17500
```

Теперь новый вид транспорта добавляется одним классом: цикл подсчёта трогать
не нужно. В варианте с `isinstance` пришлось бы править функцию каждый раз.

</details>

---

## Часть 3: Композиция

> **Теория:** [README.md — Блок 3](../README.md#блок-3-композиция-классов-10-мин) | **Примеры:** [`examples/03_composition.py`](../examples/03_composition.py)

### Задание 3.1

Заготовка: [`starter/task_3_1.py`](starter/task_3_1.py)

Опишите класс `Engine` (мощность и тип топлива) с методом `describe()`, который
возвращает `120 л.с., бензин`. Опишите класс `Car`, который **хранит** двигатель
в атрибуте и в своём `describe()` использует описание двигателя:

```
Toyota: 120 л.с., бензин
```

Создайте два автомобиля с разными двигателями.

<details>
<summary>Подсказка</summary>

Двигатель передаётся в конструктор автомобиля готовым объектом и сохраняется
в атрибут. Машина не наследует двигатель — она его имеет.

</details>

<details>
<summary>Решение</summary>

```python
class Engine:
    """Двигатель автомобиля."""

    def __init__(self, power, fuel):
        self.power = power
        self.fuel = fuel

    def describe(self):
        return f"{self.power} л.с., {self.fuel}"


class Car:
    """Автомобиль, у которого есть двигатель."""

    def __init__(self, brand, engine):
        self.brand = brand
        self.engine = engine

    def describe(self):
        return f"{self.brand}: {self.engine.describe()}"


print(Car("Toyota", Engine(120, "бензин")).describe())
print(Car("Tesla", Engine(300, "электричество")).describe())
```

Двигатель легко заменить другим объектом — автомобиль об этом ничего не знает.

</details>

### Задание 3.2

Заготовка: [`starter/task_3_2.py`](starter/task_3_2.py)

Опишите класс `Garage`, который хранит список автомобилей: `add(vehicle)`,
`count()`, `find_by_brand(brand)` и `describe()`. Поставьте в гараж три машины
(две — одной марки) и проверьте все методы.

<details>
<summary>Подсказка</summary>

Список машин создавайте в конструкторе — тогда у каждого гаража он будет свой.
Для поиска по марке пригодится списочное выражение (семинар 3).

</details>

<details>
<summary>Решение</summary>

```python
class Car:
    """Автомобиль (как в заготовке задания)."""

    def __init__(self, brand, year):
        self.brand = brand
        self.year = year

    def describe(self):
        return f"{self.brand}, {self.year} год"


class Garage:
    """Гараж: содержит автомобили, но сам автомобилем не является."""

    def __init__(self, address):
        self.address = address
        self.cars = []

    def add(self, vehicle):
        """Поставить машину в гараж."""
        self.cars.append(vehicle)

    def count(self):
        """Вернуть количество машин."""
        return len(self.cars)

    def find_by_brand(self, brand):
        """Вернуть список машин указанной марки."""
        return [car for car in self.cars if car.brand == brand]

    def describe(self):
        """Вернуть описание гаража со всеми машинами."""
        lines = [f"Гараж на {self.address}, машин: {self.count()}"]
        for car in self.cars:
            lines.append("  - " + car.describe())
        return "\n".join(lines)


garage = Garage("Институтском переулке")
garage.add(Car("Toyota", 2020))
garage.add(Car("Toyota", 2015))
garage.add(Car("Lada", 2019))

print(garage.count())  # 3
print(garage.describe())
print("Toyota в гараже:", len(garage.find_by_brand("Toyota")))  # 2
```

</details>

### Задание 3.3

_Задача на разбор, заготовки нет._

Для каждой пары определите, какая связь уместна — наследование («является»)
или композиция («имеет»):

1. `Book` и `Page`
2. `Dog` и `Animal`
3. `Computer` и `Processor`
4. `Student` и `Person`
5. `Playlist` и `Song`
6. `ElectricCar` и `Car`

<details>
<summary>Решение</summary>

| Пара | Связь | Почему |
|------|-------|--------|
| `Book` и `Page` | композиция | книга **состоит** из страниц, а не является страницей |
| `Dog` и `Animal` | наследование | собака **является** животным |
| `Computer` и `Processor` | композиция | у компьютера **есть** процессор |
| `Student` и `Person` | наследование | студент **является** человеком |
| `Playlist` и `Song` | композиция | плейлист **содержит** песни |
| `ElectricCar` и `Car` | наследование | электромобиль **является** автомобилем |

Проверка простая: подставьте классы в предложения «X является Y» и «у X есть Y»
и посмотрите, какое звучит осмысленно.

</details>

---

## Для самостоятельной работы

Задачи на темы, которые мы не разбираем на занятии: множественное наследование,
проблемы иерархий, аннотации типов, `import`, декораторы и `@property`
(теория — в [README](../README.md#темы-лекции-которые-мы-не-разбираем-на-занятии),
примеры — в файлах [`examples/04_inheritance_problems.py`](../examples/04_inheritance_problems.py)
и [`examples/05_typing_and_decorators.py`](../examples/05_typing_and_decorators.py)).

### Задание 4.1

Что напечатает эта программа? Сначала ответьте, потом проверьте.

```python
class Device:
    def status(self):
        return "устройство"


class Printer(Device):
    def status(self):
        return "принтер"


class Scanner(Device):
    def status(self):
        return "сканер"


class MFP(Printer, Scanner):
    """Многофункциональное устройство."""


print(MFP().status())
print([klass.__name__ for klass in MFP.__mro__])
```

<details>
<summary>Решение</summary>

```
принтер
['MFP', 'Printer', 'Scanner', 'Device', 'object']
```

Порядок поиска метода (MRO) идёт слева направо по списку родителей, поэтому
побеждает `Printer`. Поменяйте родителей местами — и программа напечатает «сканер»,
хотя в самом `MFP` не изменится ни строки. Это одна из причин избегать
множественного наследования.

</details>

### Задание 4.2

Найдите в коде нарушение принципа подстановки Лисков и объясните, почему функция
`refuel_fleet()` возвращает не то, что ожидает вызывающий код.

```python
class Car:
    def __init__(self, brand):
        self.brand = brand
        self.fuel = 0

    def refuel(self, liters):
        """Залить топливо в бак."""
        self.fuel += liters


class ElectricCar(Car):
    def refuel(self, liters):
        """Электромобиль бензином не заправляют."""
        print(f"{self.brand}: заправка не требуется")


def refuel_fleet(cars):
    """Заправить весь парк по 40 литров и вернуть общий запас топлива."""
    for car in cars:
        car.refuel(40)
    return sum(car.fuel for car in cars)


fleet = [Car("Toyota"), Car("Lada"), ElectricCar("Tesla")]
print(refuel_fleet(fleet))
```

<details>
<summary>Подсказка</summary>

Что функция `refuel_fleet()` считает верным после вызова `refuel(40)`?
Выполняется ли это для каждого объекта списка?

</details>

<details>
<summary>Решение</summary>

```
Tesla: заправка не требуется
80
```

Функция написана в расчёте на правило базового класса: «после `refuel(40)` в баке
стало на 40 литров больше». `ElectricCar` это правило нарушает — метод есть,
но он ничего не делает. Подставить электромобиль вместо обычного автомобиля нельзя,
значит, нарушен **принцип подстановки Лисков**, и наследование выбрано неудачно.

Что можно сделать:

- не наследовать `ElectricCar` от `Car`, а сделать общий базовый класс `Vehicle`
  с методом `charge_or_refuel()`, у которого для каждого вида транспорта своя
  осмысленная реализация;
- либо описать «заправляемость» отдельным интерфейсом и держать в парке два списка.

Второй классический пример того же нарушения — квадрат как наследник прямоугольника:
см. файл [`examples/04_inheritance_problems.py`](../examples/04_inheritance_problems.py).

</details>

### Задание 4.3

Добавьте аннотации типов к функциям и переменным:

```python
def total_price(prices, discount=0):
    return sum(prices) * (1 - discount)


def format_names(names):
    return ", ".join(names)


ages = {"Анна": 19, "Иван": 20}
```

<details>
<summary>Решение</summary>

```python
def total_price(prices: list[float], discount: float = 0) -> float:
    """Вернуть стоимость со скидкой."""
    return sum(prices) * (1 - discount)


def format_names(names: list[str]) -> str:
    """Склеить имена через запятую."""
    return ", ".join(names)


ages: dict[str, int] = {"Анна": 19, "Иван": 20}
```

Проверить аннотации в проекте курса можно командой `uv run ty check`.

</details>

### Задание 4.4

С помощью модуля `math` напишите функцию `distance(x1, y1, x2, y2)`, которая считает
расстояние между двумя точками на плоскости, и выведите расстояние между (0, 0)
и (3, 4).

<details>
<summary>Подсказка</summary>

Квадратный корень даёт `math.sqrt()`. Формула: корень из суммы квадратов разностей
координат.

</details>

<details>
<summary>Решение</summary>

```python
import math


def distance(x1: float, y1: float, x2: float, y2: float) -> float:
    """Вернуть расстояние между двумя точками на плоскости."""
    return math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)


print(distance(0, 0, 3, 4))  # 5.0
```

В модуле `math` для этого есть и готовая функция: `math.dist((0, 0), (3, 4))`.

</details>

### Задание 4.5

Напишите декоратор `count_calls`, который считает, сколько раз вызвали функцию,
и печатает номер вызова перед каждым запуском.

```
Вызов №1
Вызов №2
```

<details>
<summary>Подсказка</summary>

Счётчик заведите в декораторе — внутренняя функция сможет его увидеть. Чтобы
изменять его изнутри, пригодится список: `calls = [0]`, а затем `calls[0] += 1`.

</details>

<details>
<summary>Решение</summary>

```python
def count_calls(function):
    """Считать количество вызовов функции."""
    calls = [0]

    def wrapper(*args, **kwargs):
        calls[0] += 1
        print(f"Вызов №{calls[0]}")
        return function(*args, **kwargs)

    return wrapper


@count_calls
def greet(name):
    return f"Привет, {name}!"


print(greet("Анна"))
print(greet("Иван"))
```

Счётчик хранится в списке, потому что присваивание обычной переменной внутри
`wrapper` создало бы новую локальную переменную — ровно та история, что была
на семинаре 4.

</details>

### Задание 4.6

Опишите класс `Car` с атрибутами «марка» и «год выпуска» и вычисляемым атрибутом
`age`, который возвращает возраст машины в 2026 году. Обращаться к нему нужно
без скобок: `car.age`.

<details>
<summary>Решение</summary>

```python
class Car:
    """Автомобиль с вычисляемым возрастом."""

    CURRENT_YEAR = 2026

    def __init__(self, brand: str, year: int) -> None:
        self.brand = brand
        self.year = year

    @property
    def age(self) -> int:
        """Возраст автомобиля в годах."""
        return self.CURRENT_YEAR - self.year


car = Car("Toyota", 2020)
print(car.age)  # 6

car.year = 2015
print(car.age)  # 11 — пересчиталось само
```

</details>
