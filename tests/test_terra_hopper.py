"""Модульные тесты TerraHopper (SPEC 5.1, TC_P_1…TC_P_13, TC_N_21…TC_N_38)."""

from terra_hopper import (
    InvalidLocationError,
    NotEnoughEnergyError,
    NotEnoughStrengthError,
    TerraHopper,
)
from tests.constants import (
    Distance,
    Location,
    Mass,
    Messages,
    ReactorEnergy,
    Strength,
    Transport,
)
from tests.steps import Steps


class TestTerraHopperInit(Steps):
    """Конструктор TerraHopper (SPEC 3.2)."""

    # region =====Happy=====
    def test_p1_init_with_defaults(self):
        """TC_P_1: параметры по умолчанию."""
        # Arrange

        self.step("Создание транспорта с параметрами по умолчанию")
        hopper = self.given_hopper(mass_kg=Mass.DEFAULT)

        # Act

        self.step("Чтение имени и массы")
        name = hopper.name
        mass_kg = hopper.mass_kg

        # Assert

        self.step("Проверка имени")
        self.assertEqual(first=name,
                         second=Transport.NAME,
                         msg=None)  # fmt: skip

        self.step("Проверка массы")
        self.assert_that(actual=mass_kg,
                         expected=Mass.DEFAULT,
                         msg=None)  # fmt: skip

        self.step("Проверка статуса")
        self.assert_status(expected={"distance": Distance.DEFAULT,
                                     "strength": Strength.MAX,
                                     "reactor_energy": ReactorEnergy.MAX,
                                     "location_state": Location.SURFACE})  # fmt: skip

    def test_p2_init_with_all_parameters(self):
        """TC_P_2: все параметры заданы явно."""
        # Arrange

        self.step("Создание транспорта со всеми параметрами")
        hopper = self.given_hopper(mass_kg=350.0,
                                   strength=80.0,
                                   reactor_energy=60.0)  # fmt: skip

        # Act

        self.step("Чтение имени и массы")
        name = hopper.name
        mass_kg = hopper.mass_kg

        # Assert

        self.step("Проверка имени")
        self.assertEqual(first=name,
                         second=Transport.NAME,
                         msg=None)  # fmt: skip

        self.step("Проверка массы")
        self.assert_that(actual=mass_kg,
                         expected=350.0,
                         msg=None)  # fmt: skip

        self.step("Проверка статуса")
        self.assert_status(expected={"distance": Distance.DEFAULT,
                                     "strength": 80.0,
                                     "reactor_energy": 60.0,
                                     "location_state": Location.SURFACE})  # fmt: skip
    # endregion

    # region =====Error=====
    def test_n21_init_empty_name_raises(self):
        """TC_N_21: пустое имя."""
        # Act + Assert

        self.step("Проверка ошибки при пустом имени")
        self.assert_raises_with_message(exception=ValueError,
                                        message=Messages.EMPTY_NAME,
                                        action=TerraHopper,
                                        name="",
                                        mass_kg=Mass.DEFAULT)  # fmt: skip

    def test_n21b_init_whitespace_name_raises(self):
        """TC_N_21: имя состоит только из пробелов."""
        # Act + Assert

        self.step("Проверка ошибки при имени из пробелов")
        self.assert_raises_with_message(exception=ValueError,
                                        message=Messages.EMPTY_NAME,
                                        action=TerraHopper,
                                        name="   ",
                                        mass_kg=Mass.DEFAULT)  # fmt: skip

    def test_n22_init_mass_below_min_raises(self):
        """TC_N_22: масса меньше минимальной."""
        # Act + Assert

        self.step("Проверка ошибки при массе ниже минимума")
        self.assert_raises_with_message(exception=ValueError,
                                        message=Messages.MASS_RANGE,
                                        action=TerraHopper,
                                        name=Transport.NAME,
                                        mass_kg=50.0)  # fmt: skip

    def test_n23_init_mass_above_max_raises(self):
        """TC_N_23: масса больше максимальной."""
        # Act + Assert

        self.step("Проверка ошибки при массе выше максимума")
        self.assert_raises_with_message(exception=ValueError,
                                        message=Messages.MASS_RANGE,
                                        action=TerraHopper,
                                        name=Transport.NAME,
                                        mass_kg=600.0)  # fmt: skip

    def test_n24_init_strength_above_max_raises(self):
        """TC_N_24: сила больше максимальной."""
        # Act + Assert

        self.step("Проверка ошибки при силе выше максимума")
        self.assert_raises_with_message(exception=ValueError,
                                        message=Messages.STRENGTH_RANGE,
                                        action=TerraHopper,
                                        name=Transport.NAME,
                                        mass_kg=Mass.DEFAULT,
                                        strength=110.0)  # fmt: skip

    def test_n25_init_reactor_energy_below_min_raises(self):
        """TC_N_25: энергия реактора меньше минимальной."""
        # Act + Assert

        self.step("Проверка ошибки при энергии ниже минимума")
        self.assert_raises_with_message(exception=ValueError,
                                        message=Messages.ENERGY_RANGE,
                                        action=TerraHopper,
                                        name=Transport.NAME,
                                        mass_kg=Mass.DEFAULT,
                                        reactor_energy=-10.0)  # fmt: skip
    # endregion


