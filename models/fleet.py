

from models.ev import Ev


class Fleet:

    def __init__(self, ev: Ev, fleet_size: int) -> None:
        self.vehicle = ev
        self.fleet_size = fleet_size
        self.fleet_cost = self.calculate_total_fleet_cost_usd()

    @staticmethod
    def calculate_frequency_per_hour(volume, max_volume_to_capacity_ratio, passengers_per_car, cars_per_train=1):
        f = volume / (max_volume_to_capacity_ratio * passengers_per_car * cars_per_train)
        return f

    def calculate_total_fleet_cost_usd(self) -> float:
        return self.vehicle.total_vehicle_cost_1k_usd * self.fleet_size
