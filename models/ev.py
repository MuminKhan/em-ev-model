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
        self.passenger_capacity_to_cost_ratio = self._calculate_passenger_capacity_to_cost_ratio()

    def _calculate_total_vehicle_cost_1k_usd(self):
        total_cost = 0.0
        total_cost += self.autonomous_system.cost_1k_usd
        total_cost += self.battery_pack.cost_1k_usd
        total_cost += self.battery_charger.cost_1k_usd
        total_cost += self.chasis.cost_1k_usd
        total_cost += self.motor_and_inverter.cost_1k_usd
        return round(total_cost, 2)

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
        return round(total_weight_kg, 4)

    def _calculate_battery_charge_time_hours(self) -> float:
        """
        Battery charge time [h] = Battery Capacity [kWh] / Charger Power [kW]
        """
        charge_time_hours = self.battery_pack.capacity_kWh / self.battery_charger.power_kW
        return round(charge_time_hours, 4)

    def _calculate_power_consumption_Wh_per_km(self) -> float:
        """
        Power Consumption [Wh/km] = Nominal Power Consumption Chassis [Wh/km] + 0.1*(Total Weight [kg] - Chassis Weight [kg] ) + Added Power Consumption Autonomous System [Wh/km]
        """
        power_consumption_Wh_per_kM = self.chasis.nominal_power_consumption_Wh_per_km + \
            (0.1 * (self.total_vehicle_weight_kg - self.chasis.weight_kg)) + self.autonomous_system.added_power_consumption_Wh_per_kW
        return round(power_consumption_Wh_per_kM, 4)

    def _calculate_range_km(self) -> float:
        """
        #Range [km] = Battery Capacity [Wh] / Power Consumption [Wh/km]
        """
        wH_to_kWH = 1000
        range_km = wH_to_kWH * self.battery_pack.capacity_kWh / self.power_consumption_Wh_per_km
        return round(range_km, 4)

    def _calculate_average_speed_km_per_hour(self) -> float:
        """
        #Average Speed [km/h] = 700 * Motor Power [kW] / Total Weight [kg] 
        """
        avg_speed = 700 * self.motor_and_inverter.power_kW / self.total_vehicle_weight_kg
        return round(avg_speed, 4)

    def _calculate_uptime_hours(self) -> float:
        """
        #Up-time [h] = Range [km] / Average Speed [km/h]
        """
        uptime_hours = self.range_km / self.average_speed_km_per_hour
        return round(uptime_hours, 4)

    def _calculate_downtime_hours(self) -> float:
        """
        #Down-time [h] = Battery charge time [h] + 0.25
        """
        downtime_hours = self.battery_charge_time_hours + 0.25
        return round(downtime_hours, 4)

    def _calculate_availability(self) -> float:
        """
        Availability [dml] = Up-time / (Up-time + Down-time) 
        """
        availability = self.uptime_hours / (self.uptime_hours + self.downtime_hours)
        return round(availability, 4)

    def _calculate_passenger_capacity_to_cost_ratio(self) -> float:
        ratio = self.chasis.passenger_capacity / self.total_vehicle_cost_1k_usd
        return round(ratio, 4)

    def __str__(self) -> str:
        s = " EV ".center(50, '*')

        # Autonomous System
        s += f'\nAutonomous System\n'
        s += f'\t{"Name:":<28}{self.autonomous_system.choice.name}\n'
        s += f'\t{"Weight:":<28}{self.autonomous_system.weight_kg} kg\n'
        s += f'\t{"Cost:":<28}{"$" + str(1000*self.autonomous_system.cost_1k_usd)}\n'
        s += f'\t{"Added Power Consumption:":<28}{self.autonomous_system.added_power_consumption_Wh_per_kW} Wh/kW\n'

        # Battery Charger
        s += f'\nBattery Charger\n'
        s += f'\t{"Name:":<28}{self.battery_charger.choice.name}\n'
        s += f'\t{"Weight:":<28}{self.battery_charger.weight_kg} kg\n'
        s += f'\t{"Cost:":<28}{"$" + str(1000*self.battery_charger.cost_1k_usd)}\n'
        s += f'\t{"Power:":<28}{self.battery_charger.power_kW} kW\n'

        # Battery Pack
        s += f'\nBattery Pack\n'
        s += f'\t{"Name:":<28}{self.battery_pack.choice.name}\n'
        s += f'\t{"Weight:":<28}{self.battery_pack.weight_kg} kg\n'
        s += f'\t{"Cost:":<28}{"$" + str(1000*self.battery_pack.cost_1k_usd)}\n'
        s += f'\t{"Capacity:":<28}{self.battery_pack.capacity_kWh} kWh\n'

        # Chasis
        s += f'\nChasis\n'
        s += f'\t{"Name:":<28}{self.chasis.choice.name}\n'
        s += f'\t{"Weight:":<28}{self.chasis.passenger_capacity} passengers\n'
        s += f'\t{"Weight:":<28}{self.chasis.weight_kg} kg\n'
        s += f'\t{"Cost:":<28}{"$" + str(1000*self.chasis.cost_1k_usd)}\n'
        s += f'\t{"Nominal Power Consumption:":<28} ${self.chasis.nominal_power_consumption_Wh_per_km} Wh/km\n'

        # Motor and Inverter
        s += f'\nMotor and Inverter\n'
        s += f'\t{"Name:":<28}{self.motor_and_inverter.choice.name}\n'
        s += f'\t{"Weight:":<28}{self.motor_and_inverter.weight_kg} kg\n'
        s += f'\t{"Cost:":<28}{"$" + str(1000*self.motor_and_inverter.cost_1k_usd)}\n'
        s += f'\t{"Power:":<28}{self.motor_and_inverter.power_kW} kW\n'

        # EV Attributes
        s += f'\nEV\n'
        s += f'\t{"Total Vehicle Cost:":<28}{"$" + str(1000*self.total_vehicle_cost_1k_usd)}\n'
        s += f'\t{"Total Vehicle Weight:":<28}{self.total_vehicle_weight_kg} kg\n'
        s += f'\t{"Battery Charge Time:":<28}{self.battery_charge_time_hours} hours\n'
        s += f'\t{"Power Consumption:":<28}{self.power_consumption_Wh_per_km} Wh/km\n'
        s += f'\t{"Range:":<28}{self.range_km} km\n'
        s += f'\t{"Average Speed:":<28}{self.average_speed_km_per_hour} km/hour\n'
        s += f'\t{"Uptime:":<28}{self.uptime_hours} hours\n'
        s += f'\t{"Downtime:":<28}{self.downtime_hours} hours\n'
        s += f'\t{"Availability:":<28}{self.availability}\n'
        s += f'\t{"Passengers to Cost Ratio:":<28}{self.passenger_capacity_to_cost_ratio}\n'

        return s
