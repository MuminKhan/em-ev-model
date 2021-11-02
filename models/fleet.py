

from models.ev import Ev
from models.multi_attribute_utility import MultiAttributeUtility
from models.route import Route


class Fleet:

    def __init__(self, ev: Ev, fleet_size: int, route: Route) -> None:
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

        # Derived Parameters
        self.route = route
        self.vehicle = ev
        self.fleet_size = fleet_size
        self.fleet_cost = self.calculate_total_fleet_cost_usd()

        self.minimum_throughput = 5
        self.off_peak_throughput = 50
        self.peak_passenger_throughput = 150

        self.frequency_minimum = self.calculate_frequency_per_hour(self.minimum_throughput)
        self.frequency_off_peak = self.calculate_frequency_per_hour(self.off_peak_throughput)
        self.frequency_peak = self.calculate_frequency_per_hour(self.peak_passenger_throughput)

        self.maximum_passenger_volume = self.peak_passenger_throughput * 24
        self.route_completion_time_per_vehicle = self.calculate_route_roundtrip_minutes()
        self.average_wait_time = self.calculate_average_waiting_time_minutes()

        # I DON'T KNOWWWWWWWWWWWWW
        # self.availability = None  # TODO: Clarify? Is this from the EV?
        # self.operated_speed = None  # TODO: Clarify? Is this from the EV?

        self.score = self.calculate_mau_score()

    def calculate_frequency_per_hour(self, throughput: int, cars_per_train=1) -> float:
        # OS4 Appendix B. Thanks Wikipedia
        f = throughput / (self.LOAD_FACTOR_EXPECTED_AVG * self.vehicle.chasis.passenger_capacity * cars_per_train)
        return round(f, 4)

    def calculate_throughput(self, frequency: float, cars_per_train=1) -> float:
        # Derived from calculate_frequency_per_hour
        t = frequency * (self.LOAD_FACTOR_EXPECTED_AVG * self.vehicle.chasis.passenger_capacity * cars_per_train)
        return round(t, 4)

    def calculate_total_fleet_cost_usd(self) -> float:
        # bruh
        return round(self.vehicle.total_vehicle_cost_1k_usd * self.fleet_size, 2)

    def calculate_route_roundtrip_minutes(self) -> float:
        # t = d/r + waiting
        distance = self.route.length_km
        rate = self.vehicle.average_speed_km_per_hour
        time = distance/rate + (self.DWELL_TIME_SECONDS * self.route.stops)
        return round(time, 3)

    def calculate_average_waiting_time_minutes(self) -> float:
        # uses peak load...
        time = self.calculate_route_roundtrip_minutes() / self.frequency_peak
        return round(time, 3)

    def calculate_mau_score(self) -> float:
        mau = MultiAttributeUtility(
            daily_passenger_volume=self.maximum_passenger_volume,
            peak_passenger_throuput=self.peak_passenger_throughput,
            average_wait_time_minutes=self.average_wait_time,
            availability=self.vehicle.availability
        )
        score = mau.score
        return score

    def __str__(self) -> str:
        s = 'Fleet:\n'
        for k, v in self.__dict__.items():
            if k in {'vehicle'}:
                continue
            s += f'\t{k}: {v}\n'
        return s
