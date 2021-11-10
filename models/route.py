

class Route:
    """
    :class:`Route`: Describes the route that a :class:`Fleet` is expected to run on. Used for :class:`Fleet` initialization.
    """

    def __init__(self, length_km: float, number_stops: int) -> None:
        self.length_km = length_km
        self.stops = number_stops

    def __str__(self) -> str:
        s = '\n'
        s += f'\t\tLength: {self.length_km} km\n'
        s += f'\t\tStops:  {self.stops}'
        return s
