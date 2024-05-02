import sys

import pytest
import pandas as pd

from ..source.inputs import SampleSizeInputs
from ..source.statistics import calculate_size


@pytest.fixture
def size_inputs():
    i = SampleSizeInputs()
    i.sensitivity = 0.1
    i.confidence = 0.95
    i.power = 0.8
    i.control_ratio = 0.4
    i.treatment_ratio = 0.6
    return i


@pytest.fixture
def size_prop_inputs(size_inputs):
    i = size_inputs
    i.test = "Proportions"
    i.control_proportion = 0.15
    return i


@pytest.fixture
def size_prop_ttest_inputs(size_prop_inputs):
    i = size_prop_inputs
    i.method = "t-test"
    return i


def test_size_prop_smaller_ttest(size_prop_ttest_inputs):
    i = size_prop_ttest_inputs
    i.alternative = "smaller"
    s = calculate_size(i)

    assert (
        s.alpha == 0.050000000000000044
        and s.ratio == 1.4999999999999998
        and s.treatment_proportion == 0.135
        and s.effect_size == -0.0429244540208068
        and s.control_conversions == 839
        and s.treatment_conversions == 1132
        and s.control_sample == 5594
        and s.treatment_sample == 8391
    )


def test_size_prop_larger_ttest(size_prop_ttest_inputs):
    i = size_prop_ttest_inputs
    i.alternative = "larger"
    s = calculate_size(i)

    assert (
        s.alpha == 0.050000000000000044
        and s.ratio == 1.4999999999999998
        and s.treatment_proportion == 0.165
        and s.effect_size == 0.04118870915739414
        and s.control_conversions == 911
        and s.treatment_conversions == 1503
        and s.control_sample == 6075
        and s.treatment_sample == 9113
    )


def test_size_prop_two_sided_ttest(size_prop_ttest_inputs):
    i = size_prop_ttest_inputs
    i.alternative = "two-sided"
    s = calculate_size(i)

    assert (
        s.alpha == 0.050000000000000044
        and s.ratio == 1.4999999999999998
        and s.treatment_proportion == 0.165
        and s.effect_size == 0.04118870915739414
        and s.control_conversions == 1156
        and s.treatment_conversions == 1908
        and s.control_sample == 7712
        and s.treatment_sample == 11568
    )


@pytest.fixture
def size_prop_ztest_inputs(size_prop_inputs):
    i = size_prop_inputs
    i.method = "Z-test"
    return i


def test_size_prop_smaller_ztest(size_prop_ztest_inputs):
    i = size_prop_ztest_inputs
    i.alternative = "smaller"
    s = calculate_size(i)

    assert (
        s.alpha == 0.050000000000000044
        and s.ratio == 1.4999999999999998
        and s.treatment_proportion == 0.135
        and s.effect_size == -0.0429244540208068
        and s.control_conversions == 838
        and s.treatment_conversions == 1132
        and s.control_sample == 5593
        and s.treatment_sample == 8390
    )


def test_size_prop_larger_ztest(size_prop_ztest_inputs):
    i = size_prop_ztest_inputs
    i.alternative = "larger"
    s = calculate_size(i)

    assert (
        s.alpha == 0.050000000000000044
        and s.ratio == 1.4999999999999998
        and s.treatment_proportion == 0.165
        and s.effect_size == 0.04118870915739414
        and s.control_conversions == 911
        and s.treatment_conversions == 1503
        and s.control_sample == 6074
        and s.treatment_sample == 9111
    )


def test_size_prop_two_sided_ztest(size_prop_ztest_inputs):
    i = size_prop_ztest_inputs
    i.alternative = "two-sided"
    s = calculate_size(i)

    assert (
        s.alpha == 0.050000000000000044
        and s.ratio == 1.4999999999999998
        and s.treatment_proportion == 0.165
        and s.effect_size == 0.04118870915739414
        and s.control_conversions == 1156
        and s.treatment_conversions == 1908
        and s.control_sample == 7711
        and s.treatment_sample == 11567
    )


