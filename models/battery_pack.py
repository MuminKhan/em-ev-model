from enum import Enum, auto


class BatteryPackChoice(Enum):
    P1 = auto()
    P2 = auto()
    P3 = auto()
    P4 = auto()
    P5 = auto()
    P6 = auto()
    P7 = auto()


class BatteryPack:

    def __init__(self, battery_pack_choice: BatteryPackChoice) -> None:

        self._key_capacity_kWh = "capacity_kWh"
        self._key_cost_1k_usd = "cost_1k_usd"
        self._key_weight_kg = "weight_kg"

        attribute_dict = self._get_attribute_mapping(battery_pack_choice)

        self.choice = battery_pack_choice
        self.capacity_kWh = attribute_dict.get(self._key_capacity_kWh, -1)
        self.cost_1k_usd = attribute_dict.get(self._key_cost_1k_usd, -1)
        self.weight_kg = attribute_dict.get(self._key_weight_kg, -1)

    def _get_attribute_mapping(self, battery_pack_choice: BatteryPackChoice) -> dict:

        attribute_map = {
            BatteryPackChoice.P1: {
                self._key_capacity_kWh: 40,
                self._key_cost_1k_usd: 8,
                self._key_weight_kg: 512
            },
            BatteryPackChoice.P2: {
                self._key_capacity_kWh: 60,
                self._key_cost_1k_usd: 16,
                self._key_weight_kg: 420
            },
            BatteryPackChoice.P3: {
                self._key_capacity_kWh: 75,
                self._key_cost_1k_usd: 16,
                self._key_weight_kg: 825
            },
            BatteryPackChoice.P4: {
                self._key_capacity_kWh: 100,
                self._key_cost_1k_usd: 25,
                self._key_weight_kg: 800
            },
            BatteryPackChoice.P5: {
                self._key_capacity_kWh: 125,
                self._key_cost_1k_usd: 25,
                self._key_weight_kg: 1500
            },
            BatteryPackChoice.P6: {
                self._key_capacity_kWh: 240,
                self._key_cost_1k_usd: 62,
                self._key_weight_kg: 1680
            },
            BatteryPackChoice.P7: {
                self._key_capacity_kWh: 240,
                self._key_cost_1k_usd: 48,
                self._key_weight_kg: 2880
            }
        }

        return attribute_map.get(battery_pack_choice, None)

    def __str__(self) -> str:
        return self.choice.name
