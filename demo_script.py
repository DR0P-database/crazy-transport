"""Демонстрационный сценарий «Терра-Хоппер».

Показывает весь функционал публичного интерфейса:
каждый шаг снабжается снимками состояния «до → после»,
все исключения стихии перехватываются и поясняются.
"""

import io
from contextlib import redirect_stdout

from terra_hopper import (
    Driver,
    InvalidLocationError,
    NoTransportError,
    NotEnoughEnergyError,
    NotEnoughStrengthError,
)

LINE = "------------------------------------------------------------"


def snapshot(driver: Driver) -> dict:
    """Возвращает словарь состояния через get_current_status().

    Встроенный print() метода глушится, чтобы не шуметь в выводе.
    """
    with redirect_stdout(io.StringIO()):
        return driver.get_current_status()


def format_status(status: dict) -> str:
    location = "под землёй" if status["location_state"] == "underground" else "на поверхности"
    return (
        f"дистанция {status['distance']:.1f} м | {location} | "
        f"сила {status['strength']:.1f} ед. | "
        f"энергия реактора {status['reactor_energy']:.1f} ед."
    )


def section(title: str, driver: Driver = None):
    print(f"\n{LINE}")
    print(f"  {title}")
    print(LINE)
    if driver is not None:
        status = snapshot(driver)
        print(f"   [СТАТУС] {format_status(status)}")


def act(driver: Driver, description: str, action):
    """Выполняет один шаг и печатает состояние «до -> после»."""
    before = snapshot(driver)
    action()
    after = snapshot(driver)
    print(f"\n-> {description}")
    print(f"   было:  {format_status(before)}")
    print(f"   стало: {format_status(after)}")
    return after


def act_expect_error(driver: Driver, description: str, exception_type, action):
    """Выполняет шаг, который должен упасть, и это показываем как норму."""
    before = snapshot(driver)
    try:
        action()
    except exception_type as e:
        print(f"\n-> {description}")
        print(f"   было:   {format_status(before)}")
        print(f"   [ОЖИДАЕМАЯ ОШИБКА {exception_type.__name__}] {e}")
        print(f"   состояние не изменилось (проверка ресурсов идёт до движения)")
    else:
        print(f"\n!!! {description}: ОШИБКИ НЕ БЫЛО, а ожидался {exception_type.__name__}")


def run_demo():
    print("🦘 Демонстрация: Земляной Кенгуру-Крот «Терра-Хоппер»")
    print("Все действия идут через публичный интерфейс Driver, как в ТЗ.")
    print("Масса транспорта 200 кг: стоимость прыжка = 3 + 200/100 = 5 ед.")

    driver = Driver()

    # =================================================================
    section("1. Создание транспорта: name='Крот-1', mass_kg=200")
    driver.create_hopper(name="Крот-1", mass_kg=200.0)
    act(driver, "Транспорт создан и готов к работе", lambda: None)

    # =================================================================
    section("2. Валидация конструктора: некорректные параметры отклоняются")
    act_expect_error(
        driver, "Пытаемся создать транспорт массой 90 кг (диапазон 100–500)", ValueError,
        lambda: driver.create_hopper(name="Крот-1", mass_kg=90.0),
    )
    act_expect_error(
        driver, "Пытаемся создать транспорт с именем из одних пробелов", ValueError,
        lambda: driver.create_hopper(name="   ", mass_kg=200.0),
    )

    # =================================================================
    section("3. Прыжки по поверхности")
    act(driver, "Обычный прыжок: +10 м, -5 ед. силы", driver.basic_jump)
    act(driver, "Дальний прыжок: +30 м, -14 ед. силы, реактор не тратим", driver.long_jump)

    # =================================================================
    section("4. Ограничение стихии: бурить можно только под землёй")
    act_expect_error(
        driver, "Пытаемся бурить прямо на поверхности", InvalidLocationError,
        driver.drill_forward,
    )

    # =================================================================
    section("5. Подземный цикл: погружение -> бурение -> возврат")
    act(driver, "Погружение под землю: -6 ед. силы", driver.go_underground)
    act(
        driver,
        "Бурение вперёд: +40 м, -16 ед. силы, -50 ед. энергии реактора",
        driver.drill_forward,
    )
    act(driver, "Подъём на поверхность: -6 ед. силы", driver.return_to_surface)

    # =================================================================
    section("6. Пассивное восстановление: прыжок пересёк отметку 100 м", driver)
    act(
        driver,
        "Дальний прыжок: +30 м, дистанция 80 -> 110 м, пересечена отметка 100 м",
        driver.long_jump,
    )
    print("   И срабатывает автоматическое восстановление обоих ресурсов: +35 ед.")

    # =================================================================
    section("7. Форсаж реактора: вторая половина дальнего прыжка")
    act(
        driver,
        "Дальний прыжок с форсажем (use_reactor=True): не +30, а +45 м, но реактор отдаёт 50 ед.",
        lambda: driver.long_jump(use_reactor=True),
    )
    act_expect_error(
        driver,
        "Пытаемся снова прыгнуть с форсажем, а в реакторе осталось только 35 ед. (нужно 50)",
        NotEnoughEnergyError,
        lambda: driver.long_jump(use_reactor=True),
    )

    # =================================================================
    section("8. Истощение силы: сила тратится, а восстановление только на 100 м", driver)
    for cycle in range(1, 7):
        try:
            driver.go_underground()
            driver.return_to_surface()
            print(f"-> Цикл \"погружение-подъём\" №{cycle}: -12 ед. силы, транспорт снова сверху")
        except NotEnoughStrengthError as e:
            print(f"-> Цикл №{cycle} прерван: силы на погружение уже не хватает")
            print(f"   [ОЖИДАЕМАЯ ОШИБКА NotEnoughStrengthError] {e}")
            break
    after_cycle = snapshot(driver)
    print(f"   после циклов: {format_status(after_cycle)}")

    act_expect_error(
        driver, "Пытаемся прыгнуть на «пустом баке» (сила 0 из 5 нужных)", NotEnoughStrengthError,
        driver.basic_jump,
    )

    # =================================================================
    section("9. Водитель без транспорта: команды пролетают мимо")
    lazy_driver = Driver()
    try:
        lazy_driver.basic_jump()
    except NoTransportError as e:
        print(f"-> Пытаемся прыгнуть, но водитель ещё не создал транспорт")
        print(f"   [ОЖИДАЕМАЯ ОШИБКА NoTransportError] {e}")

    # =================================================================
    section("Финальное состояние «Крота-1»", driver)
    print("\n🎉 Демонстрация успешно завершена!")


if __name__ == "__main__":
    run_demo()
