# ТЗ: Терра-Хоппер
Автор: Сурнин Дмитрий Сергеевич

Стихия: Земля

Проект: Земляной Кенгуру-Крот «Терра-Хоппер»

Репозиторий: https://github.com/SurninDmitri/crazy-transport

Дата заморозки: 10.10.26

Версия: <1.2.0>

# 1. Назначение
Земляной Кенгуру-Крот «Терра-Хоппер» — гибридное средство передвижения, сочетающее упругую кинетику прыжков с реактивным ускорением и подземным бурением.
Предназначен для преодоления пересеченной местности и лесных троп прыжками разной дальности.
Способен мгновенно погружаться под землю с помощью мощных носовых буров.

![img.png](terra-hopper.png)

# 2. Стихия и конструкционный элемент

Стихия: Земля

- Конструкционные элементы:
    - Реактор, добавляющий энергию и скорость к далнему прыжку
    - Носовой бур, позволяющий погружаться под землю
- Ограничения стихии:
    - Способен передвигаться снаружи только прыжками разной мощности (видами прыжков)
    - Под землёй способен преодолевать не более фиксированного расстояния с помощью рывков

# 3. Публичный интерфейс

### 3.1. Класс
- class: TerraHopper
- Модуль: terra_hopper.py

### 3.2. Конструктор
```python
def __init__(
    self,
    name: str,
    mass_kg: float,
    strength: float = 100.0,
    reactor_energy: float = 100.0,
) -> None:
```
| Параметр       | Тип   | Единица              | Допустимый диапазон | Значение по умолчанию | Описание                          |
|----------------|-------|----------------------|---------------------|-----------------------|-----------------------------------|
| name           | str   | —                    | непустая строка     | —                     | Уникальное имя транспорта.        |
| mass_kg        | float | кг                   | 100.0 … 500.0       | —                     | Масса транспорта.                 |
| strength       | float | условные единицы (%) | 0 … 100             | 100.0                 | Начальный запас силы механических узлов. |
| reactor_energy | float | условные единицы (%) | 0 … 100             | 100.0                 | Начальный запас энергии реактора. |

**Исключения конструктора:**
- ValueError — если name пустой или состоит только из пробелов. **Текст ошибки:** "Имя не может быть пустым."
- ValueError — если mass_kg вне диапазона 100.0…500.0. **Текст ошибки:** "Масса должна быть в диапазоне 100.0…500.0 кг."
- ValueError — если strength вне диапазона 0…100. **Текст ошибки:** "Сила должна быть в диапазоне 0…100."
- ValueError — если reactor_energy вне диапазона 0…100. **Текст ошибки:** "Энергия реактора должна быть в диапазоне 0…100."

### 3.3. Атрибуты
| Атрибут        | Тип   | Единица              | Доступ | Описание                                          |
|----------------|-------|----------------------|--------|---------------------------------------------------|
| name           | str   | —                    | чтение | Имя транспорта                                    |
| mass_kg        | float | кг                   | чтение | Масса транспорта                                  |
| strength       | float | условные единицы (%) | чтение | Текущий запас силы и прочности                    |
| reactor_energy | float | условные единицы (%) | чтение | Текущий запас энергии реактора                    |
| location_state | str   | —                    | чтение | Текущее положение («surface» или «underground»)   |
| distance       | float | метры                | чтение | Общее пройденное расстояние                       |

### 3.4. Методы

#### 3.4.1. basic_jump
```python
def basic_jump(self) -> None:
```
**Назначение:** Совершает стандартный низкозатратный прыжок по поверхности земли.

**Параметры:** Отсутствуют (кроме self).

**Изменяет:** 
  - distance
  - strength


**Исключения:**

InvalidLocationError

  - **Условие:** транспорт находится под землей (location_state == "underground").

  - **Текст ошибки:** "Прыжок невозможен: транспорт находится под землей."

NotEnoughStrengthError

  - **Условие:** текущий запас силы (strength) меньше, чем требуется для прыжка с учетом массы ( 3.0 + (self.mass_kg / 100) )

  - **Текст ошибки:** "Не достаточно силы для выполнения обычного прыжка."

**Правила:**
  - Доступно для выполнения только на поверхности (location_state == "surface").

  - Увеличивает distance на фиксированное значение короткого прыжка (на 10.0 метров)

  - Уменьшает запас силы (strength) на фиксированную величину ( 3.0 + (self.mass_kg / 100) ).

  - Энергия реактора (reactor_energy) не расходуется и остается неизменной.

  - После увеличения дистанции проверяет пересечение новой контрольной отметки в 100 метров и при необходимости вызывает метод пассивного восстановления (_apply_distance_recovery).

#### 3.4.2. long_jump
```python
def long_jump(self, use_reactor: bool = False) -> None:
```
**Назначение:** Совершает дальний прыжок на поверхности земли с возможностью форсажа с помощью реактора.

**Параметры:** use_reactor — флаг использования реактивного ускорителя (тип bool, по умолчанию False).

**Изменяет:**
  - distance
  - strength
  - reactor_energy (только если use_reactor == True)

**Исключения:**

InvalidLocationError

  - **Условие:** транспорт находится под землей (location_state == "underground").

  - **Текст ошибки:** "Дальний прыжок невозможен: транспорт находится под землей."

