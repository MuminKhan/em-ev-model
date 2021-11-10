from enum import Enum, auto


class BatteryChargerChoice(Enum):
    """
    :class:`BatteryChargerChoice` to be used with :class:`BatteryCharger` 
    Source: OS4 Appendix A 

    +--------+--------+------------+------------+ 
    | Choice | Weight | Cost (USD) | Power (kW) |
    +========+========+============+============+
    | G1     | 1.0 kg | $1,000     | 10 kW      |
    +--------|--------+------------|------------+
    | G2     | 1.8 kg | $2,500     | 20 kW      |
    +--------|--------+------------|------------+
    | G3     | 5.0 kg | $10,000    | 60 kW      |
    +--------|--------+------------|------------+    
    """

    G1 = auto()
    G2 = auto()
    G3 = auto()


class BatteryCharger:
    """
    :class:`BatteryCharger` represents an instance of a battery charger. To be used in the construction of :class:`Ev`
    """

    def __init__(self, battery_charger_choice: BatteryChargerChoice) -> None:
        
        if type(battery_charger_choice) is not BatteryChargerChoice:
            raise ValueError(f'battery_charger_choice argument must be of type BatteryChargerChoice rather than supplied {type(battery_charger_choice)}')

        self._key_power_kW = "power_kW"
        self._key_cost_1k_usd = "cost_1k_usd"
        self._key_weight_kg = "weight_kg"

        attribute_dict = self._get_attribute_mapping(battery_charger_choice)

        self.choice: BatteryChargerChoice = battery_charger_choice
        self.power_kW: float = attribute_dict.get(self._key_power_kW, -1)
        self.cost_1k_usd: float = attribute_dict.get(self._key_cost_1k_usd, -1)
        self.weight_kg: float = attribute_dict.get(self._key_weight_kg, -1)

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