class TestBasicJump(Steps):
    """basic_jump (SPEC 3.4.1)."""

    # region =====Happy=====
    def test_p3_basic_jump_updates_state(self):
        """TC_P_3: успешный прыжок с поверхности."""
        # Arrange

        self.step("Создание транспорта")
        self.given_hopper(mass_kg=Mass.DEFAULT)

        # Act

        self.step("Снятие статуса до прыжка")
        before = self.current_status()

        self.step("Обычный прыжок")
        self.when_basic_jump()

        # Assert

        self.step("Проверка статуса после прыжка")
        expected = self.expected_after_basic_jump(mass_kg=Mass.DEFAULT,
                                                  status=before)  # fmt: skip
        self.assert_status(expected=expected)

    def test_p4_basic_jump_strength_exactly_required(self):
        """TC_P_4: силы ровно хватает."""
        # Arrange

        self.step("Создание транспорта с силой ровно на прыжок")
        self.given_hopper(mass_kg=Mass.DEFAULT,
                          strength=5.0)  # fmt: skip

        # Act

        self.step("Снятие статуса до прыжка")
        before = self.current_status()

        self.step("Обычный прыжок")
        self.when_basic_jump()

        # Assert

        self.step("Проверка статуса после прыжка")
        expected = self.expected_after_basic_jump(mass_kg=Mass.DEFAULT,
                                                  status=before)  # fmt: skip
        self.assert_status(expected=expected)
    # endregion

    # region =====Error=====
    def test_n26_basic_jump_underground_raises(self):
        """TC_N_26: прыжок под землёй."""
        # Arrange

        self.step("Создание транспорта под землёй")
        self.given_hopper(mass_kg=Mass.DEFAULT,
                          location_state=Location.UNDERGROUND)  # fmt: skip

        self.step("Снятие статуса до действия")
        before = self.current_status()

        # Act + Assert

        self.step("Проверка ошибки прыжка под землёй")
        self.assert_raises_with_message(exception=InvalidLocationError,
                                        message=Messages.JUMP_UNDERGROUND,
                                        action=self.when_basic_jump)  # fmt: skip

        self.step("Проверка неизменности состояния")
        self.assert_status(expected=before,
                           msg="состояние не изменилось после исключения")  # fmt: skip

    def test_n27_basic_jump_not_enough_strength_raises(self):
        """TC_N_27: нехватка силы."""
        # Arrange

        self.step("Создание транспорта с малой силой")
        self.given_hopper(mass_kg=Mass.DEFAULT,
                          strength=3.0)  # fmt: skip

        self.step("Снятие статуса до действия")
        before = self.current_status()

        # Act + Assert

        self.step("Проверка ошибки при нехватке силы")
        self.assert_raises_with_message(exception=NotEnoughStrengthError,
                                        message=Messages.NO_STRENGTH_BASIC,
                                        action=self.when_basic_jump)  # fmt: skip

        self.step("Проверка неизменности состояния")
        self.assert_status(expected=before,
                           msg="состояние не изменилось после исключения")  # fmt: skip
    # endregion