NotEnoughStrengthError

  - **Условие:** текущий запас силы (strength) меньше, чем требуется для прыжка с учетом массы (10.0 + (self.mass_kg / 100.0) * 2.0).

  - **Текст ошибки:** "Недостаточно силы для выполнения дальнего прыжка."

NotEnoughEnergyError

  - **Условие:** передан аргумент use_reactor=True, но текущий запас энергии реактора (reactor_energy) меньше 50.0 единиц.

  - **Текст ошибки:** "Недостаточно энергии реактора для форсажа (требуется 50.0)."

**Правила:**
  - Доступно для выполнения только на поверхности (location_state == "surface").

  - Уменьшает запас силы (strength) по формуле: 10.0 + (mass_kg / 100.0) * 2.0.

  - Если use_reactor == False:
    - Увеличивает distance на базовые 30.0 метров.
    - Энергия реактора (reactor_energy) не расходуется.

  - Если use_reactor == True:
    - Увеличивает distance на 45.0 метров (базовые 30.0 метров плюс 50%).
    - Уменьшает reactor_energy на 50.0 единиц (50% от максимального заряда).

  - После увеличения дистанции (независимо от значения use_reactor) проверяет пересечение новой контрольной отметки в 100 метров и при необходимости вызывает метод пассивного восстановления (_apply_distance_recovery).

### 3.4.3. _apply_distance_recovery
```python
def _apply_distance_recovery(self) -> None:
```
**Назначение:** Проверяет достижение контрольных отметок дистанции (каждые 100 метров) и выполняет пассивное восстановление силы транспорта и энергии реактора с учетом массы.

**Параметры:** Отсутствуют (кроме self).

**Изменяет:**
  - strength
  - reactor_energy

**Исключения:** Отсутствуют.

**Правила:**
  - Срабатывает автоматически при пересечении каждой новой отметки в 100 метров общей дистанции (distance).

  - Увеличивает запас силы (strength) по формуле: 45.0 - (self.mass_kg / 10) * 0.5 

  - Увеличивает энергию реактора (reactor_energy) по аналогичной формуле: 45.0 - (self.mass_kg / 10) * 0.5.

  -  Значения strength и reactor_energy не могут превышать максимальное значение в 100.0 единиц.

  - Вызывается действиями, изменяющими дистанцию (basic_jump, long_jump, drill_forward), при пересечении новой отметки в 100 метров.

#### 3.4.4. get_current_status
```python
def get_current_status(self) -> dict:
```
**Назначение:** Выводит текущее состояние транспорта в консоль и возвращает словарь с ключевыми характеристиками для последующей валидации или интеграции с Pydantic.

**Параметры:** Отсутствуют (кроме self).

**Изменяет:** Отсутствуют (метод работает только на чтение).

**Исключения:** Отсутствуют.

**Правила:**
  - Формирует словарь с текущими значениями distance, strength, reactor_energy и location_state.
  - Выводит её в консоль с помощью print().
  - Возвращает словарь с ключами "distance", "strength", "reactor_energy" (актуальные числовые значения float) и "location_state" (текущее положение "surface" или "underground").

#### 3.4.5. go_underground
```python
def go_underground(self) -> None:
```
**Назначение:** Переводит транспорт в подземный режим работы (погружение под землю).

**Параметры:** Отсутствуют (кроме self).

**Изменяет:**
  - location_state (меняет значение с "surface" на "underground")
  - strength

**Исключения:**

InvalidLocationError

  - **Условие:** транспорт уже находится под землей (location_state == "underground").

  - **Текст ошибки:** "Транспорт уже находится под землей."

NotEnoughStrengthError

  - **Условие:** текущий запас силы (strength) меньше, чем требуется для погружения (3.0 * (self.mass_kg / 100.0)).

  - **Текст ошибки:** "Недостаточно силы для погружения под землю."

**Правила:**
  - Доступно для выполнения только с поверхности (location_state == "surface").

  - Уменьшает запас силы (strength) по формуле: 3.0 * (self.mass_kg / 100.0) 

  - Дистанция (distance) и энергия реактора (reactor_energy) остаются неизменными.

  - Успешно меняет состояние локации на "underground".

#### 3.4.6. return_to_surface
```python
def return_to_surface(self) -> None:
```
**Назначение:** Возвращает транспорт обратно на поверхность земли из подземного режима.

**Параметры:** Отсутствуют (кроме self).

**Изменяет:**
  - location_state (меняет значение с "underground" на "surface")
  - strength

**Исключения:**

InvalidLocationError

  - **Условие:** транспорт уже находится на поверхности (location_state == "surface").

  - **Текст ошибки:** "Транспорт уже находится на поверхности."

NotEnoughStrengthError

  - **Условие:** текущий запас силы (strength) меньше, чем требуется для подъема (3.0 * (self.mass_kg / 100.0)).

  - **Текст ошибки:** "Недостаточно силы для возвращения на поверхность."

**Правила:**
  - Доступно для выполнения только из подземелья (location_state == "underground").

  - Уменьшает запас силы (strength) по формуле: 3.0 * (self.mass_kg / 100.0).

  - Дистанция (distance) и энергия реактора (reactor_energy) остаются неизменными.

  - Успешно меняет состояние локации на "surface".

#### 3.4.7. drill_forward
```python
def drill_forward(self) -> None:
```
**Назначение:** Выполняет подземный рывок (бурение) вперед, преодолевая 40 метров пути

