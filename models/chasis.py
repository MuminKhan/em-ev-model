from enum import Enum, auto


class ChasisChoice(Enum):
    """
    :class:`ChasisChoice` to be used with :class:`Chasis`
    Source: OS4 Appendix A 

    +--------+---------+------------+---------------+---------------------------+
    | Choice | Weight  | Cost (USD) | Capacity      | Nominal Power Consumption |
    +========+=========+============+===============+===========================+
    | C1     | 1350 kg | $12,000    |  2 passengers | 140 Wh/kW                 |
    +--------|---------+------------|---------------+---------------------------|
    | C2     | 1600 kg | $17,000    |  4 passengers | 135 Wh/kW                 |
    +--------|---------+------------|---------------+---------------------------|
    | C3     | 1800 kg | $21,000    |  6 passengers | 145 Wh/kW                 |
    +--------|---------+------------|---------------+---------------------------|
    | C4     | 2000 kg | $29,000    |  8 passengers | 150 Wh/kW                 |
    +--------|---------+------------|---------------+---------------------------|
    | C5     | 2200 kg | $31,000    | 10 passengers | 160 Wh/kW                 |
    +--------|---------+------------|---------------+---------------------------|
    | C6     | 2500 kg | $33,000    | 16 passengers | 165 Wh/kW                 |
    +--------|---------+------------|---------------+---------------------------|
    | C7     | 4000 kg | $38,000    | 20 passengers | 180 Wh/kW                 |
    +--------|---------+------------|---------------+---------------------------|
    | C8     | 7000 kg | $47,000    | 30 passengers | 210 Wh/kW                 |
    +--------+---------+------------+---------------+---------------------------+    
    """
    C1 = auto()
    C2 = auto()
    C3 = auto()
    C4 = auto()
    C5 = auto()
    C6 = auto()
    C7 = auto()
    C8 = auto()


class Chasis:
    """
    :class:`Chasis` represents an instance of a chasis. To be used in the construction of :class:`Ev`
    """

    def __init__(self, chasis_choice: ChasisChoice) -> None:

        if type(chasis_choice) is not ChasisChoice:
            raise ValueError(f'chasis_choice argument must be of type ChasisChoice rather than supplied {type(chasis_choice)}')

        self._key_passenger_capacity = "passenger_capacity"
        self._key_weight_kg = "weight_kg"
        self._key_cost_1k_usd = "cost_1k_usd"
        self._key_nominal_power_consumption_Wh_per_km = "nominal_power_consumption_Wh_per_km"

        attribute_dict = self._get_attribute_mapping(chasis_choice)

        self.choice = chasis_choice
        self.passenger_capacity = attribute_dict.get(self._key_passenger_capacity, -1)
        self.weight_kg = attribute_dict.get(self._key_weight_kg, -1)
        self.cost_1k_usd = attribute_dict.get(self._key_cost_1k_usd, -1)
        self.nominal_power_consumption_Wh_per_km = attribute_dict.get(self._key_nominal_power_consumption_Wh_per_km, -1)

    def _get_attribute_mapping(self, chasis_choice: ChasisChoice) -> dict:

        attribute_map = {
            ChasisChoice.C1: {
                self._key_passenger_capacity: 2,
                self._key_weight_kg: 1350,
                self._key_cost_1k_usd: 12,
                self._key_nominal_power_consumption_Wh_per_km: 140
            },
            ChasisChoice.C2: {
                self._key_passenger_capacity: 4,
                self._key_weight_kg: 1600,
                self._key_cost_1k_usd: 17,
                self._key_nominal_power_consumption_Wh_per_km: 135
            },
            ChasisChoice.C3: {
                self._key_passenger_capacity: 6,
                self._key_weight_kg: 1800,
                self._key_cost_1k_usd: 21,
                self._key_nominal_power_consumption_Wh_per_km: 145
            },
            ChasisChoice.C4: {
                self._key_passenger_capacity: 8,
                self._key_weight_kg: 2000,
                self._key_cost_1k_usd: 29,
                self._key_nominal_power_consumption_Wh_per_km: 150
            },
            ChasisChoice.C5: {
                self._key_passenger_capacity: 10,
                self._key_weight_kg: 2200,
                self._key_cost_1k_usd: 31,
                self._key_nominal_power_consumption_Wh_per_km: 160
            },
            ChasisChoice.C6: {
                self._key_passenger_capacity: 16,
                self._key_weight_kg: 2500,
                self._key_cost_1k_usd: 33,
                self._key_nominal_power_consumption_Wh_per_km: 165
            },
            ChasisChoice.C7: {
                self._key_passenger_capacity: 20,
                self._key_weight_kg: 4000,
                self._key_cost_1k_usd: 38,
                self._key_nominal_power_consumption_Wh_per_km: 180
            },
            ChasisChoice.C8: {
                self._key_passenger_capacity: 30,
                self._key_weight_kg: 7000,
                self._key_cost_1k_usd: 47,
                self._key_nominal_power_consumption_Wh_per_km: 210
            }
        }

        return attribute_map.get(chasis_choice, None)

    def __str__(self) -> str:
        return self.choice.name
