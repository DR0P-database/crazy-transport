"""Менеджер транспорта (SPEC, раздел 4)."""

from .errors import NoTransportError
from .terra_hopper import TerraHopper


class Driver:
    """Создает транспорт и делегирует ему команды."""

    def __init__(self) -> None:
        self.terra_hopper: TerraHopper | None = None

    def create_hopper(
        self,
        name: str,
        mass_kg: float,
        strength: float = 100.0,
        reactor_energy: float = 100.0,
    ) -> None:
        self.terra_hopper = TerraHopper(
            name=name,
            mass_kg=mass_kg,
            strength=strength,
            reactor_energy=reactor_energy,
        )

    def _require_hopper(self) -> TerraHopper:
        if self.terra_hopper is None:
            raise NoTransportError(
                "Транспорт не выбран. Сначала создайте транспорт!"
            )
        return self.terra_hopper

    def basic_jump(self) -> None:
        self._require_hopper().basic_jump()

    def long_jump(self, use_reactor: bool = False) -> None:
        self._require_hopper().long_jump(use_reactor=use_reactor)

    def go_underground(self) -> None:
        self._require_hopper().go_underground()

    def return_to_surface(self) -> None:
        self._require_hopper().return_to_surface()

    def drill_forward(self) -> None:
        self._require_hopper().drill_forward()

    def get_current_status(self) -> dict:
        return self._require_hopper().get_current_status()