**Параметры:** Отсутствуют (кроме self).

**Изменяет:**
  - distance
  - strength
  - reactor_energy

**Исключения:**

InvalidLocationError

  - **Условие:** транспорт находится на поверхности (location_state == "surface").

  - **Текст ошибки:** "Подземное бурение невозможно на поверхности. Сначала погрузитесь."

NotEnoughStrengthError

  - **Условие:** текущий запас силы (strength) меньше, чем требуется для бурения (10.0 + (self.mass_kg / 100.0) * 3.0).

  - **Текст ошибки:** "Недостаточно силы для подземного бурения."

NotEnoughEnergyError

  - **Условие:** текущая энергия реактора (reactor_energy) меньше 50.0 единиц.

  - **Текст ошибки:** "Недостаточно энергии реактора для запуска буров (требуется 50.0)."

**Правила:**
  - Доступно для выполнения только под землей (location_state == "underground").

  - Увеличивает общую дистанцию (distance) ровно на 40.0 метров.

  - Уменьшает запас силы (strength) по формуле: 10.0 + (self.mass_kg / 100.0) * 3.0 .

  -  Расходует 50.0 единиц энергии реактора (reactor_energy)

  - Автоматически проверяет и вызывает метод пассивного восстановления (_apply_distance_recovery), если общая дистанция перешагнула очередную отметку в 100 метров.

# 4. Модель водителя (Менеджер транспорта с защитой состояния)

### 4.1. Класс и назначение

- Класс: Driver
- Модуль: driver.py
- Тип модели: Контроллер-менеджер. Управляет жизненным циклом и командами транспорта через внутреннюю ссылку.

### 4.2. Конструктор и атрибуты

Конструктор __init__:
  - Создает объект водителя без привязанного транспорта.
  - Атрибут terra_hopper инициализируется со значением None.

### 4.3. Управляющие методы

#### 4.3.1. create_hopper (Создание транспорта)
**Назначение:** Создает экземпляр TerraHopper и привязывает его к текущему водителю.

**Параметры:** name, mass_kg, strength (опционально), reactor_energy (опционально).

**Поведение:** Инициализирует объект транспорта и сохраняет его в self.terra_hopper.

#### 4.3.2. Методы-действия (basic_jump, long_jump, go_underground, return_to_surface, drill_forward)
**Назначение:** Делегируют команды физического перемещения и изменения состояния управляемому транспорту.

**Общее правило:**
  - **Проверка:** Если self.terra_hopper is None, метод должен выбросить исключение NoTransportError с текстом: "Транспорт не выбран. Сначала создайте транспорт!"

  - Если транспорт существует, метод вызывает соответствующий метод у self.terra_hopper и возвращает None.

#### 4.3.3. Методы-запросы (get_current_status)
**Назначение:** Запрашивают и возвращают актуальные данные от управляемого транспорта.

**Общее правило:**
  - **Проверка:** Если self.terra_hopper is None, метод должен выбросить исключение NoTransportError с текстом: "Транспорт не выбран. Сначала создайте транспорт!"

  - Если транспорт существует, метод вызывает соответствующий метод у self.terra_hopper и возвращает полученный результат пользователю.

# 5. Сценарии

## 5.1 Модульные тесты

Каждый тест следует шаблону **AAA (Arrange – Act – Assert)**:

1. **Arrange** — атрибуты, с которыми создается объект (значения по умолчанию не перечисляются).
2. **Act** — одно целевое действие (конструктор или метод).
3. **Assert** — ожидаемые значения атрибутов либо исключение и его текст.


### 5.1.1. Позитивные сценарии

#### Конструктор TerraHopper

##### Сценарий 1. Инициализация с параметрами по умолчанию

* **Arrange:** name="Крот-1", mass_kg=200.0
* **Act:** `TerraHopper(name, mass_kg)`
* **Assert:** `name == "Крот-1"`, `mass_kg == 200.0`, `strength == 100.0`, `reactor_energy == 100.0`, `location_state == "surface"`, `distance == 0.0`

##### Сценарий 2. Инициализация со всеми параметрами

* **Arrange:** name="Крот-1", mass_kg=350.0, strength=80.0, reactor_energy=60.0
* **Act:** `TerraHopper(name, mass_kg, strength, reactor_energy)`
* **Assert:** `name == "Крот-1"`, `mass_kg == 350.0`, `strength == 80.0`, `reactor_energy == 60.0`, `location_state == "surface"`, `distance == 0.0`

```python
basic_jump
```

##### Сценарий 3. Успешный прыжок с поверхности

* **Arrange:** name="Крот-1", mass_kg=200.0, strength=100.0, reactor_energy=100.0, location_state="surface", distance=0.0
* **Act:** `basic_jump()`
* **Assert:** `distance == 10.0`, `strength == 95.0`, `reactor_energy == 100.0`, `location_state == "surface"`

##### Сценарий 4. Сила ровно равна требуемой (5.0)

* **Arrange:** name="Крот-1", mass_kg=200.0, strength=5.0, location_state="surface", distance=0.0
* **Act:** `basic_jump()`
* **Assert:** `distance == 10.0`, `strength == 0.0`, `location_state == "surface"`

```python
long_jump
```

##### Сценарий 5. Успешный прыжок без реактора