class TestLongJump(Steps):
    """long_jump (SPEC 3.4.2)."""

    # region =====Happy=====
    def test_p5_long_jump_without_reactor(self):
        """TC_P_5: прыжок без реактора."""
        # Arrange

        self.step("Создание транспорта")
        self.given_hopper(mass_kg=Mass.DEFAULT)

        # Act

        self.step("Снятие статуса до прыжка")
        before = self.current_status()

        self.step("Дальний прыжок без реактора")
        self.when_long_jump(use_reactor=False)

        # Assert

        self.step("Проверка статуса после прыжка")
        expected = self.expected_after_long_jump(mass_kg=Mass.DEFAULT,
                                                 status=before,
                                                 use_reactor=False)  # fmt: skip
        self.assert_status(expected=expected)

    def test_p6_long_jump_with_reactor(self):
        """TC_P_6: прыжок с форсажем."""
        # Arrange

        self.step("Создание транспорта")
        self.given_hopper(mass_kg=Mass.DEFAULT)

        # Act

        self.step("Снятие статуса до прыжка")
        before = self.current_status()

        self.step("Дальний прыжок с форсажем")
        self.when_long_jump(use_reactor=True)

        # Assert

        self.step("Проверка статуса после прыжка")
        expected = self.expected_after_long_jump(mass_kg=Mass.DEFAULT,
                                                 status=before,
                                                 use_reactor=True)  # fmt: skip
        self.assert_status(expected=expected)

    def test_p7_long_jump_reactor_energy_exactly_minimum(self):
        """TC_P_7: энергии ровно 50.0."""
        # Arrange

        self.step("Создание транспорта с минимальной энергией")
        self.given_hopper(mass_kg=Mass.DEFAULT,
                          reactor_energy=ReactorEnergy.MIN_FOR_ACTION)  # fmt: skip

        # Act

        self.step("Снятие статуса до прыжка")
        before = self.current_status()

        self.step("Дальний прыжок с форсажем")
        self.when_long_jump(use_reactor=True)

        # Assert

        self.step("Проверка статуса после прыжка")
        expected = self.expected_after_long_jump(mass_kg=Mass.DEFAULT,
                                                 status=before,
                                                 use_reactor=True)  # fmt: skip
        self.assert_status(expected=expected)
    # endregion

    # region =====Error=====
    def test_n28_long_jump_underground_raises(self):
        """TC_N_28: прыжок под землёй."""
        # Arrange

        self.step("Создание транспорта под землёй")
        self.given_hopper(mass_kg=Mass.DEFAULT,
                          location_state=Location.UNDERGROUND)  # fmt: skip

        self.step("Снятие статуса до действия")
        before = self.current_status()

        # Act + Assert

        self.step("Проверка ошибки дальнего прыжка под землёй")
        self.assert_raises_with_message(exception=InvalidLocationError,
                                        message=Messages.LONG_JUMP_UNDERGROUND,
                                        action=self.when_long_jump)  # fmt: skip

        self.step("Проверка неизменности состояния")
        self.assert_status(expected=before,
                           msg="состояние не изменилось после исключения")  # fmt: skip

    def test_n29_long_jump_not_enough_strength_raises(self):
        """TC_N_29: нехватка силы."""
        # Arrange

        self.step("Создание транспорта с малой силой")
        self.given_hopper(mass_kg=Mass.DEFAULT,
                          strength=10.0)  # fmt: skip

        self.step("Снятие статуса до действия")
        before = self.current_status()

        # Act + Assert

        self.step("Проверка ошибки при нехватке силы")
        self.assert_raises_with_message(exception=NotEnoughStrengthError,
                                        message=Messages.NO_STRENGTH_LONG,
                                        action=self.when_long_jump)  # fmt: skip

        self.step("Проверка неизменности состояния")
        self.assert_status(expected=before,
                           msg="состояние не изменилось после исключения")  # fmt: skip

    def test_n30_long_jump_not_enough_energy_raises(self):
        """TC_N_30: нехватка энергии реактора для форсажа."""
        # Arrange

        self.step("Создание транспорта с малой энергией")
        self.given_hopper(mass_kg=Mass.DEFAULT,
                          reactor_energy=30.0)  # fmt: skip

        self.step("Снятие статуса до действия")
        before = self.current_status()

        # Act + Assert

        self.step("Проверка ошибки при нехватке энергии")
        self.assert_raises_with_message(exception=NotEnoughEnergyError,
                                        message=Messages.NO_ENERGY_BOOST,
                                        action=self.when_long_jump,
                                        use_reactor=True)  # fmt: skip

        self.step("Проверка неизменности состояния")
        self.assert_status(expected=before,
                           msg="состояние не изменилось после исключения")  # fmt: skip
    # endregion


