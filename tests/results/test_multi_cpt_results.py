import numpy as np
import pytest
from matplotlib import pyplot as plt
from matplotlib.axes import Axes
from matplotlib.figure import Figure
from pandas import DataFrame

from pypilecore.common.piles import PileProperties
from pypilecore.results import MultiCPTBearingResults, SingleCPTBearingResults
from pypilecore.results.multi_cpt_results import (
    CPTGroupResultsTable,
    SingleCPTBearingResultsContainer,
)
from pypilecore.results.single_cpt_results import CPTResultsTable
from pypilecore.results.soil_properties import SoilProperties

single_cpt_result_columns = [
    "F_nk_cal",
    "F_nk_k",
    "F_nk_d",
    "R_b_cal",
    "R_b_k",
    "R_b_d",
    "R_s_cal",
    "R_s_k",
    "R_s_d",
    "R_c_cal",
    "R_c_k",
    "R_c_d",
    "R_c_d_net",
    "F_c_k",
    "F_c_k_tot",
    "negative_friction_range_nap_top",
    "negative_friction_range_nap_btm",
    "positive_friction_range_nap_top",
    "positive_friction_range_nap_btm",
    "q_b_max",
    "q_s_max_mean",
    "qc1",
    "qc2",
    "qc3",
    "s_b",
    "s_el",
    "k_v_b",
    "k_v_1",
]


@pytest.mark.parametrize(
    "api_response_name,results_passover_name,n_cpts,ptl",
    [
        ("mock_multi_cpt_bearing_response", "mock_results_passover", 4, 0.0),
        ("mock_multi_cpt_bearing_response_2", "mock_results_passover_2", 21, 0.0),
    ],
)
def test_multi_cpt_bearing_results(
    api_response_name, results_passover_name, n_cpts, ptl, request
) -> None:
    api_response = request.getfixturevalue(api_response_name)
    results_passover = request.getfixturevalue(results_passover_name)
    cptgroupresults = MultiCPTBearingResults.from_api_response(
        api_response, results_passover
    )

    # Check result object attributes/properties
    assert isinstance(cptgroupresults.pile_properties, PileProperties)
    assert isinstance(cptgroupresults.cpt_names, list)
    assert len(cptgroupresults.cpt_names) == n_cpts

    # Check plotting method
    assert isinstance(
        cptgroupresults.plot_load_settlement(pile_tip_level_nap=ptl), Axes
    )
    plt.close("all")
    assert isinstance(cptgroupresults.boxplot(attribute="k_v_1"), Axes)
    plt.close("all")

    # Check CPTGroupResultsTable object
    group_table = cptgroupresults.group_results_table

    assert isinstance(group_table, CPTGroupResultsTable)
    assert isinstance(group_table.pile_tip_level_nap, np.ndarray)
    assert isinstance(group_table.R_s_k, np.ndarray)
    assert isinstance(group_table.R_b_k, np.ndarray)
    assert isinstance(group_table.R_c_k, np.ndarray)
    assert isinstance(group_table.R_c_d, np.ndarray)
    assert isinstance(group_table.F_nk_cal_mean, np.ndarray)
    assert isinstance(group_table.F_nk_k, np.ndarray)
    assert isinstance(group_table.F_nk_d, np.ndarray)
    assert isinstance(group_table.R_c_d_net, np.ndarray)
    assert isinstance(group_table.F_c_k, np.ndarray)
    assert isinstance(group_table.F_c_k_tot, np.ndarray)
    assert isinstance(group_table.s_b, np.ndarray)
    assert isinstance(group_table.s_e, np.ndarray)
    assert isinstance(group_table.s_e_mean, np.ndarray)
    assert isinstance(group_table.R_b_mob_ratio, np.ndarray)
    assert isinstance(group_table.R_s_mob_ratio, np.ndarray)
    assert isinstance(group_table.k_v_b, np.ndarray)
    assert isinstance(group_table.R_c_min, np.ndarray)
    assert isinstance(group_table.R_c_max, np.ndarray)
    assert isinstance(group_table.R_c_mean, np.ndarray)
    assert isinstance(group_table.R_c_std, np.ndarray)
    assert isinstance(group_table.R_s_mean, np.ndarray)
    assert isinstance(group_table.R_b_mean, np.ndarray)
    assert isinstance(group_table.var_coef, np.ndarray)
    assert isinstance(group_table.n_cpts, np.ndarray)
    assert isinstance(group_table.use_group_average, np.ndarray)
    assert isinstance(group_table.xi_normative, np.ndarray)
    assert isinstance(group_table.xi_value, np.ndarray)
    assert isinstance(group_table.cpt_Rc_min, np.ndarray)
    assert isinstance(group_table.cpt_Rc_max, np.ndarray)
    assert isinstance(group_table.cpt_normative, np.ndarray)

    assert isinstance(group_table.to_pandas(), DataFrame)

    assert isinstance(group_table.plot_bearing_capacities(), Axes)
    plt.close("all")

    # Check SingleCPTBearingResultsContainer object

    singlecptcontainer = cptgroupresults.cpt_results
    assert isinstance(singlecptcontainer, SingleCPTBearingResultsContainer)
    assert isinstance(singlecptcontainer.test_ids, list)
    assert isinstance(singlecptcontainer.results, list)
    assert isinstance(singlecptcontainer.to_pandas(), DataFrame)

    # Check SingleCPTBearingResults objects
    for test_id in singlecptcontainer.test_ids:
        assert isinstance(singlecptcontainer[test_id], SingleCPTBearingResults)
        assert isinstance(
            singlecptcontainer.get_cpt_results(test_id), SingleCPTBearingResults
        )
        assert singlecptcontainer[test_id] in singlecptcontainer.results

        single_cpt_results = singlecptcontainer[test_id]

        for column_name in single_cpt_result_columns:
            assert isinstance(
                singlecptcontainer.get_results_per_cpt(column_name), DataFrame
            )

            assert isinstance(single_cpt_results.soil_properties, SoilProperties)
            assert isinstance(single_cpt_results.pile_head_level_nap, float)
            assert isinstance(single_cpt_results.table, CPTResultsTable)
            assert isinstance(single_cpt_results.plot_bearing_capacities(), Axes)
            plt.close("all")
            assert isinstance(single_cpt_results.plot_bearing_overview(), Figure)
            plt.close("all")

            cpt_results_table = single_cpt_results.table

            assert isinstance(cpt_results_table.pile_tip_level_nap, np.ndarray)
            for column_name in single_cpt_result_columns:
                assert isinstance(getattr(cpt_results_table, column_name), np.ndarray)

            assert isinstance(cpt_results_table.to_pandas(), DataFrame)
