# Test Case Specification — «Терра-Хоппер»

Соглашение об ID:
- `TC_P_{n}` — позитивный модульный сценарий (SPEC 5.1.1);
- `TC_N_{n}` — негативный модульный сценарий (SPEC 5.1.2);
- `TC_S_{n}` — сценарный (функциональный) тест (SPEC 5.2), где `n` — номер сценария из ТЗ.

## Модульные тесты

| ID | Источник | Предусловие | Вход | Ожидание | Приоритет |
|---|---|---|---|---|---|
| TC_P_1 | SPEC 3.2 | — | `TerraHopper(name="Крот-1", mass_kg=200.0)` | `name="Крот-1"`, `mass_kg=200.0`, `strength=100.0`, `reactor_energy=100.0`, `location_state="surface"`, `distance=0.0` | high |
| TC_P_2 | SPEC 3.2 | — | `TerraHopper("Крот-1", 350.0, 80.0, 60.0)` | `name="Крот-1"`, `mass_kg=350.0`, `strength=80.0`, `reactor_energy=60.0`, `location_state="surface"`, `distance=0.0` | medium |
| TC_P_3 | SPEC 3.4.1 | `location_state="surface"`, `strength=100.0`, `reactor_energy=100.0`, `distance=0.0` | `basic_jump()` | `distance=10.0`, `strength=95.0`, `reactor_energy=100.0`, `location_state="surface"` | high |
| TC_P_4 | SPEC 3.4.1 | `location_state="surface"`, `strength=5.0`, `distance=0.0` | `basic_jump()` | `distance=10.0`, `strength=0.0`, `location_state="surface"` | medium |
| TC_P_5 | SPEC 3.4.2 | `location_state="surface"`, `strength=100.0`, `reactor_energy=100.0`, `distance=0.0` | `long_jump(use_reactor=False)` | `distance=30.0`, `strength=86.0`, `reactor_energy=100.0` | high |
| TC_P_6 | SPEC 3.4.2 | `location_state="surface"`, `strength=100.0`, `reactor_energy=100.0`, `distance=0.0` | `long_jump(use_reactor=True)` | `distance=45.0`, `strength=86.0`, `reactor_energy=50.0` | high |
| TC_P_7 | SPEC 3.4.2 | `location_state="surface"`, `strength=100.0`, `reactor_energy=50.0`, `distance=0.0` | `long_jump(use_reactor=True)` | `distance=45.0`, `strength=86.0`, `reactor_energy=0.0` | medium |
| TC_P_8 | SPEC 3.4.3 | `strength=50.0`, `reactor_energy=50.0`, `distance=100.0` | `_apply_distance_recovery()` | `distance=100.0`, `strength=85.0`, `reactor_energy=85.0` | high |
| TC_P_9 | SPEC 3.4.3 | `strength=90.0`, `reactor_energy=95.0`, `distance=100.0` | `_apply_distance_recovery()` | `distance=100.0`, `strength=100.0`, `reactor_energy=100.0` | medium |
| TC_P_10 | SPEC 3.4.4 | `strength=80.0`, `reactor_energy=90.0`, `location_state="surface"`, `distance=20.0` | `get_current_status()` | `{"distance": 20.0, "strength": 80.0, "reactor_energy": 90.0, "location_state": "surface"}` | medium |
| TC_P_11 | SPEC 3.4.5 | `location_state="surface"`, `strength=100.0`, `reactor_energy=100.0`, `distance=0.0` | `go_underground()` | `location_state="underground"`, `strength=94.0`, `distance=0.0`, `reactor_energy=100.0` | high |
| TC_P_12 | SPEC 3.4.6 | `location_state="underground"`, `strength=100.0`, `reactor_energy=100.0`, `distance=0.0` | `return_to_surface()` | `location_state="surface"`, `strength=94.0`, `distance=0.0`, `reactor_energy=100.0` | high |
| TC_P_13 | SPEC 3.4.7 | `location_state="underground"`, `strength=100.0`, `reactor_energy=100.0`, `distance=0.0` | `drill_forward()` | `distance=40.0`, `strength=84.0`, `reactor_energy=50.0` | high |
| TC_P_14 | SPEC 4.2 | — | `Driver()` | `terra_hopper is None` | high |
| TC_P_15 | SPEC 4.3.1 | — | `driver.create_hopper(name="Крот-1", mass_kg=200.0)` | `driver.terra_hopper` — экземпляр `TerraHopper`; `name="Крот-1"`, `strength=100.0`, `reactor_energy=100.0` | high |
| TC_P_16 | SPEC 4.3.1 | — | `driver.create_hopper("Крот-1", 350.0, 80.0, 60.0)` | `mass_kg=350.0`, `strength=80.0`, `reactor_energy=60.0` | medium |
| TC_P_17 | SPEC 4.3.2 | транспорт: `location_state="surface"`, `strength=100.0`, `distance=0.0` | `driver.basic_jump()` | `distance=10.0`, `strength=95.0` | high |
| TC_P_18 | SPEC 4.3.2 | транспорт: `location_state="surface"`, `strength=100.0`, `reactor_energy=100.0`, `distance=0.0` | `driver.long_jump(use_reactor=True)` | `distance=45.0`, `strength=86.0`, `reactor_energy=50.0` | high |
| TC_P_19 | SPEC 4.3.2 | транспорт: `location_state="underground"`, `strength=100.0`, `reactor_energy=100.0`, `distance=0.0` | `driver.drill_forward()` | `distance=40.0`, `strength=84.0`, `reactor_energy=50.0` | high |
| TC_P_20 | SPEC 4.3.3 | транспорт: `strength=80.0`, `reactor_energy=90.0`, `location_state="surface"`, `distance=20.0` | `driver.get_current_status()` | `{"distance": 20.0, "strength": 80.0, "reactor_energy": 90.0, "location_state": "surface"}` | medium |
| TC_N_21 | SPEC 3.2 | — | `TerraHopper(name="", mass_kg=200.0)`; `TerraHopper(name="   ", mass_kg=200.0)` | `ValueError` — "Имя не может быть пустым." | high |
| TC_N_22 | SPEC 3.2 | — | `TerraHopper("Крот-1", mass_kg=90.0)` | `ValueError` — "Масса должна быть в диапазоне 100.0…500.0 кг." | high |
| TC_N_23 | SPEC 3.2 | — | `TerraHopper("Крот-1", mass_kg=550.0)` | `ValueError` — "Масса должна быть в диапазоне 100.0…500.0 кг." | medium |
| TC_N_24 | SPEC 3.2 | — | `TerraHopper("Крот-1", 200.0, strength=110.0)` | `ValueError` — "Сила должна быть в диапазоне 0…100." | medium |
| TC_N_25 | SPEC 3.2 | — | `TerraHopper("Крот-1", 200.0, reactor_energy=-10.0)` | `ValueError` — "Энергия реактора должна быть в диапазоне 0…100." | medium |
| TC_N_26 | SPEC 3.4.1 | `location_state="underground"`, `strength=100.0`, `distance=0.0` | `basic_jump()` | `InvalidLocationError` — "Прыжок невозможен: транспорт находится под землей."; `distance=0.0`, `strength=100.0` | high |
| TC_N_27 | SPEC 3.4.1 | `location_state="surface"`, `strength=3.0`, `distance=0.0` | `basic_jump()` | `NotEnoughStrengthError` — "Не достаточно силы для выполнения обычного прыжка."; `distance=0.0`, `strength=3.0` | high |
| TC_N_28 | SPEC 3.4.2 | `location_state="underground"`, `strength=100.0`, `distance=0.0` | `long_jump()` | `InvalidLocationError` — "Дальний прыжок невозможен: транспорт находится под землей."; `distance=0.0`, `strength=100.0` | high |
| TC_N_29 | SPEC 3.4.2 | `location_state="surface"`, `strength=10.0`, `distance=0.0` | `long_jump()` | `NotEnoughStrengthError` — "Недостаточно силы для выполнения дальнего прыжка."; `distance=0.0`, `strength=10.0` | high |
| TC_N_30 | SPEC 3.4.2 | `location_state="surface"`, `strength=100.0`, `reactor_energy=30.0`, `distance=0.0` | `long_jump(use_reactor=True)` | `NotEnoughEnergyError` — "Недостаточно энергии реактора для форсажа (требуется 50.0)."; `distance=0.0`, `strength=100.0`, `reactor_energy=30.0` | high |
| TC_N_31 | SPEC 3.4.3 | `strength=50.0`, `reactor_energy=50.0`, `distance=50.0` | `_apply_distance_recovery()` | `distance=50.0`, `strength=50.0`, `reactor_energy=50.0` | medium |
| TC_N_32 | SPEC 3.4.5 | `location_state="underground"`, `strength=100.0`, `distance=0.0` | `go_underground()` | `InvalidLocationError` — "Транспорт уже находится под землей."; `location_state="underground"`, `strength=100.0` | high |
| TC_N_33 | SPEC 3.4.5 | `location_state="surface"`, `strength=5.0`, `distance=0.0` | `go_underground()` | `NotEnoughStrengthError` — "Недостаточно силы для погружения под землю."; `location_state="surface"`, `strength=5.0` | medium |
| TC_N_34 | SPEC 3.4.6 | `location_state="surface"`, `strength=100.0`, `distance=0.0` | `return_to_surface()` | `InvalidLocationError` — "Транспорт уже находится на поверхности."; `location_state="surface"`, `strength=100.0` | high |
| TC_N_35 | SPEC 3.4.6 | `location_state="underground"`, `strength=5.0`, `distance=0.0` | `return_to_surface()` | `NotEnoughStrengthError` — "Недостаточно силы для возвращения на поверхность."; `location_state="underground"`, `strength=5.0` | medium |
| TC_N_36 | SPEC 3.4.7 | `location_state="surface"`, `strength=100.0`, `reactor_energy=100.0`, `distance=0.0` | `drill_forward()` | `InvalidLocationError` — "Подземное бурение невозможно на поверхности. Сначала погрузитесь."; `distance=0.0`, `strength=100.0`, `reactor_energy=100.0` | high |
| TC_N_37 | SPEC 3.4.7 | `location_state="underground"`, `strength=10.0`, `reactor_energy=100.0`, `distance=0.0` | `drill_forward()` | `NotEnoughStrengthError` — "Недостаточно силы для подземного бурения."; `distance=0.0`, `strength=10.0`, `reactor_energy=100.0` | high |
| TC_N_38 | SPEC 3.4.7 | `location_state="underground"`, `strength=100.0`, `reactor_energy=40.0`, `distance=0.0` | `drill_forward()` | `NotEnoughEnergyError` — "Недостаточно энергии реактора для запуска буров (требуется 50.0)."; `distance=0.0`, `strength=100.0`, `reactor_energy=40.0` | high |
| TC_N_39 | SPEC 4.3.2 | `terra_hopper=None` | `driver.basic_jump()` (аналогично `long_jump`, `go_underground`, `return_to_surface`, `drill_forward`) | `NoTransportError` — "Транспорт не выбран. Сначала создайте транспорт!" | high |
| TC_N_40 | SPEC 4.3.3 | `terra_hopper=None` | `driver.get_current_status()` | `NoTransportError` — "Транспорт не выбран. Сначала создайте транспорт!" | high |