class TestDistanceRecovery(Steps):
    """Восстановление на отметке 100 м (SPEC 3.4.3)."""

    # region =====Happy=====
    def test_p8_recovery_on_distance_mark(self):
        """TC_P_8: восстановление на отметке 100 м."""
        # Arrange

        self.step("Создание транспорта на отметке 100 м")
        self.given_hopper(mass_kg=Mass.DEFAULT,
                          strength=50.0,
                          reactor_energy=50.0,
                          distance=Distance.MARK)  # fmt: skip

        # Act

        self.step("Снятие статуса до восстановления")
        before = self.current_status()

        self.step("Применение восстановления")
        self.when_apply_recovery()

        # Assert

        self.step("Проверка статуса после восстановления")
        expected = self.expected_after_recovery(mass_kg=Mass.DEFAULT,
                                                status=before)  # fmt: skip
        self.assert_status(expected=expected)

    def test_p9_recovery_capped_at_maximum(self):
        """TC_P_9: ограничение восстановления значением 100.0."""
        # Arrange

        self.step("Создание транспорта на отметке 100 м")
        self.given_hopper(mass_kg=Mass.DEFAULT,
                          strength=90.0,
                          reactor_energy=95.0,
                          distance=Distance.MARK)  # fmt: skip

        # Act

        self.step("Снятие статуса до восстановления")
        before = self.current_status()

        self.step("Применение восстановления")
        self.when_apply_recovery()

        # Assert

        self.step("Проверка ограничения максимумом")
        expected = self.expected_after_recovery(mass_kg=Mass.DEFAULT,
                                                status=before)  # fmt: skip
        self.assert_status(expected=expected)
    # endregion

    # region =====Error=====
    def test_n31_recovery_not_triggered_before_mark(self):
        """TC_N_31: до отметки 100 м ничего не меняется."""
        # Arrange

        self.step("Создание транспорта до отметки 100 м")
        self.given_hopper(mass_kg=Mass.DEFAULT,
                          strength=50.0,
                          reactor_energy=50.0,
                          distance=50.0)  # fmt: skip

        self.step("Снятие статуса до действия")
        before = self.current_status()

        # Act

        self.step("Применение восстановления")
        self.when_apply_recovery()

        # Assert

        self.step("Проверка неизменности состояния")
        self.assert_status(expected=before,
                           msg="состояние не изменилось до отметки 100 м")  # fmt: skip
    # endregion


class TestGetCurrentStatus(Steps):
    """get_current_status (SPEC 3.4.4)."""

    # region =====Happy=====
    def test_p10_status_returns_state_dict(self):
        """TC_P_10: возвращается словарь состояния."""
        # Arrange

        self.step("Создание транспорта с заданными параметрами")
        self.given_hopper(mass_kg=Mass.DEFAULT,
                          strength=80.0,
                          reactor_energy=90.0,
                          distance=20.0,
                          location_state=Location.SURFACE)  # fmt: skip

        # Act

        self.step("Получение статуса")
        status = self.current_status()

        # Assert

        self.step("Проверка статуса")
        self.assert_that(actual=status,
                         expected={"distance": 20.0,
                                   "strength": 80.0,
                                   "reactor_energy": 90.0,
                                   "location_state": Location.SURFACE})  # fmt: skip
    # endregion


