from enum import Enum, auto


class AutonomousSystemChoice(Enum):
    """
    :class:`AutonomousSystemChoice` to be used with :class:`AutonomousSystem`
    Source: OS4 Appendix A 

    +-----------+---------------+---------------+-------------------------+ 
    | Choice    | Weight        | Cost (USD)    | Added Power Consumption |
    +===========+===============+===============+=========================+
    | A1        | 5 kg          | $1,000        | 0.5 Wh/kW               |
    +-----------|---------------+---------------|-------------------------+
    | A2        | 12 kg         | $2,000        | 1.0 Wh/kW               |
    +-----------|---------------+---------------|-------------------------+
    | A3        | 30 kg         | $15,000       | 1.5 Wh/kW               |
    +-----------|---------------+---------------|-------------------------+
    | A4        | 60 kg         | $35,000       | 2.5 Wh/kW               |
    +-----------|---------------+---------------|-------------------------+
    | A5        | 120 kg        | $60,000       | 5.0 Wh/kW               |
    +-----------|---------------+---------------|-------------------------+    
    """
    A1 = auto()
    A2 = auto()
    A3 = auto()
    A4 = auto()
    A5 = auto()


class AutonomousSystem:
    """
    :class:`AutonomousSystem` represents an instance of an autonomous system. To be used in the construction of :class:`Ev`
    """

    def __init__(self, autonomous_system: AutonomousSystemChoice) -> None:

        if type(autonomous_system) is not AutonomousSystemChoice:
            raise ValueError(f'autonomous_system argument must be of type AutonomousSystemChoice rather than supplied {type(autonomous_system)}')

        self._key_weight_kg = "weight_kg"
        self._key_added_power_consumption_Wh_per_kW = "added_power_consumption_Wh_per_kW"
        self._key_cost_1k_usd = "cost_1k_usd"

        attribute_dict = self._get_attribute_mapping(autonomous_system)

        self.choice: AutonomousSystemChoice = autonomous_system
        self.weight_kg: float = attribute_dict.get(self._key_weight_kg, -1)
        self.added_power_consumption_Wh_per_kW: float = attribute_dict.get(self._key_added_power_consumption_Wh_per_kW, -1)
        self.cost_1k_usd: float =  attribute_dict.get(self._key_cost_1k_usd, -1)

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
