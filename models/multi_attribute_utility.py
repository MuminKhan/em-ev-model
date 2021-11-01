class MultiAttributeUtility:
    """
    MultiAttributeUtility Class
    """

    def __init__(self, name, passenger_volume, peak_passenger_throuput, average_wait_time_minutes, availability) -> None:

        self.WEIGHT_PASSENGER_VOLUME = 0.15
        self.WEIGHT_PEAK_PASSENGER_THROUGHPUT = 0.25
        self.WEIGHT_AVERAGE_WAIT_TIME = 0.35
        self.WEIGHT_AVAILABILITY = 0.25

        if passenger_volume < 0:
            raise ValueError(f"passenger_volume must be greater than 0, not {passenger_volume}")

        if peak_passenger_throuput < 0:
            raise ValueError(f"peak_passenger_throuput must be greater than 0, not {peak_passenger_throuput}")

        if average_wait_time_minutes < 0:
            raise ValueError(f"average_wait_time_minutes must be greater than 0, not {average_wait_time_minutes}")

        if availability < 0:
            raise ValueError(f"availability must be greater than 0, not {availability}")

        self.name = name
        self.passenger_volume = passenger_volume
        self.peak_passenger_throuput = peak_passenger_throuput
        self.average_wait_time_minutes = average_wait_time_minutes
        self.availability = availability
        self.mau = self._calculate_weighted_sum_mau()


    def utility_passenger_volume(self, passenger_volume=None) -> float:
        if passenger_volume is None:
            passenger_volume = self.passenger_volume
        if passenger_volume < 0:
            raise ValueError("passenger_volume must be greater than 0.")

        util_map = {
            0: 0.0,
            1: 0.2,
            2: 0.4,
            3: 0.8,
            4: 1.0,
        }

        utility = util_map.get(passenger_volume // 500, 1.0)
        return utility

    def utility_avg_wait_time(self, average_wait_time_minutes=None) -> float:
        if average_wait_time_minutes is None:
            average_wait_time_minutes = self.average_wait_time_minutes
        if average_wait_time_minutes < 0:
            raise ValueError("average_wait_time_minutes must be greater than 0.")

        util_map = {
            0: 1.0,
            1: 0.95,
            2: 0.75,
            3: 0.40,
            4: 0.20,
            6: 0
        }

        utility = util_map.get(average_wait_time_minutes // 5, 0)
        return utility

    def utility_peak_passenger_throughput(self, peak_passenger_throuput=None) -> float:
        if peak_passenger_throuput is None:
            peak_passenger_throuput = self.peak_passenger_throuput
        if peak_passenger_throuput < 0:
            raise ValueError("peak_passenger_throuput must be greater than 0.")

        util_map = {
            0:   0,
            1: 0.2,
            2: 0.5,
            3: 0.9,
            4: 1.0,
        }

        utility = util_map.get(peak_passenger_throuput // 50, 1.0)
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
            1.0: 1.0,
        }

        utility = util_map.get(availability, 1.0)
        return utility

    def _calculate_weighted_sum_mau(self):
        pvol = self.WEIGHT_PASSENGER_VOLUME * self.utility_passenger_volume()
        pthrough = self.WEIGHT_PEAK_PASSENGER_THROUGHPUT * self.utility_peak_passenger_throughput()
        wait = self.WEIGHT_AVERAGE_WAIT_TIME * self.utility_avg_wait_time()
        avail = self.WEIGHT_AVAILABILITY * self.utility_availibility_dml3()

        mau = round(sum((pvol, pthrough, wait, avail)), 3)
        print(f'{pvol} + {pthrough} + {wait} + {avail} = {mau}')
        return mau

    def __str__(self) -> str:
        s = '*' * 20 + '\n'
        s += f'{"CASE NAME:           ":<15}{self.name:>8}\n'
        s += f'{"PASSENGER VOLUME:    ":<15}{self.passenger_volume:>8}\n'
        s += f'{"PASSENGER THROUGHPUT:":<15}{self.peak_passenger_throuput:>8}\n'
        s += f'{"AVERAGE WAIT TIME:   ":<15}{self.average_wait_time_minutes:>8}\n'
        s += f'{"AVAILABILITY:        ":<15}{self.availability:>8}\n'
        s += f'{"MAU:                 ":<15}{self.mau:>8}\n'

        return s