class TestGoUnderground(Steps):
    """go_underground (SPEC 3.4.5)."""

    # region =====Happy=====
    def test_p11_go_underground_from_surface(self):
        """TC_P_11: успешное погружение."""
        # Arrange

        self.step("Создание транспорта на поверхности")
        self.given_hopper(mass_kg=Mass.DEFAULT)

        # Act

        self.step("Снятие статуса до погружения")
        before = self.current_status()

        self.step("Погружение под землю")
        self.when_go_underground()

        # Assert

        self.step("Проверка статуса после погружения")
        expected = self.expected_after_go_underground(mass_kg=Mass.DEFAULT,
                                                      status=before)  # fmt: skip
        self.assert_status(expected=expected)
    # endregion

    # region =====Error=====
    def test_n32_go_underground_already_underground_raises(self):
        """TC_N_32: повторное погружение."""
        # Arrange

        self.step("Создание транспорта под землёй")
        self.given_hopper(mass_kg=Mass.DEFAULT,
                          location_state=Location.UNDERGROUND)  # fmt: skip

        self.step("Снятие статуса до действия")
        before = self.current_status()

        # Act + Assert

        self.step("Проверка ошибки повторного погружения")
        self.assert_raises_with_message(exception=InvalidLocationError,
                                        message=Messages.ALREADY_UNDERGROUND,
                                        action=self.when_go_underground)  # fmt: skip

        self.step("Проверка неизменности состояния")
        self.assert_status(expected=before,
                           msg="состояние не изменилось после исключения")  # fmt: skip

    def test_n33_go_underground_not_enough_strength_raises(self):
        """TC_N_33: нехватка силы."""
        # Arrange

        self.step("Создание транспорта с малой силой")
        self.given_hopper(mass_kg=Mass.DEFAULT,
                          strength=5.0)  # fmt: skip

        self.step("Снятие статуса до действия")
        before = self.current_status()

        # Act + Assert

        self.step("Проверка ошибки при нехватке силы")
        self.assert_raises_with_message(exception=NotEnoughStrengthError,
                                        message=Messages.NO_STRENGTH_DIVE,
                                        action=self.when_go_underground)  # fmt: skip

        self.step("Проверка неизменности состояния")
        self.assert_status(expected=before,
                           msg="состояние не изменилось после исключения")  # fmt: skip
    # endregion


class TestReturnToSurface(Steps):
    """return_to_surface (SPEC 3.4.6)."""

    # region =====Happy=====
    def test_p12_return_to_surface_from_underground(self):
        """TC_P_12: успешный подъём."""
        # Arrange

        self.step("Создание транспорта под землёй")
        self.given_hopper(mass_kg=Mass.DEFAULT,
                          location_state=Location.UNDERGROUND)  # fmt: skip

        # Act

        self.step("Снятие статуса до подъёма")
        before = self.current_status()

        self.step("Возврат на поверхность")
        self.when_return_to_surface()

        # Assert

        self.step("Проверка статуса после подъёма")
        expected = self.expected_after_return_to_surface(mass_kg=Mass.DEFAULT,
                                                         status=before)  # fmt: skip
        self.assert_status(expected=expected)
    # endregion

    # region =====Error=====
    def test_n34_return_to_surface_already_surface_raises(self):
        """TC_N_34: подъём с поверхности."""
        # Arrange

        self.step("Создание транспорта на поверхности")
        self.given_hopper(mass_kg=Mass.DEFAULT,
                          location_state=Location.SURFACE)  # fmt: skip

        self.step("Снятие статуса до действия")
        before = self.current_status()

        # Act + Assert

        self.step("Проверка ошибки подъёма с поверхности")
        self.assert_raises_with_message(exception=InvalidLocationError,
                                        message=Messages.ALREADY_SURFACE,
                                        action=self.when_return_to_surface)  # fmt: skip

        self.step("Проверка неизменности состояния")
        self.assert_status(expected=before,
                           msg="состояние не изменилось после исключения")  # fmt: skip

    def test_n35_return_to_surface_not_enough_strength_raises(self):
        """TC_N_35: нехватка силы."""
        # Arrange

        self.step("Создание транспорта под землёй с малой силой")
        self.given_hopper(mass_kg=Mass.DEFAULT,
                          location_state=Location.UNDERGROUND,
                          strength=5.0)  # fmt: skip

        self.step("Снятие статуса до действия")
        before = self.current_status()

        # Act + Assert

        self.step("Проверка ошибки при нехватке силы")
        self.assert_raises_with_message(exception=NotEnoughStrengthError,
                                        message=Messages.NO_STRENGTH_RETURN,
                                        action=self.when_return_to_surface)  # fmt: skip

        self.step("Проверка неизменности состояния")
        self.assert_status(expected=before,
                           msg="состояние не изменилось после исключения")  # fmt: skip
    # endregion


