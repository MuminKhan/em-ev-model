

class Route:

    def __init__(self, length_km: float, number_stops:int) -> None:
        self.length_km = length_km 
        self.stops = number_stops

    def __str__(self) -> str:
        s = '\n'
        s += f'\t\tLength: {self.length_km} km\n'
        s += f'\t\tStops:  {self.stops}'
        return s