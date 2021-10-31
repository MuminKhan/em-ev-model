from enum import Enum, auto


class MotorAndInverterChoice(Enum):
    M1 = auto()
    M2 = auto()
    M3 = auto()
    M4 = auto()


class MotorAndInverter:

    def __init__(self, motor_and_inverter: MotorAndInverterChoice) -> None:

        self._key_weight_kg = "weight_kg"
        self._key_power_kW = "power_kW"
        self._key_cost_1k_usd = "cost_1k_usd"

        attribute_dict = self._get_attribute_mapping(motor_and_inverter)

        self.choice = motor_and_inverter
        self.weight_kg = attribute_dict.get(self._key_weight_kg, -1)
        self.power_kW = attribute_dict.get(self._key_power_kW, -1)
        self.cost_1k_usd = attribute_dict.get(self._key_cost_1k_usd, -1)

    def _get_attribute_mapping(self, motor_and_inverter: MotorAndInverterChoice) -> dict:

        attribute_map = {
            MotorAndInverterChoice.M1: {
                self._key_weight_kg: 82,
                self._key_power_kW: 150,
                self._key_cost_1k_usd: 1.2
            },
            MotorAndInverterChoice.M2: {
                self._key_weight_kg: 60,
                self._key_power_kW: 150,
                self._key_cost_1k_usd: 1.4
            },
            MotorAndInverterChoice.M3: {
                self._key_weight_kg: 140,
                self._key_power_kW: 210,
                self._key_cost_1k_usd: 1.65
            },
            MotorAndInverterChoice.M4: {
                self._key_weight_kg: 100,
                self._key_power_kW: 450,
                self._key_cost_1k_usd: 3600
            }
        }

        return attribute_map.get(motor_and_inverter, None)

    def __str__(self) -> str:
        return self.choice.name