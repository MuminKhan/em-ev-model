

class MultiAttributeUtility:
    """
    :class:`MultiAttributeUtility` class will calculate the weighted sum of an :class:`Ev` configuration. 
    """

    def __init__(self, daily_passenger_volume, peak_passenger_throuput, average_wait_time_minutes, availability, name='', explain=False) -> None:

        self.WEIGHT_PASSENGER_VOLUME = 0.15
        self.WEIGHT_PEAK_PASSENGER_THROUGHPUT = 0.25
        self.WEIGHT_AVERAGE_WAIT_TIME = 0.35
        self.WEIGHT_AVAILABILITY = 0.25

        if daily_passenger_volume < 0:
            raise ValueError(f"passenger_volume must be greater than 0, not {daily_passenger_volume}")

        if peak_passenger_throuput < 0:
            raise ValueError(f"peak_passenger_throuput must be greater than 0, not {peak_passenger_throuput}")

        if average_wait_time_minutes < 0:
            raise ValueError(f"average_wait_time_minutes must be greater than 0, not {average_wait_time_minutes}")

        if availability < 0:
            raise ValueError(f"availability must be greater than 0, not {availability}")

        self.name: str = name
        self._explain: bool = explain
        self.daily_passenger_volume: int = daily_passenger_volume
        self.peak_passenger_throuput: int = peak_passenger_throuput
        self.average_wait_time_minutes: float = average_wait_time_minutes
        self.availability: float = availability
        self.score: float = self._calculate_weighted_sum_mau()

    def interpolate(self, x: float, util_map: dict) -> float:
        p1 = p2 = list(util_map.items())[0]
        for k, v in util_map.items():
            if k <= x:
                p1 = (k, v)
            if k >= x:
                p2 = (k, v)
                break
        else:
            p2 = p1

        if p1 == p2:
            return p1[1]

        x1, y1 = p1
        x2, y2 = p2
        val = round(y1 + (x - x1) * (y2 - y1)/(x2 - x1), 4)

        if self._explain:
            print(f'INTERPOLATING {x} between {p1} and {p2} => ({x}. {val})')

        return val

    def utility_passenger_volume(self, passenger_volume=None) -> float:
        if passenger_volume is None:
            passenger_volume = self.daily_passenger_volume
        if passenger_volume < 0:
            raise ValueError("passenger_volume must be greater than 0.")

        util_map = {
            0: 0.0,
            500: 0.2,
            1000: 0.4,
            1500: 0.8,
            2000: 1.0
        }

        utility = self.interpolate(passenger_volume, util_map)

        if self._explain:
            print(f'passenger_volume value of {passenger_volume} is {utility} utility')

        return utility

    def utility_avg_wait_time(self, average_wait_time_minutes=None) -> float:
        if average_wait_time_minutes is None:
            average_wait_time_minutes = self.average_wait_time_minutes
        if average_wait_time_minutes < 0:
            raise ValueError("average_wait_time_minutes must be greater than 0.")

        util_map = {
            0: 1.0,
            5: 0.95,
            10: 0.75,
            15: 0.40,
            20: 0.20,
            30: 0.0
        }

        utility = self.interpolate(average_wait_time_minutes, util_map)
        if self._explain:
            print(f'average_wait_time_minutes value of {average_wait_time_minutes} is {utility} utility')
        return utility

    def utility_peak_passenger_throughput(self, peak_passenger_throuput=None) -> float:
        if peak_passenger_throuput is None:
            peak_passenger_throuput = self.peak_passenger_throuput
        if peak_passenger_throuput < 0:
            raise ValueError("peak_passenger_throuput must be greater than 0.")

        util_map = {
            0:   0,
            50: 0.2,
            100: 0.5,
            150: 0.9,
            200: 1.0
        }

        utility = self.interpolate(peak_passenger_throuput, util_map)
        if self._explain:
            print(f'peak_passenger_throuput value of {peak_passenger_throuput} is {utility} utility')
        return utility

    def utility_availibility_dml3(self, availability=None) -> float:
        if availability is None:
            availability = self.availability
        if availability < 0:
            raise ValueError("availability must be greater than 0.")

        util_map = {
            0.0: 0.0,
            0.2: 0.2,
            0.4: 0.4,
            0.6: 0.6,
            0.8: 0.8,
            1.0: 1.0
        }

        utility = self.interpolate(availability, util_map)
        if self._explain:
            print(f'availability value of {availability} is {availability} utility')
        return utility

    def _calculate_weighted_sum_mau(self):
        pvol = self.WEIGHT_PASSENGER_VOLUME * self.utility_passenger_volume()
        pthrough = self.WEIGHT_PEAK_PASSENGER_THROUGHPUT * self.utility_peak_passenger_throughput()
        wait = self.WEIGHT_AVERAGE_WAIT_TIME * self.utility_avg_wait_time()
        avail = self.WEIGHT_AVAILABILITY * self.utility_availibility_dml3()

        mau = round(sum((pvol, pthrough, wait, avail)), 4)
        mau = max(0.0, min(1.0, mau))

        if self._explain:
            print(f'{self.WEIGHT_PASSENGER_VOLUME} * {self.utility_passenger_volume()} = {pvol}')
            print(f'{self.WEIGHT_PEAK_PASSENGER_THROUGHPUT} * {self.utility_peak_passenger_throughput()} = {pthrough}')
            print(f'{self.WEIGHT_AVERAGE_WAIT_TIME} * {self.WEIGHT_AVERAGE_WAIT_TIME} = {wait}')
            print(f'{self.WEIGHT_AVAILABILITY} * {self.utility_availibility_dml3()} = {avail}')
            print(f'{pvol} + {pthrough} + {wait} + {avail} = {mau}')

        return mau

    def __str__(self) -> str:
        s = '*' * 20 + '\n'
        s += f'{"CASE NAME:           ":<15}{self.name:>8}\n'
        s += f'{"PASSENGER VOLUME:    ":<15}{self.daily_passenger_volume:>8}\n'
        s += f'{"PASSENGER THROUGHPUT:":<15}{self.peak_passenger_throuput:>8}\n'
        s += f'{"AVERAGE WAIT TIME:   ":<15}{self.average_wait_time_minutes:>8}\n'
        s += f'{"AVAILABILITY:        ":<15}{self.availability:>8}\n'
        s += f'{"MAU:                 ":<15}{self.score:>8}\n'

        return s