class TestDrillForward(Steps):
    """drill_forward (SPEC 3.4.7)."""

    # region =====Happy=====
    def test_p13_drill_forward_underground(self):
        """TC_P_13: успешный подземный рывок."""
        # Arrange

        self.step("Создание транспорта под землёй")
        self.given_hopper(mass_kg=Mass.DEFAULT,
                          location_state=Location.UNDERGROUND)  # fmt: skip

        # Act

        self.step("Снятие статуса до бурения")
        before = self.current_status()

        self.step("Бурение вперёд")
        self.when_drill_forward()

        # Assert

        self.step("Проверка статуса после бурения")
        expected = self.expected_after_drill_forward(mass_kg=Mass.DEFAULT,
                                                     status=before)  # fmt: skip
        self.assert_status(expected=expected)
    # endregion

    # region =====Error=====
    def test_n36_drill_forward_on_surface_raises(self):
        """TC_N_36: бурение на поверхности."""
        # Arrange

        self.step("Создание транспорта на поверхности")
        self.given_hopper(mass_kg=Mass.DEFAULT,
                          location_state=Location.SURFACE)  # fmt: skip

        self.step("Снятие статуса до действия")
        before = self.current_status()

        # Act + Assert

        self.step("Проверка ошибки бурения на поверхности")
        self.assert_raises_with_message(exception=InvalidLocationError,
                                        message=Messages.DRILL_ON_SURFACE,
                                        action=self.when_drill_forward)  # fmt: skip

        self.step("Проверка неизменности состояния")
        self.assert_status(expected=before,
                           msg="состояние не изменилось после исключения")  # fmt: skip

    def test_n37_drill_forward_not_enough_strength_raises(self):
        """TC_N_37: нехватка силы."""
        # Arrange

        self.step("Создание транспорта под землёй с малой силой")
        self.given_hopper(mass_kg=Mass.DEFAULT,
                          location_state=Location.UNDERGROUND,
                          strength=10.0)  # fmt: skip

        self.step("Снятие статуса до действия")
        before = self.current_status()

        # Act + Assert

        self.step("Проверка ошибки при нехватке силы")
        self.assert_raises_with_message(exception=NotEnoughStrengthError,
                                        message=Messages.NO_STRENGTH_DRILL,
                                        action=self.when_drill_forward)  # fmt: skip

        self.step("Проверка неизменности состояния")
        self.assert_status(expected=before,
                           msg="состояние не изменилось после исключения")  # fmt: skip

    def test_n38_drill_forward_not_enough_energy_raises(self):
        """TC_N_38: нехватка энергии реактора."""
        # Arrange

        self.step("Создание транспорта под землёй с малой энергией")
        self.given_hopper(mass_kg=Mass.DEFAULT,
                          location_state=Location.UNDERGROUND,
                          reactor_energy=40.0)  # fmt: skip

        self.step("Снятие статуса до действия")
        before = self.current_status()

        # Act + Assert

        self.step("Проверка ошибки при нехватке энергии")
        self.assert_raises_with_message(exception=NotEnoughEnergyError,
                                        message=Messages.NO_ENERGY_DRILL,
                                        action=self.when_drill_forward)  # fmt: skip

        self.step("Проверка неизменности состояния")
        self.assert_status(expected=before,
                           msg="состояние не изменилось после исключения")  # fmt: skip
    # endregion