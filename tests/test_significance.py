import sys

import pytest
import pandas as pd

sys.path.insert(1, "/Users/gabrieltempass/Repositories/abtester/source")
from inputs import StatSignifInputs
from statistics import evaluate_signif


@pytest.fixture
def signif_inputs():
    i = StatSignifInputs()
    i.confidence = 0.95
    return i


@pytest.fixture
def signif_prop_inputs(signif_inputs):
    i = signif_inputs
    i.test = "Proportions"
    i.control_users = 30000
    i.treatment_users = 30000
    i.control_conversions = 1202
    i.treatment_conversions = 1298
    return i


@pytest.fixture
def signif_prop_ztest_inputs(signif_prop_inputs):
    i = signif_prop_inputs
    i.method = "Z-test"
    return i


def test_signif_prop_smaller_ztest(signif_prop_ztest_inputs):
    i = signif_prop_ztest_inputs
    i.alternative = "smaller"
    s = evaluate_signif(i)

    assert (
        s.alpha == 0.050000000000000044
        and s.control_prop == 0.04006666666666667
        and s.treatment_prop == 0.04326666666666667
        and s.observed_diff == 0.0032000000000000015
        and s.tstat == 1.9612950468681578
        and s.p_value == 0.9750776926200764
    )


def test_signif_prop_larger_ztest(signif_prop_ztest_inputs):
    i = signif_prop_ztest_inputs
    i.alternative = "larger"
    s = evaluate_signif(i)

    assert (
        s.alpha == 0.050000000000000044
        and s.control_prop == 0.04006666666666667
        and s.treatment_prop == 0.04326666666666667
        and s.observed_diff == 0.0032000000000000015
        and s.tstat == 1.9612950468681578
        and s.p_value == 0.024922307379923653
    )


def test_signif_prop_two_sided_ztest(signif_prop_ztest_inputs):
    i = signif_prop_ztest_inputs
    i.alternative = "two-sided"
    s = evaluate_signif(i)

    assert (
        s.alpha == 0.050000000000000044
        and s.control_prop == 0.04006666666666667
        and s.treatment_prop == 0.04326666666666667
        and s.observed_diff == 0.0032000000000000015
        and s.tstat == 1.9612950468681578
        and s.p_value == 0.049844614759847305
    )


@pytest.fixture
def signif_prop_perm_inputs(signif_prop_inputs):
    i = signif_prop_inputs
    i.method = "Permutation"
    i.iterations = 100
    return i


def test_signif_prop_smaller_perm(signif_prop_perm_inputs):
    i = signif_prop_perm_inputs
    i.alternative = "smaller"
    s = evaluate_signif(i)

    assert (
        s.alpha == 0.050000000000000044
        and s.control_prop == 0.04006666666666667
        and s.treatment_prop == 0.04326666666666667
        and s.control_no_conversions == 28798
        and s.treatment_no_conversions == 28702
        and s.observed_diff == 0.0032000000000000015
        and s.p_value == 0.98
    )


def test_signif_prop_larger_perm(signif_prop_perm_inputs):
    i = signif_prop_perm_inputs
    i.alternative = "larger"
    s = evaluate_signif(i)

    assert (
        s.alpha == 0.050000000000000044
        and s.control_prop == 0.04006666666666667
        and s.treatment_prop == 0.04326666666666667
        and s.control_no_conversions == 28798
        and s.treatment_no_conversions == 28702
        and s.observed_diff == 0.0032000000000000015
        and s.p_value == 0.02
    )


def test_signif_prop_two_sided_perm(signif_prop_perm_inputs):
    i = signif_prop_perm_inputs
    i.alternative = "two-sided"
    s = evaluate_signif(i)

    assert (
        s.alpha == 0.050000000000000044
        and s.control_prop == 0.04006666666666667
        and s.treatment_prop == 0.04326666666666667
        and s.control_no_conversions == 28798
        and s.treatment_no_conversions == 28702
        and s.observed_diff == 0.0032000000000000015
        and s.p_value == 0.03
    )


@pytest.fixture
def signif_mean_inputs(signif_inputs):
    i = signif_inputs
    i.test = "Means"
    i.df = pd.read_csv("/Users/gabrieltempass/Repositories/abtester/datasets/statistical_significance/dataset_1.csv")
    i.alias = {
        "Measurement": "Measurement",
        "Group": "Group",
        "Control": "Control",
        "Treatment": "Treatment",
    }
    return i


@pytest.fixture
def signif_mean_ttest_inputs(signif_mean_inputs):
    i = signif_mean_inputs
    i.method = "t-test"
    return i


def test_signif_mean_smaller_ttest(signif_mean_ttest_inputs):
    i = signif_mean_ttest_inputs
    i.alternative = "smaller"
    s = evaluate_signif(i)

    assert (
        s.alpha == 0.050000000000000044
        and s.control_n == 100
        and s.treatment_n == 100
        and s.control_mean == 170.57
        and s.treatment_mean == 160.44
        and s.control_std == 33.26576636906494
        and s.treatment_std == 31.047802830571772
        and s.dof == 198.0
        and s.observed_diff == -10.129999999999995
        and s.tstat == -2.226197670573247
        and s.p_value == 0.013564141699454522
    )