## Сценарные тесты

Все шаги выполняются через публичный интерфейс `Driver`; перед проверкой состояния вызывается `driver.get_current_status()`.

| ID | Источник | Вход | Ожидание | Приоритет |
|---|---|---|---|---|
| TC_S_41 | SPEC 5.2 | `basic_jump()`, `long_jump()`, `get_current_status()` | `distance=40.0`, `strength=81.0`, `reactor_energy=100.0`, `location_state="surface"` | high |
| TC_S_42 | SPEC 5.2 | `long_jump(use_reactor=True)`, `long_jump(use_reactor=True)`, `get_current_status()` | `distance=90.0`, `strength=72.0`, `reactor_energy=0.0`, `location_state="surface"` | high |
| TC_S_43 | SPEC 5.2 | `long_jump(use_reactor=True)` ×3 | `NotEnoughEnergyError` — "Недостаточно энергии реактора для форсажа (требуется 50.0)." | high |
| TC_S_44 | SPEC 5.2 | шаги 1–8: `go_underground()`/`return_to_surface()` ×4; шаги 9–12: `long_jump()` ×4 | `NotEnoughStrengthError` — "Недостаточно силы для выполнения дальнего прыжка." (перед падением `strength=10.0`, `distance=90.0`, `location_state="surface"`) | medium |
| TC_S_45 | SPEC 5.2 | `go_underground()`, `drill_forward()`, `return_to_surface()`, `get_current_status()` | `distance=40.0`, `strength=72.0`, `reactor_energy=50.0`, `location_state="surface"` | high |
| TC_S_46 | SPEC 5.2 | шаг 1: `go_underground()`, `drill_forward()`, `return_to_surface()`, `long_jump()`, `basic_jump()`, `get_current_status()`; шаг 2: `long_jump()`, `get_current_status()` | шаг 1: `distance=80.0`, `strength=53.0`, `reactor_energy=50.0`, `location_state="surface"`; шаг 2: `distance=110.0`, `strength=74.0`, `reactor_energy=85.0`, `location_state="surface"` | medium |
| TC_S_47 | SPEC 5.2 | шаг 1: `go_underground()`, `drill_forward()`, `return_to_surface()`, `basic_jump()`, `long_jump()`, `go_underground()`, `get_current_status()`; шаг 2: `drill_forward()`, `get_current_status()` | шаг 1: `distance=80.0`, `strength=47.0`, `reactor_energy=50.0`, `location_state="underground"`; шаг 2: `distance=120.0`, `strength=66.0`, `reactor_energy=35.0`, `location_state="underground"` | medium |
| TC_S_48 | SPEC 5.2 | `basic_jump()`, `long_jump()`, `long_jump()`, `basic_jump()`, `long_jump()`, `long_jump()`, `long_jump()`, `go_underground()`, `drill_forward()`, `get_current_status()` | `distance=210.0`, `strength=68.0`, `reactor_energy=85.0`, `location_state="underground"` | medium |
