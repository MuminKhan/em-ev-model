from enum import Enum, auto


class BatteryChargerChoice(Enum):
    G1 = auto()
    G2 = auto()
    G3 = auto()


class BatteryCharger:

    def __init__(self, battery_choice: BatteryChargerChoice) -> None:

        self._key_power_kW = "power_kW"
        self._key_cost_1k_usd = "cost_1k_usd"
        self._key_weight_kg = "weight_kg"

        attribute_dict = self._get_attribute_mapping(battery_choice)

        self.choice = battery_choice
        self.power_kW = attribute_dict.get(self._key_power_kW, -1)
        self.cost_1k_usd = attribute_dict.get(self._key_cost_1k_usd, -1)
        self.weight_kg = attribute_dict.get(self._key_weight_kg, -1)

    def _get_attribute_mapping(self, battery_choice: BatteryChargerChoice) -> dict:

        attribute_map = {
            BatteryChargerChoice.G1: {
                self._key_power_kW: 10,
                self._key_cost_1k_usd: 1,
                self._key_weight_kg: 1
            },
            BatteryChargerChoice.G2: {
                self._key_power_kW: 20,
                self._key_cost_1k_usd: 2.5,
                self._key_weight_kg: 1.8
            },
            BatteryChargerChoice.G3: {
                self._key_power_kW: 60,
                self._key_cost_1k_usd: 10,
                self._key_weight_kg: 5
            }
        }

        return attribute_map.get(battery_choice, None)

    def __str__(self) -> str:
        return self.choice.name
