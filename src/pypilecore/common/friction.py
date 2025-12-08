from enum import StrEnum

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
    def __init__(self, 
                 friction_range_strategy = FrictionRangeStrategy.lower_bound, 
                 negative_friction = None, 
                 negative_friction_range_nap = None, 
                 positive_friction_range_nap = None):
        self.friction_range_strategy = friction_range_strategy
        self.negative_friction = negative_friction
        self.negative_friction_range_nap = negative_friction_range_nap
        self.positive_friction_range_nap = positive_friction_range_nap
    def serialize_payload(self):
        return dict((key,val) for key,val in vars(self).items() if val is not None)