* **Arrange:** name="Крот-1", mass_kg=200.0, strength=100.0, reactor_energy=100.0, location_state="surface", distance=0.0
* **Act:** `long_jump(use_reactor=False)`
* **Assert:** `distance == 30.0`, `strength == 86.0`, `reactor_energy == 100.0`

##### Сценарий 6. Успешный прыжок с форсажем

* **Arrange:** name="Крот-1", mass_kg=200.0, strength=100.0, reactor_energy=100.0, location_state="surface", distance=0.0
* **Act:** `long_jump(use_reactor=True)`
* **Assert:** `distance == 45.0`, `strength == 86.0`, `reactor_energy == 50.0`

##### Сценарий 7. Энергия реактора ровно 50.0 при форсаже

* **Arrange:** name="Крот-1", mass_kg=200.0, strength=100.0, reactor_energy=50.0, location_state="surface", distance=0.0
* **Act:** `long_jump(use_reactor=True)`
* **Assert:** `distance == 45.0`, `strength == 86.0`, `reactor_energy == 0.0`

```python
_apply_distance_recovery
```

##### Сценарий 8. Восстановление при пересечении отметки 100 м

* **Arrange:** name="Крот-1", mass_kg=200.0, strength=50.0, reactor_energy=50.0, distance=100.0
* **Act:** `_apply_distance_recovery()`
* **Assert:** `distance == 100.0`, `strength == 85.0`, `reactor_energy == 85.0`

##### Сценарий 9. Ограничение восстановления значением 100.0

* **Arrange:** name="Крот-1", mass_kg=200.0, strength=90.0, reactor_energy=95.0, distance=100.0
* **Act:** `_apply_distance_recovery()`
* **Assert:** `distance == 100.0`, `strength == 100.0`, `reactor_energy == 100.0`

```python
get_current_status
```

##### Сценарий 10. Возврат словаря состояния

* **Arrange:** name="Крот-1", mass_kg=200.0, strength=80.0, reactor_energy=90.0, location_state="surface", distance=20.0
* **Act:** `get_current_status()`
* **Assert:** возвращается `{"distance": 20.0, "strength": 80.0, "reactor_energy": 90.0, "location_state": "surface"}`; `distance == 20.0`, `strength == 80.0`, `reactor_energy == 90.0`

```python
go_underground
```

##### Сценарий 11. Успешное погружение с поверхности

* **Arrange:** name="Крот-1", mass_kg=200.0, strength=100.0, reactor_energy=100.0, location_state="surface", distance=0.0
* **Act:** `go_underground()`
* **Assert:** `location_state == "underground"`, `strength == 94.0`, `distance == 0.0`, `reactor_energy == 100.0`

```python
return_to_surface
```

##### Сценарий 12. Успешный подъем из подземелья

* **Arrange:** name="Крот-1", mass_kg=200.0, strength=100.0, reactor_energy=100.0, location_state="underground", distance=0.0
* **Act:** `return_to_surface()`
* **Assert:** `location_state == "surface"`, `strength == 94.0`, `distance == 0.0`, `reactor_energy == 100.0`

```python
drill_forward
```

##### Сценарий 13. Успешный подземный рывок

* **Arrange:** name="Крот-1", mass_kg=200.0, strength=100.0, reactor_energy=100.0, location_state="underground", distance=0.0
* **Act:** `drill_forward()`
* **Assert:** `distance == 40.0`, `strength == 84.0`, `reactor_energy == 50.0`

#### Driver

##### Сценарий 14. Инициализация водителя без транспорта

* **Arrange:** —
* **Act:** `Driver()`
* **Assert:** `terra_hopper is None`

##### Сценарий 15. Создание транспорта с параметрами по умолчанию

* **Arrange:** name="Крот-1", mass_kg=200.0
* **Act:** `driver.create_hopper(name, mass_kg)`
* **Assert:** `driver.terra_hopper` — экземпляр `TerraHopper`; `name == "Крот-1"`, `strength == 100.0`, `reactor_energy == 100.0`

##### Сценарий 16. Создание транспорта со всеми параметрами

* **Arrange:** name="Крот-1", mass_kg=350.0, strength=80.0, reactor_energy=60.0
* **Act:** `driver.create_hopper(name, mass_kg, strength, reactor_energy)`
* **Assert:** `mass_kg == 350.0`, `strength == 80.0`, `reactor_energy == 60.0`

##### Сценарий 17. Делегирование `basic_jump`

* **Arrange:** name="Крот-1", mass_kg=200.0, strength=100.0, location_state="surface", distance=0.0
* **Act:** `driver.basic_jump()`
* **Assert:** `distance == 10.0`, `strength == 95.0`

##### Сценарий 18. Делегирование `long_jump` с форсажем

* **Arrange:** name="Крот-1", mass_kg=200.0, strength=100.0, reactor_energy=100.0, location_state="surface", distance=0.0
* **Act:** `driver.long_jump(use_reactor=True)`
* **Assert:** `distance == 45.0`, `strength == 86.0`, `reactor_energy == 50.0`

##### Сценарий 19. Делегирование `drill_forward`

* **Arrange:** name="Крот-1", mass_kg=200.0, strength=100.0, reactor_energy=100.0, location_state="underground", distance=0.0
* **Act:** `driver.drill_forward()`
* **Assert:** `distance == 40.0`, `strength == 84.0`, `reactor_energy == 50.0`

