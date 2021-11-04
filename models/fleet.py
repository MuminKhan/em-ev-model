import math

from models.ev import Ev
from models.multi_attribute_utility import MultiAttributeUtility
from models.route import Route


class Fleet:

    def __init__(self, route: Route, ev: Ev, fleet_size: int = -1) -> None:
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
        self._PASSENGER_WEIGHT_AVERAGE_KG = 100

        # Expected average load factor/trip = 0.75
        self._LOAD_FACTOR_EXPECTED_AVG = 0.75

        # Benchmark availability of competing systems: 0.75
        self._BENCHMARK_AVAIL_COMPETING_SYSTEMS = 0.75

        # Dwell time [s] = 60 (time for passengers get out and get in)
        self._DWELL_TIME_SECONDS = 60

        # Desired maximum waiting time for transportation on-site, Table 1
        self._DESIRED_WAIT_TIME = 5

        # Derived Parameters
        self.route = route
        self.vehicle = ev

        self.off_peak_throughput = 50
        self.peak_passenger_throughput = 150
        self.operated_speed_km_hour = 32

        self.frequency_off_peak = self.calculate_frequency_per_hour(self.off_peak_throughput)
        self.frequency_peak = self.calculate_frequency_per_hour(self.peak_passenger_throughput)

        self.maximum_passenger_volume = self.calculate_maximum_passenger_volume()
        self.route_completion_time_per_vehicle_minutes = self.calculate_route_roundtrip_minutes()

        self.fleet_size = fleet_size if fleet_size > 0 else self.calculate_ideal_fleet_size()
        self.fleet_cost_1M_usd = self.calculate_total_fleet_cost_usd()

        self.average_wait_time_minutes = self.calculate_average_waiting_time_minutes()

        # I DON'T KNOWWWWWWWWWWWWW
        # self.availability = None  # TODO: Clarify? Is this from the EV?
        # self.operated_speed = None  # TODO: Clarify? Is this from the EV?

        self.score = self.calculate_mau_score()

    def calculate_route_roundtrip_minutes(self) -> float:
        # t = d/r + waiting
        distance = self.route.length_km
        rate = min(self.vehicle.average_speed_km_per_hour, self.operated_speed_km_hour)
        time = (60*distance/rate) + (round(self._DWELL_TIME_SECONDS/60, 2) * self.route.stops)
        return round(time, 3)

    def calculate_ideal_fleet_size(self) -> int:
        # gives you b
        fleet = self.peak_passenger_throughput / ((60/self._DESIRED_WAIT_TIME) * self._LOAD_FACTOR_EXPECTED_AVG * self.vehicle.chasis.passenger_capacity)
        fleet = math.ceil(fleet)
        return fleet if fleet >= 3 else 3

    def calculate_maximum_passenger_volume(self):
        # sum of passengers in peak and non-peak hours
        peak_hours = 4
        off_peak_hours = 24-peak_hours
        return (self.peak_passenger_throughput * peak_hours) + (self.off_peak_throughput * off_peak_hours)

    def calculate_frequency_per_hour(self, throughput: int, cars_per_train=1) -> float:
        # OS4 Appendix B. Thanks Wikipedia
        # will give you the number of vehicles required to service a route given a throughput target
        f = throughput / (self._LOAD_FACTOR_EXPECTED_AVG * self.vehicle.chasis.passenger_capacity * cars_per_train)
        return round(f, 4)

    def calculate_throughput(self, frequency: float, cars_per_train=1) -> float:
        # Derived from calculate_frequency_per_hour
        # given a frequency, get throughput
        t = frequency * (self._LOAD_FACTOR_EXPECTED_AVG * self.vehicle.chasis.passenger_capacity * cars_per_train)
        return round(t, 4)

    def calculate_total_fleet_cost_usd(self) -> float:
        cost_in_thousands = self.vehicle.total_vehicle_cost_1k_usd * self.fleet_size
        cost_in_millions = cost_in_thousands / 1000
        return round(cost_in_millions, 3)

    def calculate_average_waiting_time_minutes(self) -> float:
        # uses peak load...
        time = self.calculate_route_roundtrip_minutes() / self.fleet_size
        return round(time, 3)

    def calculate_mau_score(self) -> float:
        mau = MultiAttributeUtility(
            daily_passenger_volume=self.maximum_passenger_volume,
            peak_passenger_throuput=self.peak_passenger_throughput,
            average_wait_time_minutes=self.average_wait_time_minutes,
            availability=self.vehicle.availability
        )
        score = mau.score
        return score

    def to_dict(self) -> dict:
        # fleet
        d = {k: v for k, v in self.__dict__.items() if k[0] != '_' and k not in ('route', 'vehicle')}

        # route
        route = {k: v for k, v in self.route.__dict__.items() if k[0] != '_'}
        d.update(route)

        # ev and subsystems
        ev = {k: v for k, v in self.vehicle.__dict__.items() if k[0] != '_'}
        for subsystem_str, subsystem in self.vehicle.subsystems.items():
            elements = {f'{subsystem_str}_{k}': v for k, v in subsystem.__dict__.items() if k[0] != '_' and k != 'choice'}
            elements[subsystem_str] = subsystem.choice.name
            ev.update(elements)
        
        ev.pop("subsystems")
        d.update(ev)

        return d

    def __str__(self) -> str:
        s = 'Fleet:\n'
        for k, v in self.__dict__.items():
            if k in {'vehicle'}:
                continue
            s += f'\t{k}: {v}\n'
        return s
