# Code Coverage Analysis Report

**Project:** L6_L7_05 Blood Donation Screening
**Lab:** Lab 6: Code and Branch Coverage Analysis
**Author:** Anishwar (PES2UG24CS068)
**Submitted To:** Prof. Asha K, Software Engineering

---

## 1. Introduction

This report presents the line (code) coverage analysis of the module `blood_donation_screening.py`. Line coverage measures the proportion of executable statements that run at least once during testing. The objective is to raise line coverage from the baseline set by the starter test to at least 90 percent.

## 2. Module Under Test

The module contains two functions.

| Function | Purpose |
|---|---|
| `process_donor_cohort(cohorts, standard_volume_ml)` | Screens donors in each registered cohort by age, weight and hemoglobin. It totals the collected blood volume and returns a status of `ACCEPTED`, `ZERO_YIELD` or `HIGH_DEFERRAL`. |
| `verify_storage_centrifuge(centrifuge_runs)` | Checks centrifuge runs for two consecutive readings below 3000 rpm. It returns `NO_DATA`, `ABORT_SPIN` or `STABLE`. |

## 3. Tools and Environment

| Item | Version |
|---|---|
| Python | 3.12.8 |
| pytest | 9.2.0 |
| coverage | coverage.py (installed via pip) |
| Platform | macOS (darwin) |

## 4. Methodology

The tests were executed under coverage with the following commands from the `Lab 6` directory.

```
python3 -m coverage run -m pytest CodeCoverageTest_blood_donation_screening.py
python3 -m coverage report -m
```

The `-m` flag lists the line numbers that were not executed. Each uncovered line in the baseline report was traced to the condition that guards it. A test case was then written to satisfy that condition.

## 5. Baseline Results

The starter file `test_blood_donation.py` contains one test. It submits a single eligible donor in a standard cohort.

| Name | Stmts | Miss | Cover | Missing |
|---|---|---|---|---|
| blood_donation_screening.py | 45 | 24 | 47% | 3, 10, 21-22, 25-28, 30-31, 36, 39, 41, 46-58 |

The baseline test never exercises invalid input, unregistered cohorts, donor deferrals, the fast-track bonus, the `HIGH_DEFERRAL` and `ZERO_YIELD` outcomes or the centrifuge function.

## 6. Test Cases Added

The file `CodeCoverageTest_blood_donation_screening.py` retains the original test and adds nine test cases.

| No. | Test Case | Input Summary | Expected Result | Lines Covered |
|---|---|---|---|---|
| 1 | `test_single_accepted_donor` | One eligible donor in a standard cohort | 450 ml, `ACCEPTED` | 2, 5-9, 12-20, 24, 29, 33, 35, 38, 40, 42 |
| 2 | `test_invalid_cohort_list_raises` | Cohorts passed as a string | `ValueError` | 3 |
| 3 | `test_unregistered_cohort_is_skipped` | Cohort with `clinic_registered` set to False | 0 ml, `ZERO_YIELD` | 10, 41 |
| 4 | `test_fast_track_adds_bonus` | Fast-track cohort with one eligible donor | 500 ml, `ACCEPTED` | 36 |
| 5 | `test_underage_underweight_and_high_hb_are_deferred` | Donors aged 16, weighing 45 kg and with hemoglobin 18.5 | 0 ml, `ZERO_YIELD` | 21-22, 30-31 |
| 6 | `test_high_altitude_low_hb_resets_collection` | High-altitude cohort with a donor of hemoglobin 11.0 | 0 ml, `ZERO_YIELD` | 25-28 |
| 7 | `test_high_deferral_status` | Five underage donors and one eligible donor | 450 ml, `HIGH_DEFERRAL` | 39 |
| 8 | `test_centrifuge_no_data` | Empty run list | `NO_DATA` | 46-47 |
| 9 | `test_centrifuge_abort_on_two_consecutive_drops` | Run of 3200, 2900, 2800, 3100 rpm | `ABORT_SPIN` | 49-55 |
| 10 | `test_centrifuge_stable_with_isolated_dip` | Runs with a single isolated reading below 3000 rpm | `STABLE` | 57-58 |

## 7. Results

All ten tests passed. Every statement in the module was executed.

| Name | Stmts | Miss | Cover | Missing |
|---|---|---|---|---|
| CodeCoverageTest_blood_donation_screening.py | 36 | 0 | 100% | |
| blood_donation_screening.py | 45 | 0 | 100% | |
| **TOTAL** | **81** | **0** | **100%** | |

![Code coverage terminal output](code_coverage.png)

*Figure 1. Terminal output of the code coverage run and report.*

## 8. Analysis

Line coverage rose from 47 percent to 100 percent. This exceeds the required threshold of 90 percent.

Full line coverage does not imply that every decision outcome was tested. When the same suite runs with the `--branch` flag, coverage.py reports one partial branch at `26->15`. Line 26 evaluated to True in the high-altitude test. It never evaluated to False because no test placed a low-hemoglobin donor in a standard cohort. The loop continuation path that follows a False result therefore remained untested. The Branch Coverage Analysis Report addresses this gap.

## 9. Conclusion

The code coverage test suite executes every statement of `blood_donation_screening.py` and achieves 100 percent line coverage. The remaining untested decision outcome confirms that line coverage alone overstates test completeness. Branch coverage is required to verify both outcomes of each decision.