##### Сценарий 20. Делегирование `get_current_status`

* **Arrange:** name="Крот-1", mass_kg=200.0, strength=80.0, reactor_energy=90.0, location_state="surface", distance=20.0
* **Act:** `driver.get_current_status()`
* **Assert:** возвращается `{"distance": 20.0, "strength": 80.0, "reactor_energy": 90.0}`

### 5.1.2. Негативные сценарии

#### Конструктор TerraHopper

##### Сценарий 21. Пустое имя

* **Arrange:** name="", mass_kg=200.0
* **Act:** `TerraHopper(name, mass_kg)`
* **Assert:** `ValueError` — "Имя не может быть пустым."

##### Сценарий 21б. Имя из пробелов

* **Arrange:** name="   ", mass_kg=200.0
* **Act:** `TerraHopper(name, mass_kg)`
* **Assert:** `ValueError` — "Имя не может быть пустым."

##### Сценарий 22. Масса меньше 100.0

* **Arrange:** name="Крот-1", mass_kg=90.0
* **Act:** `TerraHopper(name, mass_kg)`
* **Assert:** `ValueError` — "Масса должна быть в диапазоне 100.0…500.0 кг."

##### Сценарий 23. Масса больше 500.0

* **Arrange:** name="Крот-1", mass_kg=550.0
* **Act:** `TerraHopper(name, mass_kg)`
* **Assert:** `ValueError` — "Масса должна быть в диапазоне 100.0…500.0 кг."

##### Сценарий 24. `strength` больше 100.0

* **Arrange:** name="Крот-1", mass_kg=200.0, strength=110.0
* **Act:** `TerraHopper(name, mass_kg, strength)`
* **Assert:** `ValueError` — "Сила должна быть в диапазоне 0…100."

##### Сценарий 25. `reactor_energy` меньше 0.0

* **Arrange:** name="Крот-1", mass_kg=200.0, reactor_energy=-10.0
* **Act:** `TerraHopper(name, mass_kg, reactor_energy=reactor_energy)`
* **Assert:** `ValueError` — "Энергия реактора должна быть в диапазоне 0…100."

```python
basic_jump
```

##### Сценарий 26. Прыжок под землей

* **Arrange:** name="Крот-1", mass_kg=200.0, strength=100.0, location_state="underground", distance=0.0
* **Act:** `basic_jump()`
* **Assert:** `InvalidLocationError` — "Прыжок невозможен: транспорт находится под землей."; `distance == 0.0`, `strength == 100.0`

##### Сценарий 27. Нехватка силы

* **Arrange:** name="Крот-1", mass_kg=200.0, strength=3.0, location_state="surface", distance=0.0
* **Act:** `basic_jump()`
* **Assert:** `NotEnoughStrengthError` — "Не достаточно силы для выполнения обычного прыжка."; `distance == 0.0`, `strength == 3.0`

```python
long_jump
```

##### Сценарий 28. Прыжок под землей

* **Arrange:** name="Крот-1", mass_kg=200.0, strength=100.0, location_state="underground", distance=0.0
* **Act:** `long_jump()`
* **Assert:** `InvalidLocationError` — "Дальний прыжок невозможен: транспорт находится под землей."; `distance == 0.0`, `strength == 100.0`

##### Сценарий 29. Нехватка силы

* **Arrange:** name="Крот-1", mass_kg=200.0, strength=10.0, location_state="surface", distance=0.0
* **Act:** `long_jump()`
* **Assert:** `NotEnoughStrengthError` — "Недостаточно силы для выполнения дальнего прыжка."; `distance == 0.0`, `strength == 10.0`

##### Сценарий 30. Форсаж при нехватке энергии реактора

* **Arrange:** name="Крот-1", mass_kg=200.0, strength=100.0, reactor_energy=30.0, location_state="surface", distance=0.0
* **Act:** `long_jump(use_reactor=True)`
* **Assert:** `NotEnoughEnergyError` — "Недостаточно энергии реактора для форсажа (требуется 50.0)."; `distance == 0.0`, `strength == 100.0`, `reactor_energy == 30.0`

```python
_apply_distance_recovery
```

##### Сценарий 31. Восстановление не срабатывает до отметки 100 м

* **Arrange:** name="Крот-1", mass_kg=200.0, strength=50.0, reactor_energy=50.0, distance=50.0
* **Act:** `_apply_distance_recovery()`
* **Assert:** `distance == 50.0`, `strength == 50.0`, `reactor_energy == 50.0`


##### Сценарий 32. Повторное погружение

* **Arrange:** name="Крот-1", mass_kg=200.0, strength=100.0, location_state="underground", distance=0.0
* **Act:** `go_underground()`
* **Assert:** `InvalidLocationError` — "Транспорт уже находится под землей."; `location_state == "underground"`, `strength == 100.0`

##### Сценарий 33. Нехватка силы

* **Arrange:** name="Крот-1", mass_kg=200.0, strength=5.0, location_state="surface", distance=0.0
* **Act:** `go_underground()`
* **Assert:** `NotEnoughStrengthError` — "Недостаточно силы для погружения под землю."; `location_state == "surface"`, `strength == 5.0`

```python
return_to_surface
```

##### Сценарий 34. Подъем с поверхности

