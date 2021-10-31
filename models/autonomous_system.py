from enum import Enum, auto


class AutonomousSystemChoice(Enum):
    A1 = auto()
    A2 = auto()
    A3 = auto()
    A4 = auto()
    A5 = auto()


class AutonomousSystem:

    def __init__(self, autonomous_system: AutonomousSystemChoice) -> None:

        self._key_weight_kg = "weight_kg"
        self._key_added_power_consumption_Wh_per_kW = "added_power_consumption_Wh_per_kW"
        self._key_cost_1k_usd = "cost_1k_usd"

        attribute_dict = self._get_attribute_mapping(autonomous_system)

        self.choice = autonomous_system
        self.weight_kg = attribute_dict.get(self._key_weight_kg, -1)
        self.added_power_consumption_Wh_per_kW = attribute_dict.get(self._key_added_power_consumption_Wh_per_kW, -1)
        self.cost_1k_usd = attribute_dict.get(self._key_cost_1k_usd, -1)

    def _get_attribute_mapping(self, autonomous_system: AutonomousSystemChoice) -> dict:

        attribute_map = {
            AutonomousSystemChoice.A1: {
                self._key_weight_kg: 5,
                self._key_added_power_consumption_Wh_per_kW: 0.5,
                self._key_cost_1k_usd: 1
            },
            AutonomousSystemChoice.A2: {
                self._key_weight_kg: 12,
                self._key_added_power_consumption_Wh_per_kW: 1.0,
                self._key_cost_1k_usd: 2
            },
            AutonomousSystemChoice.A3: {
                self._key_weight_kg: 30,
                self._key_added_power_consumption_Wh_per_kW: 1.5,
                self._key_cost_1k_usd: 15
            },
            AutonomousSystemChoice.A4: {
                self._key_weight_kg: 60,
                self._key_added_power_consumption_Wh_per_kW: 2.5,
                self._key_cost_1k_usd: 35
            },
            AutonomousSystemChoice.A5: {
                self._key_weight_kg: 120,
                self._key_added_power_consumption_Wh_per_kW: 5.0,
                self._key_cost_1k_usd: 60
            }
        }

        return attribute_map.get(autonomous_system, None)

    def __str__(self) -> str:
        return self.choice.name
