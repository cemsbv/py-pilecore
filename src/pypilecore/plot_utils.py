from typing import Any, List, Union

from matplotlib import pyplot as plt


def validate_axes_array(axes: Any, shape: Union[int, List[int]]) -> None:
    """
    Validates if the axes argument is an iterable object of a certain shape, filled with
    plt.Axes objects.

    Parameters
    ----------
    axes:
        The presumed array of `plt.Axes` objects
    shape:
        The shape of the `axes` array.
    """
    if isinstance(shape, int):
        shape = [shape]

    try:
        assert len(axes) == shape[0]

        for idx in range(shape[0]):
            if len(shape) > 1:
                validate_axes_array(axes[idx], shape[1:])

            else:
                assert axes[idx] is None or isinstance(axes[idx], plt.Axes)

    except (IndexError, AssertionError, ValueError, TypeError):
        raise ValueError(
            f"""Invalid value for axes argument.
        Provide an array-like with Optional[plt.Axes] objects and shape {shape}."""
        )