* **Arrange:** name="Крот-1", mass_kg=200.0, strength=100.0, location_state="surface", distance=0.0
* **Act:** `return_to_surface()`
* **Assert:** `InvalidLocationError` — "Транспорт уже находится на поверхности."; `location_state == "surface"`, `strength == 100.0`

##### Сценарий 35. Нехватка силы

* **Arrange:** name="Крот-1", mass_kg=200.0, strength=5.0, location_state="underground", distance=0.0
* **Act:** `return_to_surface()`
* **Assert:** `NotEnoughStrengthError` — "Недостаточно силы для возвращения на поверхность."; `location_state == "underground"`, `strength == 5.0`

```python
drill_forward
```

##### Сценарий 36. Бурение на поверхности

* **Arrange:** name="Крот-1", mass_kg=200.0, strength=100.0, reactor_energy=100.0, location_state="surface", distance=0.0
* **Act:** `drill_forward()`
* **Assert:** `InvalidLocationError` — "Подземное бурение невозможно на поверхности. Сначала погрузитесь."; `distance == 0.0`, `strength == 100.0`, `reactor_energy == 100.0`

##### Сценарий 37. Нехватка силы

* **Arrange:** name="Крот-1", mass_kg=200.0, strength=10.0, reactor_energy=100.0, location_state="underground", distance=0.0
* **Act:** `drill_forward()`
* **Assert:** `NotEnoughStrengthError` — "Недостаточно силы для подземного бурения."; `distance == 0.0`, `strength == 10.0`, `reactor_energy == 100.0`

##### Сценарий 38. Нехватка энергии реактора

* **Arrange:** name="Крот-1", mass_kg=200.0, strength=100.0, reactor_energy=40.0, location_state="underground", distance=0.0
* **Act:** `drill_forward()`
* **Assert:** `NotEnoughEnergyError` — "Недостаточно энергии реактора для запуска буров (требуется 50.0)."; `distance == 0.0`, `strength == 100.0`, `reactor_energy == 40.0`

#### Driver

##### Сценарий 39. `basic_jump` без транспорта

* **Arrange:** terra_hopper=None
* **Act:** `driver.basic_jump()`
* **Assert:** `NoTransportError` — "Транспорт не выбран. Сначала создайте транспорт!"; то же поведение для `long_jump`, `go_underground`, `return_to_surface`, `drill_forward`

##### Сценарий 40. `get_current_status` без транспорта

* **Arrange:** terra_hopper=None
* **Act:** `driver.get_current_status()`
* **Assert:** `NoTransportError` — "Транспорт не выбран. Сначала создайте транспорт!"

## 5.2 Функциональные тесты

Каждый тест следует шаблону **Given – When – Then**:

1. **Given (дано)** — начальное состояние мира.
2. **When (когда)** — действие или событие.
3. **Then (тогда)** — ожидаемый результат.

Всего 8 функциональных тестов (20% от числа модульных). Сценарии выполняются через публичный интерфейс `Driver`; перед проверкой состояния вызывается `get_current_status()` и сверяется весь возвращаемый словарь (distance, strength, reactor_energy, location_state).

#### Маршрут по поверхности

##### Сценарий 41. Два последовательных прыжка

* **Given:** водитель создал транспорт: name="Крот-1", mass_kg=200.0
* **When:**
  - `driver.basic_jump()`
  - `driver.long_jump()`
  - `driver.get_current_status()`
* **Then:**
  - `distance == 40.0`
  - `strength == 81.0`
  - `reactor_energy == 100.0`
  - `location_state == "surface"`

#### Два прыжка с форсажем

##### Сценарий 42. Два последовательных прыжка с использованием реактора

* **Given:** водитель создал транспорт: name="Крот-1", mass_kg=200.0
* **When:**
  - `driver.long_jump(use_reactor=True)`
  - `driver.long_jump(use_reactor=True)`
  - `driver.get_current_status()`
* **Then:**
  - `distance == 90.0`
  - `strength == 72.0`
  - `reactor_energy == 0.0`
  - `location_state == "surface"`

#### Прыжок с реактором без энергии

##### Сценарий 43. Третий прыжок с использованием реактора без энергии

* **Given:** водитель создал транспорт: name="Крот-1", mass_kg=200.0
* **When:**
  - `driver.long_jump(use_reactor=True)`
  - `driver.long_jump(use_reactor=True)`
  - `driver.long_jump(use_reactor=True)`
* **Then:**
  - `NotEnoughEnergyError` — "Недостаточно энергии реактора для форсажа (требуется 50.0)."
  - состояние не изменилось: `distance == 90.0`, `strength == 72.0`, `reactor_energy == 0.0`, `location_state == "surface"`

#### Истощение силы

##### Сценарий 44. Прыжок при исчерпанной силе

* **Given:** водитель создал транспорт: name="Крот-1", mass_kg=200.0
* **When:**
  - `driver.go_underground()`
  - `driver.return_to_surface()`
  - `driver.go_underground()`
  - `driver.return_to_surface()`
  - `driver.go_underground()`
  - `driver.return_to_surface()`
  - `driver.go_underground()`
  - `driver.return_to_surface()`
  - `driver.long_jump()`
  - `driver.long_jump()`
  - `driver.long_jump()`
  - `driver.long_jump()`
