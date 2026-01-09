from enum import StrEnum
from typing import List


class FrictionRangeStrategy(StrEnum):
    lower_bound = "lower_bound"
    settlement_driven = "settlement_driven"
    manual = "manual"


class SchemaKeys(StrEnum):
    friction_settings = "friction_settings"
    friction_range_strategy = "friction_range_strategy"
    negative_friction = "negative_friction"
    negative_friction_range_nap = "negative_friction_range_nap"
    positive_friction_range_nap = "positive_friction_range_nap"


class FrictionSettings:
    def __init__(
        self,
        friction_range_strategy: (
            str | FrictionRangeStrategy
        ) = FrictionRangeStrategy.lower_bound,
        negative_friction: float | None = None,
        negative_friction_range_nap: List[float] | None = None,
        positive_friction_range_nap: List[float] | None = None,
    ):
        # With loop for compatibility in python 3.11
        assert any(
            item.value == friction_range_strategy for item in FrictionRangeStrategy
        ), f"Invalid value for friction_range_strategy defined, please enter one of {[item.value for item in FrictionRangeStrategy]}"
        self.friction_range_strategy = friction_range_strategy
        self.negative_friction = negative_friction
        self.negative_friction_range_nap = negative_friction_range_nap
        self.positive_friction_range_nap = positive_friction_range_nap

    def serialize_payload(self) -> dict:
        return dict((key, val) for key, val in vars(self).items() if val is not None)
