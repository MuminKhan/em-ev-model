"""
OS4 H2T11 Task 1
"""

from models.multi_attribute_utility import MultiAttributeUtility

"""
Based on stakeholder interviews in the MIT/Kendall Square area, researchers have defined single attribute utility for each of the system attributes represented in the level 0 requirements. They have also collected data on the relative importance assigned by the representatives to those attributes. (See Appendix A for both).

Create a multi-attribute utility (MAU) function using the utility data provided in Appendix A. Use the MAU function to calculate multi-attribute utilities for these combinations of attributes seen in three different architecture cases:

Surface transportation System Attribute	    Case A	Case B	Case C
Passenger Volume	                        1000	2000	750
Peak Passenger Throughput	                75	    100	    75
Average wait time, at MIT/Kendall node 	    8	    12	    6
Availability	                            0.7	    0.6	    0.8
"""


case_a = MultiAttributeUtility(
    name = "CASE A",
    passenger_volume = 1000,
    peak_passenger_throuput = 75,
    average_wait_time_minutes = 8,
    availability = 0.7
)

case_b = MultiAttributeUtility(
    name = "CASE B",
    passenger_volume = 2000,
    peak_passenger_throuput = 100,
    average_wait_time_minutes = 12,
    availability = 0.6
)

case_c = MultiAttributeUtility(
    name = "CASE C",
    passenger_volume = 750,
    peak_passenger_throuput = 75,
    average_wait_time_minutes = 6,
    availability = 0.8
)

print(case_a)
print(case_b)
print(case_c)