* **Then:**
  - `NotEnoughStrengthError` — "Недостаточно силы для выполнения дальнего прыжка."
  - перед падением: `strength == 10.0`, `distance == 90.0`, `location_state == "surface"`

#### Полный цикл под землей

##### Сценарий 45. Погружение, бурение и возврат на поверхность

* **Given:** водитель создал транспорт: name="Крот-1", mass_kg=200.0
* **When:**
  - `driver.go_underground()`
  - `driver.drill_forward()`
  - `driver.return_to_surface()`
  - `driver.get_current_status()`
* **Then:**
  - `distance == 40.0`
  - `strength == 72.0`
  - `reactor_energy == 50.0`
  - `location_state == "surface"`

#### Преодоление отметки 100 м на поверхности

##### Сценарий 46. Пассивное восстановление после прыжка на поверхности

* **Given:** водитель создал транспорт: name="Крот-1", mass_kg=200.0
* **When:**
  - `driver.go_underground()`
  - `driver.drill_forward()`
  - `driver.return_to_surface()`
  - `driver.long_jump()`
  - `driver.basic_jump()`
  - `driver.get_current_status()`
* **Then:**
  - `distance == 80.0`
  - `strength == 53.0`
  - `reactor_energy == 50.0`
  - `location_state == "surface"`

* **When:**
  - `driver.long_jump()`
  - `driver.get_current_status()`
* **Then:**
  - `distance == 110.0`
  - `strength == 74.0`
  - `reactor_energy == 85.0`
  - `location_state == "surface"`

#### Преодоление отметки 100 м под землёй

##### Сценарий 47. Пассивное восстановление после бурения под землёй

* **Given:** водитель создал транспорт: name="Крот-1", mass_kg=200.0
* **When:**
  - `driver.go_underground()`
  - `driver.drill_forward()`
  - `driver.return_to_surface()`
  - `driver.basic_jump()`
  - `driver.long_jump()`
  - `driver.go_underground()`
  - `driver.get_current_status()`
* **Then:**
  - `distance == 80.0`
  - `strength == 47.0`
  - `reactor_energy == 50.0`
  - `location_state == "underground"`

* **When:**
  - `driver.drill_forward()`
  - `driver.get_current_status()`
* **Then:**
  - `distance == 120.0`
  - `strength == 66.0`
  - `reactor_energy == 35.0`
  - `location_state == "underground"`

#### Восстановление на поверхности и под землёй

##### Сценарий 48. Пересечение отметок 100 м (поверхность) и 200 м (под землёй)

* **Given:** водитель создал транспорт: name="Крот-1", mass_kg=200.0
* **When:**
  - `driver.basic_jump()`
  - `driver.long_jump()`
  - `driver.long_jump()`
  - `driver.basic_jump()`
  - `driver.long_jump()`
  - `driver.long_jump()`
  - `driver.long_jump()`
  - `driver.go_underground()`
  - `driver.drill_forward()`
  - `driver.get_current_status()`
* **Then:**
  - `distance == 210.0`
  - `strength == 68.0`
  - `reactor_energy == 85.0`
  - `location_state == "underground"`

# 6. Исключения и иерархия

Ошибки, связанные с параметрами, — стандартное исключение `ValueError`. Ошибки, связанные с состоянием транспорта и правилами домена, — доменные исключения с общим корнем `TerraHopperError`.

## 6.1. Иерархия

```
Exception
├── ValueError                    # параметры (стандартное)
└── TerraHopperError              # домен
    ├── NoTransportError
    ├── InvalidLocationError
    ├── NotEnoughStrengthError
    └── NotEnoughEnergyError
```

## 6.2. Таблица

| Ситуация | Исключение | Сообщение |
|---|---|---|
| Пустое имя (конструктор) | ValueError | "Имя не может быть пустым." |
| mass_kg вне диапазона 100.0…500.0 | ValueError | "Масса должна быть в диапазоне 100.0…500.0 кг." |
| strength вне диапазона 0…100 | ValueError | "Сила должна быть в диапазоне 0…100." |
| reactor_energy вне диапазона 0…100 | ValueError | "Энергия реактора должна быть в диапазоне 0…100." |
| Водителю не назначен транспорт | NoTransportError | "Транспорт не выбран. Сначала создайте транспорт!" |
| Прыжок под землёй (`basic_jump`) | InvalidLocationError | "Прыжок невозможен: транспорт находится под землей." |
| Дальний прыжок под землёй (`long_jump`) | InvalidLocationError | "Дальний прыжок невозможен: транспорт находится под землей." |
| Повторное погружение (`go_underground`) | InvalidLocationError | "Транспорт уже находится под землей." |
| Возврат уже на поверхности (`return_to_surface`) | InvalidLocationError | "Транспорт уже находится на поверхности." |
| Бурение на поверхности (`drill_forward`) | InvalidLocationError | "Подземное бурение невозможно на поверхности. Сначала погрузитесь." |
| Нехватка силы для обычного прыжка (`basic_jump`) | NotEnoughStrengthError | "Не достаточно силы для выполнения обычного прыжка." |
| Нехватка силы для дальнего прыжка (`long_jump`) | NotEnoughStrengthError | "Недостаточно силы для выполнения дальнего прыжка." |
| Нехватка силы для погружения (`go_underground`) | NotEnoughStrengthError | "Недостаточно силы для погружения под землю." |
| Нехватка силы для возврата (`return_to_surface`) | NotEnoughStrengthError | "Недостаточно силы для возвращения на поверхность." |
| Нехватка силы для бурения (`drill_forward`) | NotEnoughStrengthError | "Недостаточно силы для подземного бурения." |
| Нехватка энергии для форсажа (`long_jump(use_reactor=True)`) | NotEnoughEnergyError | "Недостаточно энергии реактора для форсажа (требуется 50.0)." |
| Нехватка энергии для бурения (`drill_forward`) | NotEnoughEnergyError | "Недостаточно энергии реактора для запуска буров (требуется 50.0)." |

