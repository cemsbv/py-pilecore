from typing import Optional, Union, overload

import numpy as np
from numpy.typing import NDArray

Number = Union[int, float]


@overload
def nap_to_depth(nap: float, zid: float) -> float:
    ...


@overload
def nap_to_depth(nap: None, zid: float) -> None:
    ...


@overload
def nap_to_depth(
    nap: NDArray[Union[np.floating, np.integer]], zid: float
) -> NDArray[Union[np.floating, np.integer]]:
    ...


def nap_to_depth(
    nap: Optional[Union[Number, NDArray[Union[np.floating, np.integer]]]], zid: float
) -> Optional[Union[float, NDArray[Union[np.floating, np.integer]]]]:
    if nap is None:
        return None
    return -(nap - zid)


@overload
def depth_to_nap(depth: float, zid: float) -> float:
    ...


@overload
def depth_to_nap(depth: None, zid: float) -> None:
    ...


@overload
def depth_to_nap(
    depth: NDArray[Union[np.floating, np.integer]], zid: float
) -> NDArray[Union[np.floating, np.integer]]:
    ...


def depth_to_nap(
    depth: Optional[Union[Number, NDArray[Union[np.floating, np.integer]]]], zid: float
) -> Optional[Union[Number, NDArray[Union[np.floating, np.integer]]]]:
    if depth is None:
        return None
    return zid - depth