def test_signif_mean_larger_ttest(signif_mean_ttest_inputs):
    i = signif_mean_ttest_inputs
    i.alternative = "larger"
    s = evaluate_signif(i)

    assert (
        s.alpha == 0.050000000000000044
        and s.control_n == 100
        and s.treatment_n == 100
        and s.control_mean == 170.57
        and s.treatment_mean == 160.44
        and s.control_std == 33.26576636906494
        and s.treatment_std == 31.047802830571772
        and s.dof == 198.0
        and s.observed_diff == -10.129999999999995
        and s.tstat == -2.226197670573247
        and s.p_value == 0.9864358583005455
    )


def test_signif_mean_two_sided_ttest(signif_mean_ttest_inputs):
    i = signif_mean_ttest_inputs
    i.alternative = "two-sided"
    s = evaluate_signif(i)

    assert (
        s.alpha == 0.050000000000000044
        and s.control_n == 100
        and s.treatment_n == 100
        and s.control_mean == 170.57
        and s.treatment_mean == 160.44
        and s.control_std == 33.26576636906494
        and s.treatment_std == 31.047802830571772
        and s.dof == 198.0
        and s.observed_diff == -10.129999999999995
        and s.tstat == -2.226197670573247
        and s.p_value == 0.027128283398909044
    )


@pytest.fixture
def signif_mean_ztest_inputs(signif_mean_inputs):
    i = signif_mean_inputs
    i.method = "Z-test"
    return i


def test_signif_mean_smaller_ztest(signif_mean_ztest_inputs):
    i = signif_mean_ztest_inputs
    i.alternative = "smaller"
    s = evaluate_signif(i)

    assert (
        s.alpha == 0.050000000000000044
        and s.control_n == 100
        and s.treatment_n == 100
        and s.control_mean == 170.57
        and s.treatment_mean == 160.44
        and s.control_std == 33.26576636906494
        and s.treatment_std == 31.047802830571772
        and s.observed_diff == -10.129999999999995
        and s.tstat == -2.2261976705732467
        and s.p_value == 0.013000471966839849
    )


def test_signif_mean_larger_ztest(signif_mean_ztest_inputs):
    i = signif_mean_ztest_inputs
    i.alternative = "larger"
    s = evaluate_signif(i)

    assert (
        s.alpha == 0.050000000000000044
        and s.control_n == 100
        and s.treatment_n == 100
        and s.control_mean == 170.57
        and s.treatment_mean == 160.44
        and s.control_std == 33.26576636906494
        and s.treatment_std == 31.047802830571772
        and s.observed_diff == -10.129999999999995
        and s.tstat == -2.2261976705732467
        and s.p_value == 0.9869995280331602
    )


def test_signif_mean_two_sided_ztest(signif_mean_ztest_inputs):
    i = signif_mean_ztest_inputs
    i.alternative = "two-sided"
    s = evaluate_signif(i)

    assert (
        s.alpha == 0.050000000000000044
        and s.control_n == 100
        and s.treatment_n == 100
        and s.control_mean == 170.57
        and s.treatment_mean == 160.44
        and s.control_std == 33.26576636906494
        and s.treatment_std == 31.047802830571772
        and s.observed_diff == -10.129999999999995
        and s.tstat == -2.2261976705732467
        and s.p_value == 0.026000943933679698
    )


@pytest.fixture
def signif_mean_perm_inputs(signif_mean_inputs):
    i = signif_mean_inputs
    i.method = "Permutation"
    i.iterations = 100
    return i


def test_signif_mean_smaller_perm(signif_mean_perm_inputs):
    i = signif_mean_perm_inputs
    i.alternative = "smaller"
    s = evaluate_signif(i)

    assert (
        s.alpha == 0.050000000000000044
        and s.control_n == 100
        and s.treatment_n == 100
        and s.control_mean == 170.57
        and s.treatment_mean == 160.44
        and s.control_std == 33.26576636906494
        and s.treatment_std == 31.047802830571772
        and s.observed_diff == -10.129999999999995
        and s.p_value == 0.01
    )


def test_signif_mean_larger_perm(signif_mean_perm_inputs):
    i = signif_mean_perm_inputs
    i.alternative = "larger"
    s = evaluate_signif(i)

    assert (
        s.alpha == 0.050000000000000044
        and s.control_n == 100
        and s.treatment_n == 100
        and s.control_mean == 170.57
        and s.treatment_mean == 160.44
        and s.control_std == 33.26576636906494
        and s.treatment_std == 31.047802830571772
        and s.observed_diff == -10.129999999999995
        and s.p_value == 0.99
    )


def test_signif_mean_two_sided_perm(signif_mean_perm_inputs):
    i = signif_mean_perm_inputs
    i.alternative = "two-sided"
    s = evaluate_signif(i)

    assert (
        s.alpha == 0.050000000000000044
        and s.treatment_n == 100
        and s.control_n == 100
        and s.control_mean == 170.57
        and s.treatment_mean == 160.44
        and s.control_std == 33.26576636906494
        and s.treatment_std == 31.047802830571772
        and s.observed_diff == -10.129999999999995
        and s.p_value == 0.03
    )