# 7. Что вне рамок

- Транспорт не размножается.
- Транспорт не взаимодействует с другими транспортами.
- Нет сохранения состояния между запусками.
- Нет учёта рельефа, препятствий и коллизий.

# 8. Трассируемость «требование → тест»

| Требование | Раздел ТЗ | Тест (TC ID) |
|---|---|---|
| Инициализация параметрами по умолчанию | 3.2 | `test_p1_init_with_defaults` (TC_P_1) |
| Инициализация всеми параметрами | 3.2 | `test_p2_init_with_all_parameters` (TC_P_2) |
| Валидация пустого имени и имени из пробелов | 3.2 | `test_n21_init_empty_name_raises`, `test_n21b_init_whitespace_name_raises` (TC_N_21) |
| Валидация массы | 3.2 | `test_n22_init_mass_below_min_raises`, `test_n23_init_mass_above_max_raises` (TC_N_22, TC_N_23) |
| Валидация силы | 3.2 | `test_n24_init_strength_above_max_raises` (TC_N_24) |
| Валидация энергии реактора | 3.2 | `test_n25_init_reactor_energy_below_min_raises` (TC_N_25) |
| Обычный прыжок на поверхности | 3.4.1 | `test_p3_basic_jump_updates_state`, `test_p4_basic_jump_strength_exactly_required` (TC_P_3, TC_P_4) |
| Запрет обычного прыжка | 3.4.1 | `test_n26_basic_jump_underground_raises`, `test_n27_basic_jump_not_enough_strength_raises` (TC_N_26, TC_N_27) |
| Дальний прыжок и форсаж | 3.4.2 | `test_p5_long_jump_without_reactor`, `test_p6_long_jump_with_reactor`, `test_p7_long_jump_reactor_energy_exactly_minimum` (TC_P_5–TC_P_7) |
| Запрет дальнего прыжка | 3.4.2 | `test_n28_long_jump_underground_raises`, `test_n29_long_jump_not_enough_strength_raises`, `test_n30_long_jump_not_enough_energy_raises` (TC_N_28–TC_N_30) |
| Пассивное восстановление на отметке 100 м | 3.4.3 | `test_p8_recovery_on_distance_mark`, `test_p9_recovery_capped_at_maximum`, `test_n31_recovery_not_triggered_before_mark` (TC_P_8, TC_P_9, TC_N_31) |
| Статус транспорта | 3.4.4 | `test_p10_status_returns_state_dict`, `test_p20_get_current_status_delegated` (TC_P_10, TC_P_20) |
| Смена локации погружение/возврат | 3.4.5–3.4.6 | `test_p11_go_underground_from_surface`, `test_p12_return_to_surface_from_underground`, `test_n32_go_underground_already_underground_raises`, `test_n33_go_underground_not_enough_strength_raises`, `test_n34_return_to_surface_already_surface_raises`, `test_n35_return_to_surface_not_enough_strength_raises` (TC_P_11, TC_P_12, TC_N_32–TC_N_35) |
| Бурение только под землёй | 3.4.7 | `test_p13_drill_forward_underground`, `test_n36_drill_forward_on_surface_raises`, `test_n37_drill_forward_not_enough_strength_raises`, `test_n38_drill_forward_not_enough_energy_raises` (TC_P_13, TC_N_36–TC_N_38) |
| Водитель: создание транспорта | 4.2–4.3.1 | `test_p14_init_without_transport`, `test_p15_create_hopper_with_defaults`, `test_p16_create_hopper_with_all_parameters` (TC_P_14–TC_P_16) |
| Делегирование действий транспорту | 4.3.2 | `test_p17_basic_jump_delegated`, `test_p18_long_jump_with_reactor_delegated`, `test_p19_drill_forward_delegated` (TC_P_17–TC_P_19) |
| Действие без транспорта | 4.3.2–4.3.3 | `test_n39_actions_without_transport_raise`, `test_n40_get_current_status_without_transport_raises` (TC_N_39, TC_N_40) |
| Сквозные сценарии | 5.2 | `test_s41_two_jumps_on_surface`, `test_s42_two_reactor_jumps`, `test_s43_third_reactor_jump_without_energy_raises`, `test_s44_jump_with_exhausted_strength_raises`, `test_s45_full_underground_cycle`, `test_s46_recovery_after_surface_jump`, `test_s47_recovery_after_underground_drill`, `test_s48_crossing_100m_and_200m_marks` (TC_S_41–TC_S_48) |

Каждая строка разделов 3–6 должна иметь хотя бы один связанный тест.

# 9. Открытые вопросы

- Срабатывает ли восстановление, если за одно действие пересекается сразу несколько отметок по 100 м?
- Какой порядок проверки исключений, если одновременно не хватает силы и энергии?
