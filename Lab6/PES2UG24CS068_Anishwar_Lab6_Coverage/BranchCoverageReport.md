# Branch Coverage Analysis Report

**Project:** L6_L7_05 Blood Donation Screening
**Lab:** Lab 6: Code and Branch Coverage Analysis
**Author:** Anishwar (PES2UG24CS068)
**Submitted To:** Prof. Asha K, Software Engineering

---

## 1. Introduction

This report presents the branch coverage analysis of the module `blood_donation_screening.py`. Branch coverage measures whether each control structure has been evaluated to both True and False. Loop statements count as branches because a loop may either enter its body or exit. The objective is to achieve at least 90 percent branch coverage.

## 2. Tools and Environment

| Item | Version |
|---|---|
| Python | 3.12.8 |
| pytest | 9.2.0 |
| coverage | coverage.py (installed via pip) |
| Platform | macOS (darwin) |

## 3. Methodology

The tests were executed under coverage with branch measurement enabled. The commands were run from the `Lab 6` directory.

```
python3 -m coverage run --branch -m pytest BranchCoverageTest_blood_donation_screening.py
python3 -m coverage report -m
```

Each decision point in the module was listed with its two possible outcomes. Test cases were then written so that every outcome executes at least once. Boundary values and missing dictionary keys were also tested because they decide which outcome a condition takes.

## 4. Decision Points

The module contains 16 decision points. Each has two outcomes for a total of 32 branches.

| Line | Decision | True Outcome | False Outcome |
|---|---|---|---|
| 2 | Invalid cohort list or non-positive volume | Raise `ValueError` | Continue processing |
| 8 | Cohort loop | Process next cohort | Compute final status |
| 9 | Cohort not registered | Skip cohort | Read cohort type and donors |
| 15 | Donor loop | Screen next donor | Check fast-track flag |
| 20 | Age below 17 or weight below 50 | Defer donor | Check hemoglobin |
| 24 | Hemoglobin below 12.5 | Defer donor | Check upper hemoglobin limit |
| 26 | Cohort type is high altitude | Reset total and exit loop | Continue to next donor |
| 29 | Hemoglobin above 18.0 | Defer donor | Collect standard volume |
| 35 | Cohort is fast-track | Add 50 ml | Move to next cohort |
| 38 | More than four deferrals | Return `HIGH_DEFERRAL` | Check total volume |
| 40 | Total volume is zero | Return `ZERO_YIELD` | Return `ACCEPTED` |
| 46 | No centrifuge data | Return `NO_DATA` | Inspect runs |
| 49 | Run loop | Inspect next run | Return `STABLE` |
| 51 | RPM reading loop | Inspect next reading | Move to next run |
| 52 | Reading below 3000 rpm | Increase drop streak | Reset drop streak |
| 54 | Drop streak of two or more | Return `ABORT_SPIN` | Read next value |

## 5. Baseline Results

The starter file `test_blood_donation.py` produced the following branch coverage report.

| Name | Stmts | Miss | Branch | BrPart | Cover | Missing |
|---|---|---|---|---|---|---|
| blood_donation_screening.py | 45 | 24 | 32 | 8 | 43% | 3, 10, 21-22, 25-28, 30-31, 36, 39, 41, 46-58 |

The code coverage suite raised line coverage to 100 percent and branch coverage to 99 percent. One partial branch remained at `26->15`. A low-hemoglobin donor in a standard cohort had not been tested.

## 6. Test Cases Added

The file `BranchCoverageTest_blood_donation_screening.py` contains 30 test executions. The table below groups them by the decision they target.

