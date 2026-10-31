import pytest
from blood_donation_screening import process_donor_cohort, verify_storage_centrifuge

# Goal: make every decision in blood_donation_screening.py go both ways (branch coverage),
# including loops that run zero times, boundary values and default (missing) keys.


def make_cohort(donors, registered=True, cohort_type="standard", fast_track=False):
    return {
        "clinic_registered": registered,
        "type": cohort_type,
        "fast_track": fast_track,
        "donors": donors,
    }


GOOD_DONOR = {"age": 25, "weight_kg": 65, "hb": 14.0}


# ---------- process_donor_cohort: input validation (line 2) ----------

def test_single_accepted_donor():
    result = process_donor_cohort([make_cohort([GOOD_DONOR])], 450)
    assert result == {"collected_ml": 450, "status": "ACCEPTED"}


def test_invalid_cohort_list_raises():
    with pytest.raises(ValueError):
        process_donor_cohort("not a list", 450)


@pytest.mark.parametrize("volume", [0, -100])
def test_non_positive_volume_raises(volume):
    with pytest.raises(ValueError):
        process_donor_cohort([make_cohort([GOOD_DONOR])], volume)


# ---------- cohort loop (lines 8, 9, 15, 35) ----------

def test_empty_cohort_list_is_zero_yield():
    # outer for-loop body never runs
    assert process_donor_cohort([], 450) == {"collected_ml": 0, "status": "ZERO_YIELD"}


def test_unregistered_cohort_is_skipped():
    result = process_donor_cohort([make_cohort([GOOD_DONOR], registered=False)], 450)
    assert result == {"collected_ml": 0, "status": "ZERO_YIELD"}


def test_missing_clinic_registered_defaults_to_skipped():
    result = process_donor_cohort([{"donors": [GOOD_DONOR]}], 450)
    assert result == {"collected_ml": 0, "status": "ZERO_YIELD"}


def test_registered_cohort_without_donors():
    # inner for-loop body never runs; type and donors use their defaults
    result = process_donor_cohort([{"clinic_registered": True}], 450)
    assert result == {"collected_ml": 0, "status": "ZERO_YIELD"}


def test_fast_track_adds_bonus():
    result = process_donor_cohort([make_cohort([GOOD_DONOR], fast_track=True)], 450)
    assert result == {"collected_ml": 500, "status": "ACCEPTED"}


def test_fast_track_bonus_alone_is_accepted():
    # no donor gives blood but the fast-track bonus still makes the total non-zero
    result = process_donor_cohort([make_cohort([], fast_track=True)], 450)
    assert result == {"collected_ml": 50, "status": "ACCEPTED"}


def test_mixed_cohorts_are_summed():
    cohorts = [
        make_cohort([GOOD_DONOR], fast_track=True),
        make_cohort([GOOD_DONOR], registered=False),
        make_cohort([GOOD_DONOR, GOOD_DONOR]),
    ]
    assert process_donor_cohort(cohorts, 450) == {"collected_ml": 1400, "status": "ACCEPTED"}


# ---------- donor eligibility (line 20) ----------

@pytest.mark.parametrize("donor", [
    {"age": 16, "weight_kg": 65, "hb": 14.0},   # age < 17
    {"age": 30, "weight_kg": 49, "hb": 14.0},   # weight < 50
    {},                                         # missing keys default to 0
])
def test_ineligible_donor_is_deferred(donor):
    result = process_donor_cohort([make_cohort([donor])], 450)
    assert result == {"collected_ml": 0, "status": "ZERO_YIELD"}


def test_age_and_weight_boundaries_are_eligible():
    donor = {"age": 17, "weight_kg": 50, "hb": 14.0}
    result = process_donor_cohort([make_cohort([donor])], 450)
    assert result == {"collected_ml": 450, "status": "ACCEPTED"}


# ---------- hemoglobin checks (lines 24, 26, 29) ----------

def test_low_hb_in_standard_cohort_only_defers_that_donor():
    donors = [GOOD_DONOR, {"age": 30, "weight_kg": 70, "hb": 12.0}, GOOD_DONOR]
    result = process_donor_cohort([make_cohort(donors)], 450)
    assert result == {"collected_ml": 900, "status": "ACCEPTED"}


def test_high_altitude_low_hb_resets_collection():
    donors = [GOOD_DONOR, {"age": 30, "weight_kg": 70, "hb": 11.0}, GOOD_DONOR]
    result = process_donor_cohort([make_cohort(donors, cohort_type="high_altitude")], 450)
    assert result == {"collected_ml": 0, "status": "ZERO_YIELD"}


def test_high_altitude_reset_still_gets_fast_track_bonus():
    donors = [GOOD_DONOR, {"age": 30, "weight_kg": 70, "hb": 11.0}]
    cohort = make_cohort(donors, cohort_type="high_altitude", fast_track=True)
    assert process_donor_cohort([cohort], 450) == {"collected_ml": 50, "status": "ACCEPTED"}


def test_high_hb_is_deferred():
    donors = [{"age": 30, "weight_kg": 70, "hb": 18.5}]
    result = process_donor_cohort([make_cohort(donors)], 450)
    assert result == {"collected_ml": 0, "status": "ZERO_YIELD"}


def test_hb_boundaries_are_accepted():
    donors = [
        {"age": 30, "weight_kg": 70, "hb": 12.5},
        {"age": 30, "weight_kg": 70, "hb": 18.0},
    ]
    result = process_donor_cohort([make_cohort(donors)], 450)
    assert result == {"collected_ml": 900, "status": "ACCEPTED"}


# ---------- final status (lines 38, 40) ----------

def test_high_deferral_status():
    donors = [{"age": 16, "weight_kg": 60, "hb": 14.0}] * 5 + [GOOD_DONOR]
    result = process_donor_cohort([make_cohort(donors)], 450)
    assert result == {"collected_ml": 450, "status": "HIGH_DEFERRAL"}


def test_exactly_four_deferrals_is_not_high_deferral():
    donors = [{"age": 16, "weight_kg": 60, "hb": 14.0}] * 4 + [GOOD_DONOR]
    result = process_donor_cohort([make_cohort(donors)], 450)
    assert result == {"collected_ml": 450, "status": "ACCEPTED"}


# ---------- verify_storage_centrifuge (lines 46-58) ----------

@pytest.mark.parametrize("runs", [[], None])
def test_centrifuge_no_data(runs):
    assert verify_storage_centrifuge(runs) == "NO_DATA"


def test_centrifuge_abort_on_two_consecutive_drops():
    assert verify_storage_centrifuge([[3200, 2900, 2800, 3100]]) == "ABORT_SPIN"


def test_centrifuge_abort_in_later_run():
    assert verify_storage_centrifuge([[3500, 3400], [2900, 2500]]) == "ABORT_SPIN"


def test_centrifuge_stable_with_isolated_dip():
    assert verify_storage_centrifuge([[3200, 2900, 3100], [3000, 3500]]) == "STABLE"


def test_centrifuge_streak_resets_between_runs():
    # one low reading at the end of a run and one at the start of the next is not a streak
    assert verify_storage_centrifuge([[3200, 2900], [2900, 3200]]) == "STABLE"


def test_centrifuge_empty_run_is_stable():
    assert verify_storage_centrifuge([[]]) == "STABLE"


def test_centrifuge_3000_rpm_is_not_a_drop():
    assert verify_storage_centrifuge([[3000, 3000, 3000]]) == "STABLE"
