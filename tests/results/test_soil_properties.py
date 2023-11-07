import numpy as np
import pytest
from matplotlib import pyplot as plt
from matplotlib.axes import Axes
from matplotlib.figure import Figure
from pandas import DataFrame

from pypilecore.results.soil_properties import CPTTable, LayerTable, SoilProperties


def test_layer_table():
    with pytest.raises(ValueError):
        LayerTable(
            index=[0, 1],
            thickness=[0.0],
            depth_btm=[0.0],
            C_s=None,
            C_p=None,
            gamma=[0.016],
            gamma_sat=[0.018],
            phi=[0.001],
            soil_code=["Z"],
        )

    layer_table = LayerTable(
        index=[0, 1],
        thickness=[1.0, 1.0],
        depth_btm=[1.0, 2.0],
        C_s=None,
        C_p=None,
        gamma=[0.016, 0.016],
        gamma_sat=[0.018, 0.018],
        phi=[0.001, 0.001],
        soil_code=["Z", "Z"],
    )

    assert isinstance(layer_table.to_pandas(), DataFrame)


def test_cpt_table():
    with pytest.raises(ValueError):
        CPTTable(
            depth_nap=[0.0, 0.01],
            qc=[15],
            qc_original=[15],
            qc_chamfered=None,
            qc1=None,
            qc2=None,
            fs=None,
        )

    cpt_table = CPTTable(
        depth_nap=[0.0, 0.01],
        qc=[15, 15],
        qc_original=[15, 15],
        qc_chamfered=[15, 15],
        qc1=[15, 15],
        qc2=[15, 15],
        fs=[0.15, 0.15],
    )

    assert isinstance(cpt_table.depth_nap, np.ndarray)
    assert isinstance(cpt_table.qc, np.ndarray)
    assert isinstance(cpt_table.qc_original, np.ndarray)
    assert isinstance(cpt_table.qc_chamfered, np.ndarray)
    assert isinstance(cpt_table.qc1, np.ndarray)
    assert isinstance(cpt_table.qc2, np.ndarray)
    assert isinstance(cpt_table.fs, np.ndarray)
    assert isinstance(cpt_table.friction_ratio, np.ndarray)
    assert isinstance(cpt_table.qc_has_been_chamfered, bool)
    assert isinstance(cpt_table.qc_has_been_reduced, bool)

    assert isinstance(cpt_table.to_pandas(), DataFrame)

    assert isinstance(cpt_table.plot_qc(), Axes)
    plt.close("all")
    assert isinstance(cpt_table.plot_friction_ratio(), Axes)
    plt.close("all")

    with pytest.raises(TypeError):
        cpt_table.plot_qc(axes=1)
    with pytest.raises(TypeError):
        cpt_table.plot_friction_ratio(axes=1)

    # Test empty CPTTable object
    cpt_table = CPTTable.from_api_response({})

    assert isinstance(cpt_table.depth_nap, np.ndarray)
    assert isinstance(cpt_table.qc, np.ndarray)
    assert isinstance(cpt_table.qc_original, np.ndarray)
    assert isinstance(cpt_table.qc_chamfered, np.ndarray)
    assert isinstance(cpt_table.qc1, np.ndarray)
    assert isinstance(cpt_table.qc2, np.ndarray)
    assert isinstance(cpt_table.fs, np.ndarray)
    assert isinstance(cpt_table.friction_ratio, np.ndarray)
    assert isinstance(cpt_table.qc_has_been_chamfered, bool)
    assert isinstance(cpt_table.qc_has_been_reduced, bool)

    assert isinstance(cpt_table.to_pandas(), DataFrame)

    assert isinstance(cpt_table.plot_qc(), Axes)
    plt.close("all")
    assert isinstance(cpt_table.plot_friction_ratio(), Axes)
    plt.close("all")


def test_soil_properties():
    layer_table = LayerTable(
        index=[0, 1],
        thickness=[1.0, 1.0],
        depth_btm=[1.0, 2.0],
        C_s=None,
        C_p=None,
        gamma=[0.016, 0.016],
        gamma_sat=[0.018, 0.018],
        phi=[0.001, 0.001],
        soil_code=["Z", "Z"],
    )

    cpt_table = CPTTable(
        depth_nap=[0.0, 0.01],
        qc=[15, 15],
        qc_original=[15, 15],
        qc_chamfered=[15, 15],
        qc1=[15, 15],
        qc2=[15, 15],
        fs=[0.15, 0.15],
    )

    soil_properties = SoilProperties(
        cpt_table=cpt_table,
        layer_table=layer_table,
        ref_height=0.0,
        surface_level_ref=0.0,
        groundwater_level_ref=-1.0,
        test_id="test",
    )

    assert isinstance(soil_properties.cpt_table, CPTTable)
    assert isinstance(soil_properties.layer_table, LayerTable)
    assert soil_properties.x is None
    assert soil_properties.y is None
    assert isinstance(soil_properties.test_id, str)
    assert isinstance(soil_properties.ref_height, float)
    assert isinstance(soil_properties.groundwater_level_ref, float)
    assert isinstance(soil_properties.surface_level_ref, float)

    assert isinstance(soil_properties.plot_layers(), Axes)
    plt.close("all")
    assert isinstance(soil_properties.plot(), Figure)
    plt.close("all")
