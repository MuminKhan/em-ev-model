import math

from models.ev import Ev
from models.multi_attribute_utility import MultiAttributeUtility
from models.route import Route


class Fleet:
    """
    :class:`Fleet` represents an n number of vehicle fleet of :class:`Ev` and its derived properties. 
    """

    def __init__(self, route: Route, ev: Ev, fleet_size: int = None, peak_throughput_target: int = None) -> None:
        """
        Creates the :class:`Fleet` class. 

        :param route: :class:`Route` of route information
        :type route: :class:`Route`
        :param ev: :class:`Ev` object that fleet should be comprised of
        :type ev: :class:`Ev`
        :param fleet_size: Size of fleet
        :type fleet_size: int
        
        
        """

        # Parameter validation
        if type(route) is not Route:
            raise ValueError(f'route argument must be of type route rather than supplied {type(route)}')
        if type(ev) is not Ev:
            raise ValueError(f'ev argument must be of type Ev rather than supplied {type(ev)}')
        if fleet_size is None and peak_throughput_target is None:
            raise AttributeError("Please either specify a fleet_size value or peak_throughput_target")
        if fleet_size is not None and type(fleet_size) is not int:
            raise AttributeError(f"fleet_size must be of type int.")

        # CONSTANTS
        # Average passenger weight [kg] = 100
        self._PASSENGER_WEIGHT_AVERAGE_KG = 100

        # Expected average load factor/trip = 0.75
        self._LOAD_FACTOR_EXPECTED_AVG = 0.75

        # Benchmark availability of competing systems: 0.75
        self._BENCHMARK_AVAIL_COMPETING_SYSTEMS = 0.75

        # Dwell time [s] = 60 (time for passengers get out and get in)
        self._DWELL_TIME_SECONDS = 60

        self._FLEET_BUFFER_VEHICLES = 0

        # Derived Parameters
        self.route = route
        self.vehicle = ev

        self.peak_throughput_target = peak_throughput_target
        self.route_completion_time_per_vehicle_minutes = self.calculate_route_roundtrip_minutes()

        self.fleet_size = fleet_size if fleet_size is not None else self.optimize_ideal_fleet_size()
        self.fleet_cost_1k_usd = self.calculate_total_fleet_cost_usd()

        self.average_wait_time_minutes = self.calculate_average_waiting_time_minutes()
        self.peak_hourly_passenger_throughput = self.calculate_throughput(self.fleet_size)
        self.maximum_passenger_volume = self.calculate_maximum_passenger_volume()
        self.frequency_peak = self.calculate_frequency_per_hour(self.peak_hourly_passenger_throughput)

        self.score = self.calculate_mau_score()

    def calculate_frequency_per_hour(self, throughput: int, cars_per_train=1) -> float:
        # OS4 Appendix B. Thanks Wikipedia
        # will give you the number of vehicles required to service a route given a throughput target
        f = throughput / (self._LOAD_FACTOR_EXPECTED_AVG * self.vehicle.chasis.passenger_capacity * cars_per_train)
        return round(f, 4)

    def calculate_route_roundtrip_minutes(self) -> float:
        # t = d/r + waiting
        distance = self.route.length_km
        rate = self.vehicle.operated_speed_km_hour
        time = (60*distance/rate) + (round(self._DWELL_TIME_SECONDS/60, 2) * self.route.stops)
        return round(time, 3)

    def calculate_maximum_passenger_volume(self):
        # sum of passengers in peak and non-peak hours
        return self.peak_hourly_passenger_throughput * 24 * self.vehicle.availability

    def calculate_throughput(self, fleet_size) -> int:
        pass_per_stop = math.floor(self.vehicle.chasis.passenger_capacity * self._LOAD_FACTOR_EXPECTED_AVG * fleet_size)
        cycles = 60 / (self.route_completion_time_per_vehicle_minutes / fleet_size)
        calculated_throughput = math.floor(pass_per_stop * cycles)
        return calculated_throughput

    def optimize_ideal_fleet_size(self) -> int:
        fleet_size = 0
        calculated_throughput = 0
        while calculated_throughput < self.peak_throughput_target:
            fleet_size += 1
            calculated_throughput = self.calculate_throughput(fleet_size)
        return fleet_size + self._FLEET_BUFFER_VEHICLES

    def calculate_total_fleet_cost_usd(self) -> float:
        cost_in_thousands = self.vehicle.total_vehicle_cost_1k_usd * self.fleet_size
        return cost_in_thousands

    def calculate_average_waiting_time_minutes(self) -> float:
        # uses peak load...
        time = self.calculate_route_roundtrip_minutes() / self.fleet_size
        return round(time, 3)

    def calculate_mau_score(self) -> float:
        mau = MultiAttributeUtility(
            daily_passenger_volume=self.maximum_passenger_volume,
            peak_passenger_throuput=self.peak_hourly_passenger_throughput,
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
