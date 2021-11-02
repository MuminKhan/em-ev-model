

from models.ev import Ev


class Fleet:

    def __init__(self, ev: Ev, fleet_size: int) -> None:

        """
        In addition to the model documentation, create a table that describes 5 unique architecture instances (of your choice) that includes this information used and/or produced by your model:
        •	Fleet size (number of vehicles).
        •	Vehicle specifications (the design variables—from Appendix C—used in the specific architecture instance).
        •	Intermediate performance variables for each architecture instance:
            o	Vehicle speed and range; fleet throughput, average wait time, and availability.
        •	Vehicle and fleet cost.
        """

        # CONSTANTS
        # Average passenger weight [kg] = 100
        self.PASSENGER_WEIGHT_AVERAGE_KG = 100

        # Expected average load factor/trip = 0.75
        self.LOAD_FACTOR_EXPECTED_AVG = 0.75

        # Benchmark availability of competing systems: 0.75
        self.BENCHMARK_AVAIL_COMPETING_SYSTEMS = 0.75

        # Dwell time [s] = 60 (time for passengers get out and get in)
        self.DWELL_TIME_SECONDS = 60

        self.vehicle = ev
        self.fleet_size = fleet_size
        self.fleet_cost = self.calculate_total_fleet_cost_usd()

        self.operated_speed = None # TODO: Clarify? Is this from the EV?
        self.availability = None # TODO: Clarify? Is this from the EV?

        self.fleet_throughput = None # TODO: Clarify?
        self.average_wait_time = None # TODO: Clarify? Route dependent? 

    def calculate_frequency_per_hour(self, volume, cars_per_train=1):
        f = volume / (self.LOAD_FACTOR_EXPECTED_AVG * self.vehicle.chasis.passenger_capacity * cars_per_train)
        return f

    def calculate_total_fleet_cost_usd(self) -> float:
        return self.vehicle.total_vehicle_cost_1k_usd * self.fleet_size
