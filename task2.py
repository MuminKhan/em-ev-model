"""
Create the design vector and system model using the information provided in the appendices to represent the MIT/Kendall Square autonomous surface transportation system. 
Create also a constants vector to manage inputs and constants for your model. 
Test your model to verify that it doesn’t break down across the range of the system attributes you will be modeling.

Note the unit of analysis for this model – the surface transportation system. 
That means that in addition to the vehicle characteristics, you will have to explore a range of fleet sizes. 
Use your judgment to determine the appropriate range of potential vehicles in the fleet and the size of the increment between the size groupings that you choose to model (e.g., in increments of 1, 5, 10 vehicles, and so forth). Your surface transportation system model will also draw on fundamentals of transportation system design (see Appendix B).

As you develop your model, you will need to select a primary use case (from one of your reports from OS3 — briefly state what the use case is). 
This use case will lay out a specific operating route (and routines). 
You will want to put the characteristics of the model that are unique to this use case in the constants vector.

Make sure your model is well documented, i.e. assumptions are clear, the equations are defined with consistent units. 
Prepare write-ups or partial tables as needed to demonstrate to a technically competent peer or supervisor that your model has been verified and validated and is ready to be used to generate valid architectures. 

In addition to the model documentation, create a table that describes 5 unique architecture instances (of your choice) that includes this information used and/or produced by your model:
•	Fleet size (number of vehicles).
•	Vehicle specifications (the design variables—from Appendix C—used in the specific architecture instance).
•	Intermediate performance variables for each architecture instance:
    o	Vehicle speed and range; fleet throughput, average wait time, and availability.
•	Vehicle and fleet cost.
"""

from models.autonomous_system import AutonomousSystemChoice
from models.battery_charger import BatteryChargerChoice
from models.battery_pack import BatteryPackChoice
from models.chasis import ChasisChoice
from models.ev import Ev
from models.fleet import Fleet
from models.motor_and_inverter import MotorAndInverterChoice

from itertools import product

"""
csv_header = ['id', 'PASSENGER_WEIGHT_AVERAGE_KG', 'LOAD_FACTOR_EXPECTED_AVG', 'BENCHMARK_AVAIL_COMPETING_SYSTEMS', 'DWELL_TIME_SECONDS', 'autonomous_system', 'battery_pack', 'battery_charger', 'chasis', 'motor_and_inverter',
              'total_vehicle_cost_1k_usd', 'total_vehicle_weight_kg', 'battery_charge_time_hours', 'power_consumption_Wh_per_km', 'range_km', 'average_speed_km_per_hour', 'uptime_hours', 'downtime_hours', 'availability']
bad_row = ', '.join(['-1'] * (len(csv_header) - 1))

print(', '.join(csv_header))

cycles = 0
for autonomy, bcharger, bpack, chasis, motor in product(list(AutonomousSystemChoice), list(BatteryChargerChoice), list(BatteryPackChoice), list(ChasisChoice), list(MotorAndInverterChoice)):
    

    #print('*'*10, f'{cycles}: {autonomy.name}, {bcharger.name}, {bpack.name}, {chasis.name}, {motor.name}',  '*'*10)
    
    try:
        ev = Ev(
            autonomous_system_choice=autonomy,
            battery_charger_choice=bcharger,
            battery_pack_choice=bpack,
            chasis_choice=chasis,
            motor_and_inverter_choice=motor
        )
        cycles += 1
        print(ev)
    except ValueError as e:
        #print(bad_row, end='')
        pass

    if cycles >= 10:
        exit()
"""

car = Ev(
    autonomous_system_choice=AutonomousSystemChoice.A3,
    battery_charger_choice=BatteryChargerChoice.G1,
    battery_pack_choice=BatteryPackChoice.P3,
    motor_and_inverter_choice=MotorAndInverterChoice.M3,
    chasis_choice=ChasisChoice.C7
)

fleet = Fleet(car, 50)

print(fleet)