

class Frequency:

    def __init__(self) -> None:
        pass

    @staticmethod
    def calculate_frequency_per_hour(volume, max_volume_to_capacity_ratio, passengers_per_car, cars_per_train=1):
        
        f = volume / (max_volume_to_capacity_ratio * passengers_per_car * cars_per_train)
        return f