| Decision (Line) | Test Case | Input Summary | Expected Result |
|---|---|---|---|
| 2 | `test_single_accepted_donor` | One eligible donor | 450 ml, `ACCEPTED` |
| 2 | `test_invalid_cohort_list_raises` | Cohorts passed as a string | `ValueError` |
| 2 | `test_non_positive_volume_raises` | Volume of 0 and of -100 | `ValueError` |
| 8 | `test_empty_cohort_list_is_zero_yield` | Empty cohort list | 0 ml, `ZERO_YIELD` |
| 9 | `test_unregistered_cohort_is_skipped` | `clinic_registered` set to False | 0 ml, `ZERO_YIELD` |
| 9 | `test_missing_clinic_registered_defaults_to_skipped` | Cohort without the `clinic_registered` key | 0 ml, `ZERO_YIELD` |
| 15 | `test_registered_cohort_without_donors` | Registered cohort without a donor list | 0 ml, `ZERO_YIELD` |
| 35 | `test_fast_track_adds_bonus` | Fast-track cohort with one eligible donor | 500 ml, `ACCEPTED` |
| 35 | `test_fast_track_bonus_alone_is_accepted` | Fast-track cohort with no donors | 50 ml, `ACCEPTED` |
| 8, 9, 35 | `test_mixed_cohorts_are_summed` | Fast-track, unregistered and standard cohorts | 1400 ml, `ACCEPTED` |
| 20 | `test_ineligible_donor_is_deferred` | Age 16, weight 49 kg and an empty donor record | 0 ml, `ZERO_YIELD` |
| 20 | `test_age_and_weight_boundaries_are_eligible` | Age 17 and weight 50 kg | 450 ml, `ACCEPTED` |
| 24, 26 | `test_low_hb_in_standard_cohort_only_defers_that_donor` | Standard cohort with a donor of hemoglobin 12.0 | 900 ml, `ACCEPTED` |
| 24, 26 | `test_high_altitude_low_hb_resets_collection` | High-altitude cohort with a donor of hemoglobin 11.0 | 0 ml, `ZERO_YIELD` |
| 26, 35 | `test_high_altitude_reset_still_gets_fast_track_bonus` | High-altitude fast-track cohort with a low-hemoglobin donor | 50 ml, `ACCEPTED` |
| 29 | `test_high_hb_is_deferred` | Hemoglobin 18.5 | 0 ml, `ZERO_YIELD` |
| 24, 29 | `test_hb_boundaries_are_accepted` | Hemoglobin 12.5 and 18.0 | 900 ml, `ACCEPTED` |
| 38 | `test_high_deferral_status` | Five deferrals | 450 ml, `HIGH_DEFERRAL` |
| 38, 40 | `test_exactly_four_deferrals_is_not_high_deferral` | Four deferrals | 450 ml, `ACCEPTED` |
| 46 | `test_centrifuge_no_data` | Empty list and `None` | `NO_DATA` |
| 52, 54 | `test_centrifuge_abort_on_two_consecutive_drops` | 3200, 2900, 2800, 3100 rpm | `ABORT_SPIN` |
| 49, 54 | `test_centrifuge_abort_in_later_run` | Stable first run and failing second run | `ABORT_SPIN` |
| 49, 52 | `test_centrifuge_stable_with_isolated_dip` | Single readings below 3000 rpm | `STABLE` |
| 49, 52 | `test_centrifuge_streak_resets_between_runs` | Low reading at the end of one run and the start of the next | `STABLE` |
| 51 | `test_centrifuge_empty_run_is_stable` | One run with no readings | `STABLE` |
| 52 | `test_centrifuge_3000_rpm_is_not_a_drop` | Readings of exactly 3000 rpm | `STABLE` |

## 7. Results

All 30 tests passed. All 32 branches were taken.

| Name | Stmts | Miss | Branch | BrPart | Cover |
|---|---|---|---|---|---|
| BranchCoverageTest_blood_donation_screening.py | 86 | 0 | 0 | 0 | 100% |
| blood_donation_screening.py | 45 | 0 | 32 | 0 | 100% |
| **TOTAL** | **131** | **0** | **32** | **0** | **100%** |

![Branch coverage terminal output](branch_coverage.png)

*Figure 1. Terminal output of the branch coverage run and report.*

## 8. Analysis

Branch coverage rose from 43 percent at baseline to 100 percent. This exceeds the required threshold of 90 percent.

The test `test_low_hb_in_standard_cohort_only_defers_that_donor` closed the gap at `26->15` that the code coverage suite left open. It confirms that a low-hemoglobin donor in a standard cohort is deferred without discarding volume already collected from earlier donors.

The suite also verifies behaviour that line coverage cannot detect.

* **Zero-iteration loops.** An empty cohort list, a cohort without donors and a centrifuge run without readings each skip a loop body entirely.
* **Default values.** Missing `clinic_registered`, `type`, `donors`, `age`, `weight_kg` and `hb` keys fall back to their defaults.
* **Boundary values.** Age 17, weight 50 kg, hemoglobin 12.5 and 18.0, exactly four deferrals and exactly 3000 rpm all fall on the accepting side of their conditions.
* **State reset.** The drop streak resets at the start of each centrifuge run. Low readings split across two runs do not trigger an abort.
* **Interaction effects.** A high-altitude reset is followed by the fast-track bonus. The cohort therefore returns 50 ml with status `ACCEPTED` instead of `ZERO_YIELD`.

coverage.py measures branches at the level of control flow arcs. It does not measure each operand of a compound condition such as the `or` on line 2 and line 20. Separate tests were written for each operand to provide condition-level assurance beyond the reported metric.

## 9. Conclusion

The branch coverage test suite evaluates every decision in `blood_donation_screening.py` to both outcomes and achieves 100 percent branch coverage. The added boundary, default value and empty loop tests give stronger evidence of correctness than full line coverage alone.
