from __future__ import annotations

from typing import Tuple

import numpy as np
import pytest
from matplotlib import pyplot as plt
from matplotlib.axes import Axes
from numpy.typing import NDArray

from pypilecore.common.piles.geometry.components import PrimaryPileComponentDimension
from pypilecore.common.piles.geometry.components.common import (
    get_area_vs_depth,
    get_circum_vs_depth,
    get_component_bounds_nap,
    instantiate_axes,
)


def test_vanilla_primary_pile_dimension() -> None:
    # Test primary pile component dimension
    primary_pile_component_dimension = PrimaryPileComponentDimension()
    # Check properties
    assert primary_pile_component_dimension.length is None


def test_primary_pile_dimension_with_length() -> None:
    # Test primary pile component dimension
    primary_pile_component_dimension = PrimaryPileComponentDimension(
        length=1.0,
    )
    # Check properties
    assert primary_pile_component_dimension.length == 1.0


@pytest.mark.parametrize(
    "response, valid_payload",
    [
        (
            dict(
                length=1.0,
            ),
            dict(
                length=1.0,
            ),
        ),
        (
            dict(),
            None,
        ),
        (
            dict(
                length=None,
            ),
            None,
        ),
    ],
    ids=["length=1", "empty", "length=None"],
)
def test_init_primary_component_serialization(
    response: dict, valid_payload: dict | None
) -> None:
    length = response.get("length")
    ppcd = PrimaryPileComponentDimension.from_api_response(response)
    assert isinstance(ppcd, PrimaryPileComponentDimension)
    if length is not None:
        assert ppcd.length == length
    else:
        assert ppcd.length is None

    payload = ppcd.serialize_payload()

    assert payload == valid_payload


@pytest.mark.parametrize(
    "depth_nap, pile_tip_level_nap, pile_head_level_nap, length, circumference, valid_circums",
    [
        (
            np.array([-4, -3, -2, -1, 0]),
            -4,
            0,
            None,
            1.0,
            np.array([1, 1, 1, 1, 1]),
        ),
        (
            np.array([-5, -4, -3, -2, -1, 0, 1]),
            -4,
            0,
            None,
            1.0,
            np.array([0, 1, 1, 1, 1, 1, 0]),
        ),
        (
            np.array([-4, -3, -2, -1, 0]),
            -4,
            0,
            2.0,
            1.0,
            np.array([1, 1, 1, 0, 0]),
        ),
        (
            np.array([-5, -4, -3, -2, -1, 0, 1]),
            -4,
            0,
            2.0,
            1.0,
            np.array([0, 1, 1, 1, 0, 0, 0]),
        ),
        (
            np.array([-3, -2]),
            -4,
            0,
            2.0,
            1.0,
            np.array([1, 1]),
        ),
        (
            np.array([-3, -2, -1]),
            -4,
            0,
            1.0,
            1.0,
            np.array([1, 0, 0]),
        ),
        (
            np.array([-1, 0, 1]),
            -4,
            0,
            1.0,
            1.0,
            np.array([0, 0, 0]),
        ),
    ],
    ids=[
        "depths==component==pile",
        "depths>pile==component",
        "depths==pile>component",
        "depths>pile>component",
        "depths<component<pile",
        "pile<depths<component",
        "pile<depths!=component",
    ],
)
def test_get_circumference_vs_depth(
    depth_nap: NDArray[np.floating],
    pile_tip_level_nap: float | int,
    pile_head_level_nap: float | int,
    length: float | None,
    circumference: float,
    valid_circums: NDArray[np.floating],
) -> None:
    circums = get_circum_vs_depth(
        depth_nap=depth_nap,
        pile_tip_level_nap=pile_tip_level_nap,
        pile_head_level_nap=pile_head_level_nap,
        length=length,
        circumference=circumference,
    )
    assert isinstance(circums, np.ndarray)
    assert np.allclose(circums, valid_circums)


@pytest.mark.parametrize(
    "pile_tip_level_nap, pile_head_level_nap, length, valid_bounds",
    [
        (
            -4,
            0,
            None,
            (0, -4),
        ),
        (
            -4,
            0,
            2,
            (-2, -4),
        ),
        (
            -4,
            0,
            0,
            (-4, -4),
        ),
    ],
    ids=["component==pile", "component<pile", "component=0"],
)
def test_get_component_bounds_nap(
    pile_tip_level_nap: float | int,
    pile_head_level_nap: float | int,
    length: float | None,
    valid_bounds: Tuple[float, float],
) -> None:
    head, tip = get_component_bounds_nap(
        pile_tip_level_nap=pile_tip_level_nap,
        pile_head_level_nap=pile_head_level_nap,
        component_primary_length=length,
    )
    assert isinstance(head, float)
    assert isinstance(tip, float)
    assert np.allclose([head, tip], valid_bounds)


@pytest.mark.parametrize(
    "depth_nap, area_full, component_head_level_nap, component_tip_level_nap, inner_area, valid_areas",
    [
        (
            np.array([0, -1, -2, -3, -4]),
            1.0,
            0,
            -4,
            np.array([0, 0, 0, 0, 0]),
            np.array([1, 1, 1, 1, 1]),
        ),
        (
            np.array([2, 1, 0, -1, -2]),
            1.0,
            2,
            -2,
            np.array([0, 0, 0, 0, 0]),
            np.array([1, 1, 1, 1, 1]),
        ),
        (
            np.array([0, -1, -2, -3, -4]),
            1.0,
            -1,
            -3,
            np.array([0.1, 0.1, 0.1, 0.1, 0.1]),
            np.array([0, 0.9, 0.9, 0.9, 0]),
        ),
        (
            np.array([0, -1, -2, -3, -4]),
            2.0,
            0,
            -4,
            np.array(
                [
                    0.0,
                    0.25,
                    0.5,
                    1.0,
                    2.0,
                ]
            ),
            np.array([2.0, 1.75, 1.5, 1.0, 0.0]),
        ),
    ],
    ids=[
        "core,depths==component,v1",
        "core,depths==component,v2",
        "shell,depths>component",
        "shell,irregular-inner",
    ],
)
def test_get_area_vs_depth(
    depth_nap: NDArray[np.floating],
    area_full: float | int,
    component_head_level_nap: float | int,
    component_tip_level_nap: float | int,
    inner_area: NDArray[np.floating],
    valid_areas: NDArray[np.floating],
) -> None:
    areas = get_area_vs_depth(
        depth_nap=depth_nap,
        area_full=area_full,
        component_head_level_nap=component_head_level_nap,
        component_tip_level_nap=component_tip_level_nap,
        inner_area=inner_area,
    )

    assert isinstance(areas, np.ndarray)
    assert np.allclose(areas, valid_areas)


def test_instantiate_axes_with_valid_axes_object():
    # Create a valid axes object
    fig, ax = plt.subplots()

    # Call the instantiate_axes function with the valid axes object
    returned_axes = instantiate_axes(axes=ax)

    # Check if the returned object is the same as the input axes object
    assert returned_axes is ax


def test_instantiate_axes_with_invalid_axes_object():
    # Create an invalid axes object (not an instance of Axes)
    invalid_axes = "invalid_axes"

    # Call the instantiate_axes function with the invalid axes object
    with pytest.raises(ValueError):
        instantiate_axes(axes=invalid_axes)


def test_instantiate_axes_without_axes_object():
    # Call the instantiate_axes function without providing axes object
    returned_axes = instantiate_axes()

    # Check if the returned object is an instance of Axes
    assert isinstance(returned_axes, Axes)