@pytest.fixture
def size_mean_inputs(size_inputs):
    i = size_inputs
    i.test = "Means"
    i.df = pd.read_csv("/Users/gabrieltempass/Repositories/abtester/datasets/sample_size/dataset_a.csv")
    i.alias = {
        "Measurement": "Measurement",
        "Group": "Group",
        "Control": "Control",
        "Treatment": "Treatment",
    }
    i.control_proportion = None
    return i


@pytest.fixture
def size_mean_ttest_inputs(size_mean_inputs):
    i = size_mean_inputs
    i.method = "t-test"
    return i


def test_size_mean_smaller_ttest(size_mean_ttest_inputs):
    i = size_mean_ttest_inputs
    i.alternative = "smaller"
    s = calculate_size(i)

    assert (
        s.alpha == 0.050000000000000044
        and s.ratio == 1.4999999999999998
        and s.difference == -38.364782608695634
        and s.effect_size == -0.24480319125235722
        and s.standard_deviation == 156.71684021940305
        and s.control_mean == 383.6478260869565
        and s.treatment_mean == 345.2830434782609
        and s.control_sample == 173
        and s.treatment_sample == 260
    )


def test_size_mean_larger_ttest(size_mean_ttest_inputs):
    i = size_mean_ttest_inputs
    i.alternative = "larger"
    s = calculate_size(i)

    assert (
        s.alpha == 0.050000000000000044
        and s.ratio == 1.4999999999999998
        and s.difference == 38.36478260869569
        and s.effect_size == 0.24480319125235758
        and s.standard_deviation == 156.71684021940305
        and s.control_mean == 383.6478260869565
        and s.treatment_mean == 422.0126086956522
        and s.control_sample == 173
        and s.treatment_sample == 260
    )


def test_size_mean_two_sided_ttest(size_mean_ttest_inputs):
    i = size_mean_ttest_inputs
    i.alternative = "two-sided"
    s = calculate_size(i)

    assert (
        s.alpha == 0.050000000000000044
        and s.ratio == 1.4999999999999998
        and s.difference == 38.36478260869569
        and s.effect_size == 0.24480319125235758
        and s.standard_deviation == 156.71684021940305
        and s.control_mean == 383.6478260869565
        and s.treatment_mean == 422.0126086956522
        and s.control_sample == 220
        and s.treatment_sample == 330
    )


@pytest.fixture
def size_mean_ztest_inputs(size_mean_inputs):
    i = size_mean_inputs
    i.method = "Z-test"
    return i


def test_size_mean_smaller_ztest(size_mean_ztest_inputs):
    i = size_mean_ztest_inputs
    i.alternative = "smaller"
    s = calculate_size(i)

    assert (
        s.alpha == 0.050000000000000044
        and s.ratio == 1.4999999999999998
        and s.difference == -38.364782608695634
        and s.effect_size == -0.24480319125235722
        and s.standard_deviation == 156.71684021940305
        and s.control_mean == 383.6478260869565
        and s.treatment_mean == 345.2830434782609
        and s.control_sample == 172
        and s.treatment_sample == 258
    )


def test_size_mean_larger_ztest(size_mean_ztest_inputs):
    i = size_mean_ztest_inputs
    i.alternative = "larger"
    s = calculate_size(i)

    assert (
        s.alpha == 0.050000000000000044
        and s.ratio == 1.4999999999999998
        and s.difference == 38.36478260869569
        and s.effect_size == 0.24480319125235758
        and s.standard_deviation == 156.71684021940305
        and s.control_mean == 383.6478260869565
        and s.treatment_mean == 422.0126086956522
        and s.control_sample == 172
        and s.treatment_sample == 258
    )


def test_size_mean_two_sided_ztest(size_mean_ztest_inputs):
    i = size_mean_ztest_inputs
    i.alternative = "two-sided"
    s = calculate_size(i)

    assert (
        s.alpha == 0.050000000000000044
        and s.ratio == 1.4999999999999998
        and s.difference == 38.36478260869569
        and s.effect_size == 0.24480319125235758
        and s.standard_deviation == 156.71684021940305
        and s.control_mean == 383.6478260869565
        and s.treatment_mean == 422.0126086956522
        and s.control_sample == 219
        and s.treatment_sample == 329
    )
