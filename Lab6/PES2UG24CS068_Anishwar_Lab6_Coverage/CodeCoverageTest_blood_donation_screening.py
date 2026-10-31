import pytest
from blood_donation_screening import process_donor_cohort, verify_storage_centrifuge

# Goal: execute every line of blood_donation_screening.py at least once (line coverage).


def make_cohort(donors, registered=True, cohort_type="standard", fast_track=False):
    return {
        "clinic_registered": registered,
        "type": cohort_type,
        "fast_track": fast_track,
        "donors": donors,
    }


GOOD_DONOR = {"age": 25, "weight_kg": 65, "hb": 14.0}


# Original example test case
def test_single_accepted_donor():
    result = process_donor_cohort([make_cohort([GOOD_DONOR])], 450)
    assert result["collected_ml"] == 450
    assert result["status"] == "ACCEPTED"


# Line 3: invalid input raises ValueError
def test_invalid_cohort_list_raises():
    with pytest.raises(ValueError):
        process_donor_cohort("not a list", 450)


# Line 10 (skip unregistered cohort) and line 41 (ZERO_YIELD)
def test_unregistered_cohort_is_skipped():
    result = process_donor_cohort([make_cohort([GOOD_DONOR], registered=False)], 450)
    assert result == {"collected_ml": 0, "status": "ZERO_YIELD"}


# Line 36: fast-track cohorts get a 50 ml bonus
def test_fast_track_adds_bonus():
    result = process_donor_cohort([make_cohort([GOOD_DONOR], fast_track=True)], 450)
    assert result == {"collected_ml": 500, "status": "ACCEPTED"}


# Lines 21-22 (age/weight deferral) and lines 30-31 (hemoglobin too high)
def test_underage_underweight_and_high_hb_are_deferred():
    donors = [
        {"age": 16, "weight_kg": 65, "hb": 14.0},
        {"age": 30, "weight_kg": 45, "hb": 14.0},
        {"age": 30, "weight_kg": 70, "hb": 18.5},
    ]
    result = process_donor_cohort([make_cohort(donors)], 450)
    assert result == {"collected_ml": 0, "status": "ZERO_YIELD"}


# Lines 25-28: low hemoglobin in a high-altitude cohort wipes the collection and stops
def test_high_altitude_low_hb_resets_collection():
    donors = [GOOD_DONOR, {"age": 30, "weight_kg": 70, "hb": 11.0}, GOOD_DONOR]
    result = process_donor_cohort([make_cohort(donors, cohort_type="high_altitude")], 450)
    assert result == {"collected_ml": 0, "status": "ZERO_YIELD"}


# Line 39: more than 4 deferrals gives HIGH_DEFERRAL
def test_high_deferral_status():
    donors = [{"age": 16, "weight_kg": 60, "hb": 14.0}] * 5 + [GOOD_DONOR]
    result = process_donor_cohort([make_cohort(donors)], 450)
    assert result == {"collected_ml": 450, "status": "HIGH_DEFERRAL"}


# Line 47: no centrifuge data
def test_centrifuge_no_data():
    assert verify_storage_centrifuge([]) == "NO_DATA"


# Lines 50-55: two consecutive low readings abort the spin
def test_centrifuge_abort_on_two_consecutive_drops():
    assert verify_storage_centrifuge([[3200, 2900, 2800, 3100]]) == "ABORT_SPIN"


# Lines 57-58: an isolated dip resets the streak and the runs are stable
def test_centrifuge_stable_with_isolated_dip():
    assert verify_storage_centrifuge([[3200, 2900, 3100], [3000, 3500]]) == "STABLE"
