from enum import Enum, auto


class ChasisChoice(Enum):
    C1 = auto()
    C2 = auto()
    C3 = auto()
    C4 = auto()
    C5 = auto()
    C6 = auto()
    C7 = auto()
    C8 = auto()


class Chasis:

    def __init__(self, chasis_choice: ChasisChoice) -> None:

        self._key_pax = "pax"
        self._key_weight_kg = "weight_kg"
        self._key_cost_1k_usd = "cost_1k_usd"
        self._key_nominal_power_consumption_Wh_per_km = "nominal_power_consumption_Wh_per_km"

        attribute_dict = self._get_attribute_mapping(chasis_choice)

        self.choice = chasis_choice
        self.pax = attribute_dict.get(self._key_pax, -1)
        self.weight_kg = attribute_dict.get(self._key_weight_kg, -1)
        self.cost_1k_usd = attribute_dict.get(self._key_cost_1k_usd, -1)
        self.nominal_power_consumption_Wh_per_km = attribute_dict.get(self._key_nominal_power_consumption_Wh_per_km, -1)

    def _get_attribute_mapping(self, chasis_choice: ChasisChoice) -> dict:

        attribute_map = {
            ChasisChoice.C1: {
                self._key_pax: 2,
                self._key_weight_kg: 1350,
                self._key_cost_1k_usd: 12,
                self._key_nominal_power_consumption_Wh_per_km: 140
            },
            ChasisChoice.C2: {
                self._key_pax: 4,
                self._key_weight_kg: 1600,
                self._key_cost_1k_usd: 17,
                self._key_nominal_power_consumption_Wh_per_km: 135
            },
            ChasisChoice.C3: {
                self._key_pax: 6,
                self._key_weight_kg: 1800,
                self._key_cost_1k_usd: 21,
                self._key_nominal_power_consumption_Wh_per_km: 145
            },
            ChasisChoice.C4: {
                self._key_pax: 8,
                self._key_weight_kg: 2000,
                self._key_cost_1k_usd: 29,
                self._key_nominal_power_consumption_Wh_per_km: 150
            },
            ChasisChoice.C5: {
                self._key_pax: 10,
                self._key_weight_kg: 2200,
                self._key_cost_1k_usd: 31,
                self._key_nominal_power_consumption_Wh_per_km: 160
            },
            ChasisChoice.C6: {
                self._key_pax: 16,
                self._key_weight_kg: 2500,
                self._key_cost_1k_usd: 33,
                self._key_nominal_power_consumption_Wh_per_km: 165
            },
            ChasisChoice.C7: {
                self._key_pax: 20,
                self._key_weight_kg: 4000,
                self._key_cost_1k_usd: 38,
                self._key_nominal_power_consumption_Wh_per_km: 180
            },
            ChasisChoice.C8: {
                self._key_pax: 30,
                self._key_weight_kg: 7000,
                self._key_cost_1k_usd: 47,
                self._key_nominal_power_consumption_Wh_per_km: 210
            }
        }

        return attribute_map.get(chasis_choice, None)

    def __str__(self) -> str:
        return self.choice.name
