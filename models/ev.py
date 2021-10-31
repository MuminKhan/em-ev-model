from models.autonomous_system import AutonomousSystem, AutonomousSystemChoice
from models.battery_charger import BatteryCharger, BatteryChargerChoice
from models.battery_pack import BatteryPack, BatteryPackChoice
from models.chasis import Chasis, ChasisChoice
from models.motor_and_inverter import MotorAndInverter, MotorAndInverterChoice


class Ev():

    def __init__(self, autonomous_system_choice: AutonomousSystemChoice = None, battery_charger_choice: BatteryChargerChoice = None, battery_pack_choice: BatteryPackChoice = None,  chasis_choice: ChasisChoice = None, motor_and_inverter_choice: MotorAndInverterChoice = None) -> None:

        # CONSTANTS
        # Average passenger weight [kg] = 100
        self.PASSENGER_WEIGHT_AVERAGE_KG = 100

        # Expected average load factor/trip = 0.75
        self.LOAD_FACTOR_EXPECTED_AVG = 0.75

        # Benchmark availability of competing systems: 0.75
        self.BENCHMARK_AVAIL_COMPETING_SYSTEMS = 0.75

        # Dwell time [s] = 60 (time for passengers get out and get in)
        self.DWELL_TIME_SECONDS = 60

        choices = (autonomous_system_choice, battery_pack_choice, battery_charger_choice, chasis_choice, motor_and_inverter_choice)
        if any(choices) is None:
            raise ValueError("Must supply choices for each: autonomous_system_choice, battery_pack_choice, battery_charger_choice, chasis_choice, motor_and_inverter_choice")

        # Subsystems
        self.autonomous_system = AutonomousSystem(autonomous_system_choice)
        self.battery_pack = BatteryPack(battery_pack_choice)
        self.battery_charger = BatteryCharger(battery_charger_choice)
        self.chasis = Chasis(chasis_choice)
        self.motor_and_inverter = MotorAndInverter(motor_and_inverter_choice)

        if self.battery_pack.weight_kg > self.chasis.weight_kg/3:
            raise ValueError("The battery pack weight shall be no greater than ⅓ of the chassis weight (this is a proxy for limited space availability).")

        # Derived Attributes
        self.total_vehicle_cost_1k_usd = self._calculate_total_vehicle_cost_1k_usd()
        self.total_vehicle_weight_kg = self._calculate_total_vehicle_weight_kg()
        self.battery_charge_time_hours = self._calculate_battery_charge_time_hours()
        self.power_consumption_Wh_per_km = self._calculate_power_consumption_Wh_per_km()
        self.range_km = self._calculate_range_km()
        self.average_speed_km_per_hour = self._calculate_average_speed_km_per_hour()
        self.uptime_hours = self._calculate_uptime_hours()
        self.downtime_hours = self._calculate_downtime_hours()
        self.availability = self._calculate_availability()

    def _calculate_total_vehicle_cost_1k_usd(self):
        total_cost = 0.0
        total_cost += self.autonomous_system.cost_1k_usd
        total_cost += self.battery_pack.cost_1k_usd
        total_cost += self.battery_charger.cost_1k_usd
        total_cost += self.chasis.cost_1k_usd
        total_cost += self.motor_and_inverter.cost_1k_usd
        return total_cost

    def _calculate_total_vehicle_weight_kg(self) -> float:
        """
        Total Vehicle Weight [kg] = Chassis Weight + Battery Weight + Charger Weight + Motor and inverter Weight + Passengers Weight + Autonomy system Weight
        """
        total_weight_kg = 0.0
        total_weight_kg += self.autonomous_system.weight_kg
        total_weight_kg += self.battery_pack.weight_kg
        total_weight_kg += self.battery_charger.weight_kg
        total_weight_kg += self.chasis.weight_kg
        total_weight_kg += self.motor_and_inverter.weight_kg
        return total_weight_kg

    def _calculate_battery_charge_time_hours(self) -> float:
        """
        Battery charge time [h] = Battery Capacity [kWh] / Charger Power [kW]
        """
        charge_time_hours = self.battery_pack.capacity_kWh / self.battery_charger.power_kW
        return charge_time_hours

    def _calculate_power_consumption_Wh_per_km(self) -> float:
        """
        Power Consumption [Wh/km] = Nominal Power Consumption Chassis [Wh/km] + 0.1*(Total Weight [kg] - Chassis Weight [kg] ) + Added Power Consumption Autonomous System [Wh/km]
        """
        power_consumption_Wh_per_kM = self.chasis.nominal_power_consumption_Wh_per_km + (0.1 * (self.total_vehicle_weight_kg - self.chasis.weight_kg)) + self.autonomous_system.added_power_consumption_Wh_per_kW
        return power_consumption_Wh_per_kM

    def _calculate_range_km(self) -> float:
        """
        #Range [km] = Battery Capacity [Wh] / Power Consumption [Wh/km]
        """
        wH_to_kWH = 1000
        range_km = wH_to_kWH * self.battery_pack.capacity_kWh / self.power_consumption_Wh_per_km
        return range_km

    def _calculate_average_speed_km_per_hour(self) -> float:
        """
        #Average Speed [km/h] = 700 * Motor Power [kW] / Total Weight [kg] 
        """
        avg_speed = 700 * self.motor_and_inverter.power_kW / self.total_vehicle_weight_kg
        return avg_speed

    def _calculate_uptime_hours(self) -> float:
        """
        #Up-time [h] = Range [km] / Average Speed [km/h]
        """
        uptime_hours = self.range_km / self.average_speed_km_per_hour
        return uptime_hours

    def _calculate_downtime_hours(self) -> float:
        """
        #Down-time [h] = Battery charge time [h] + 0.25
        """
        downtime_hours = self.battery_charge_time_hours + 0.25
        return downtime_hours

    def _calculate_availability(self) -> float:
        """
        Availability [dml] = Up-time / (Up-time + Down-time) 
        """
        return self.uptime_hours / (self.uptime_hours + self.downtime_hours)

    def calculate_total_fleet_cost_usd(self, number_of_vehicles: int) -> float:
        return self.total_vehicle_cost_1k_usd * number_of_vehicles
