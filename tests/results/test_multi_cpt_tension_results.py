import numpy as np
import pytest
from matplotlib import pyplot as plt
from matplotlib.axes import Axes
from matplotlib.figure import Figure
from pandas import DataFrame

from pypilecore.common.piles import PileProperties
from pypilecore.results.soil_properties import SoilProperties
from pypilecore.results.tension.multi_cpt_results import (
    CPTTensionGroupResultsTable,
    MultiCPTTensionBearingResults,
    SingleCPTTensionBearingResults,
    SingleCPTTensionBearingResultsContainer,
)
from pypilecore.results.tension.single_cpt_results import CPTTensionResultsTable

single_cpt_result_columns = [
    "A",
    "R_t_d_plug",
    "R_t_d",
    "R_t_k",
    "R_t_mob_ratio",
    "R_t_mob",
    "q_s_max_mean",
    "k_v_b",
    "k_v_1",
    "s_e",
    "s_b",
]


@pytest.mark.parametrize(
    "api_response_name,results_passover_name,n_cpts,ptl",
    [
        ("mock_multi_cpt_tension_response", "mock_results_passover", 1, 0.0),
    ],
)
def test_multi_cpt_bearing_results(
    api_response_name, results_passover_name, n_cpts, ptl, request
) -> None:
    api_response = request.getfixturevalue(api_response_name)
    results_passover = request.getfixturevalue(results_passover_name)
    cptgroupresults = MultiCPTTensionBearingResults.from_api_response(
        api_response, results_passover
    )

    # Check result object attributes/properties
    assert isinstance(cptgroupresults.pile_properties, PileProperties)
    assert isinstance(cptgroupresults.cpt_names, list)
    assert len(cptgroupresults.cpt_names) == n_cpts

    # Check CPTGroupResultsTable object
    group_table = cptgroupresults.group_results_table

    assert isinstance(group_table, CPTTensionGroupResultsTable)
    assert isinstance(group_table.pile_tip_level_nap, np.ndarray)
    assert isinstance(group_table.R_t_d, np.ndarray)
    assert isinstance(group_table.var_coef, np.ndarray)
    assert isinstance(group_table.n_cpts, np.ndarray)
    assert isinstance(group_table.xi_normative, np.ndarray)
    assert isinstance(group_table.xi_value, np.ndarray)
    assert isinstance(group_table.cpt_normative, np.ndarray)

    assert isinstance(group_table.to_pandas(), DataFrame)

    assert isinstance(group_table.plot_bearing_capacities(), Axes)
    plt.close("all")

    # Check SingleCPTBearingResultsContainer object

    singlecptcontainer = cptgroupresults.cpt_results
    assert isinstance(singlecptcontainer, SingleCPTTensionBearingResultsContainer)
    assert isinstance(singlecptcontainer.test_ids, list)
    assert isinstance(singlecptcontainer.results, list)
    assert isinstance(singlecptcontainer.to_pandas(), DataFrame)

    # Check SingleCPTBearingResults objects
    for test_id in singlecptcontainer.test_ids:
        assert isinstance(singlecptcontainer[test_id], SingleCPTTensionBearingResults)
        assert isinstance(
            singlecptcontainer.get_cpt_results(test_id), SingleCPTTensionBearingResults
        )
        assert singlecptcontainer[test_id] in singlecptcontainer.results

        single_cpt_results = singlecptcontainer[test_id]

        for column_name in single_cpt_result_columns:
            assert isinstance(
                singlecptcontainer.get_results_per_cpt(column_name), DataFrame
            )

            assert isinstance(single_cpt_results.soil_properties, SoilProperties)
            assert isinstance(single_cpt_results.pile_head_level_nap, float)
            assert isinstance(single_cpt_results.table, CPTTensionResultsTable)
            assert isinstance(single_cpt_results.plot_bearing_capacities(), Axes)
            plt.close("all")
            assert isinstance(single_cpt_results.plot_bearing_overview(), Figure)
            plt.close("all")

            cpt_results_table = single_cpt_results.table

            assert isinstance(cpt_results_table.pile_tip_level_nap, np.ndarray)
            for column_name in single_cpt_result_columns:
                assert isinstance(getattr(cpt_results_table, column_name), np.ndarray)

            assert isinstance(cpt_results_table.to_pandas(), DataFrame)
