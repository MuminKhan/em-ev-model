import pytest
import sys

print(sys.path)

from models.multi_attribute_utility import MultiAttributeUtility



@pytest.fixture
def test_case():
    t = MultiAttributeUtility(
        name="CASE TEST",
        daily_passenger_volume=0,
        peak_passenger_throuput=0,
        average_wait_time_minutes=0,
        availability=0
    )

    return t


def test_model_weights(test_case):
    assert test_case.WEIGHT_PASSENGER_VOLUME == 0.15
    assert test_case.WEIGHT_PEAK_PASSENGER_THROUGHPUT == 0.25
    assert test_case.WEIGHT_AVERAGE_WAIT_TIME == 0.35
    assert test_case.WEIGHT_AVAILABILITY == 0.25


def test_passenger_volume_utility(test_case):
    assert test_case.utility_passenger_volume(0) == 0.0
    assert test_case.utility_passenger_volume(500) == 0.2
    assert test_case.utility_passenger_volume(1000) == 0.4
    assert test_case.utility_passenger_volume(1500) == 0.8
    assert test_case.utility_passenger_volume(2000) == 1.0
    assert test_case.utility_passenger_volume(8888) == 1.0

    with pytest.raises(ValueError):
        test_case.utility_passenger_volume(-1)


def test_avg_wait_time_utility(test_case):
    assert test_case.utility_avg_wait_time(0) == 1.0
    assert test_case.utility_avg_wait_time(5) == 0.95
    assert test_case.utility_avg_wait_time(10) == 0.75
    assert test_case.utility_avg_wait_time(15) == 0.4
    assert test_case.utility_avg_wait_time(20) == 0.2
    assert test_case.utility_avg_wait_time(30) == 0

    with pytest.raises(ValueError):
        test_case.utility_avg_wait_time(-1)


def test_peak_passenger_throughput_utility(test_case):
    assert test_case.utility_peak_passenger_throughput(0) == 0.0
    assert test_case.utility_peak_passenger_throughput(50) == 0.2
    assert test_case.utility_peak_passenger_throughput(100) == 0.5
    assert test_case.utility_peak_passenger_throughput(150) == 0.9
    assert test_case.utility_peak_passenger_throughput(200) == 1.0
    assert test_case.utility_peak_passenger_throughput(999) == 1.0

    with pytest.raises(ValueError):
        test_case.utility_peak_passenger_throughput(-1)


def test_availibility_dml3_utility(test_case):
    assert test_case.utility_availibility_dml3(0.0) == 0.0
    assert test_case.utility_availibility_dml3(0.2) == 0.2
    assert test_case.utility_availibility_dml3(0.4) == 0.4
    assert test_case.utility_availibility_dml3(0.6) == 0.6
    assert test_case.utility_availibility_dml3(0.8) == 0.8
    assert test_case.utility_availibility_dml3(1.0) == 1.0
    assert test_case.utility_availibility_dml3(10.0) == 1.0

    with pytest.raises(ValueError):
        test_case.utility_availibility_dml3(-1)
