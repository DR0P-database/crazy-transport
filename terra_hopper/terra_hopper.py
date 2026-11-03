"""Транспорт «Терра-Хоппер» (SPEC, раздел 3)."""

from .errors import (
    InvalidLocationError,
    NotEnoughEnergyError,
    NotEnoughStrengthError,
)


class TerraHopper:
    """Земляной Кенгуру-Крот с учетом ресурсов и пройденного пути."""

    def __init__(
        self,
        name: str,
        mass_kg: float,
        strength: float = 100.0,
        reactor_energy: float = 100.0,
    ) -> None:
        if not name.strip():
            raise ValueError("Имя не может быть пустым.")
        if not 100.0 <= mass_kg <= 500.0:
            raise ValueError("Масса должна быть в диапазоне 100.0…500.0 кг.")
        if not 0.0 <= strength <= 100.0:
            raise ValueError("Сила должна быть в диапазоне 0…100.")
        if not 0.0 <= reactor_energy <= 100.0:
            raise ValueError("Энергия реактора должна быть в диапазоне 0…100.")
        self._name = name
        self._mass_kg = float(mass_kg)
        self._strength = float(strength)
        self._reactor_energy = float(reactor_energy)
        self.location_state = "surface"
        self.distance = 0.0
        self._recovered_marks = 0

    @property
    def name(self) -> str:
        return self._name

    @property
    def mass_kg(self) -> float:
        return self._mass_kg

    @property
    def strength(self) -> float:
        return self._strength

    @property
    def reactor_energy(self) -> float:
        return self._reactor_energy

    def _check_action(
        self,
        location: str,
        location_message: str,
        strength_cost: float,
        strength_message: str,
        energy_cost: float = 0.0,
        energy_message: str = "",
    ) -> None:
        """Проверяет условия до любых изменений: локация, сила, энергия."""
        if self.location_state != location:
            raise InvalidLocationError(location_message)
        if self.strength < strength_cost:
            raise NotEnoughStrengthError(strength_message)
        if self.reactor_energy < energy_cost:
            raise NotEnoughEnergyError(energy_message)

    def basic_jump(self) -> None:
        cost = 3.0 + self.mass_kg / 100.0
        self._check_action(
            "surface",
            "Прыжок невозможен: транспорт находится под землей.",
            cost,
            "Не достаточно силы для выполнения обычного прыжка.",
        )
        self._strength -= cost
        self.distance += 10.0
        self._apply_distance_recovery()

    def long_jump(self, use_reactor: bool = False) -> None:
        cost = 10.0 + (self.mass_kg / 100.0) * 2.0
        energy_cost = 50.0 if use_reactor else 0.0
        self._check_action(
            "surface",
            "Дальний прыжок невозможен: транспорт находится под землей.",
            cost,
            "Недостаточно силы для выполнения дальнего прыжка.",
            energy_cost,
            "Недостаточно энергии реактора для форсажа (требуется 50.0).",
        )
        self._strength -= cost
        self._reactor_energy -= energy_cost
        self.distance += 45.0 if use_reactor else 30.0
        self._apply_distance_recovery()

    def _apply_distance_recovery(self) -> None:
        """Восстанавливает ресурсы один раз за каждую новую отметку 100 м."""
        marks = int(self.distance // 100.0)
        new_marks = marks - self._recovered_marks
        if new_marks <= 0:
            return
        gain = (45.0 - (self.mass_kg / 10.0) * 0.5) * new_marks
        self._strength = min(100.0, self.strength + gain)
        self._reactor_energy = min(100.0, self.reactor_energy + gain)
        self._recovered_marks = marks

    def get_current_status(self) -> dict:
        status = {
            "distance": self.distance,
            "strength": self.strength,
            "reactor_energy": self.reactor_energy,
            "location_state": self.location_state,
        }
        print(status)
        return status

    def go_underground(self) -> None:
        cost = 3.0 * (self.mass_kg / 100.0)
        self._check_action(
            "surface",
            "Транспорт уже находится под землей.",
            cost,
            "Недостаточно силы для погружения под землю.",
        )
        self._strength -= cost
        self.location_state = "underground"

    def return_to_surface(self) -> None:
        cost = 3.0 * (self.mass_kg / 100.0)
        self._check_action(
            "underground",
            "Транспорт уже находится на поверхности.",
            cost,
            "Недостаточно силы для возвращения на поверхность.",
        )
        self._strength -= cost
        self.location_state = "surface"

    def drill_forward(self) -> None:
        cost = 10.0 + (self.mass_kg / 100.0) * 3.0
        self._check_action(
            "underground",
            "Подземное бурение невозможно на поверхности. Сначала погрузитесь.",
            cost,
            "Недостаточно силы для подземного бурения.",
            50.0,
            "Недостаточно энергии реактора для запуска буров (требуется 50.0).",
        )
        self._strength -= cost
        self._reactor_energy -= 50.0
        self.distance += 40.0
        self._apply_distance_recovery()
