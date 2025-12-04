from dataclasses import dataclass
from enum import Enum
from typing import Hashable

import pandas as pd

from pypilecore.results.result_definitions import ResultDefinition


class ResultsPandasColumn(Enum):
    CASE_NAME = "case_name"
    TEST_ID = "test_id"
    X = "x"
    Y = "y"
    PILE_TIP_LEVEL_NAP = "pile_tip_level_nap"
    RESULT_NAME = "result_name"
    RESULT = "result"
    RESULT_UNIT = "result_unit"


@dataclass
class CptResultsTable:
    case_name: list[Hashable]
    result_def: list[ResultDefinition]
    result_value: list[float]
    test_id: list[str]
    x: list[float]
    y: list[float]
    pile_tip_level_nap: list[float]

    @classmethod
    def initialize(cls) -> "CptResultsTable":
        return cls(
            case_name=[],
            result_def=[],
            result_value=[],
            test_id=[],
            x=[],
            y=[],
            pile_tip_level_nap=[],
        )

    def add_entry(
        self,
        case_name: Hashable,
        result_def: ResultDefinition,
        test_id: str,
        x: float | int,
        y: float | int,
        pile_tip_level_nap: float,
        result_value: float,
    ) -> None:
        """
        Add an data entry to the CPT results table.
        """
        self.case_name.append(case_name)
        self.result_def.append(result_def)
        self.test_id.append(test_id)
        self.x.append(x)
        self.y.append(y)
        self.pile_tip_level_nap.append(pile_tip_level_nap)
        self.result_value.append(result_value)

    def to_pandas(self) -> pd.DataFrame:
        """
        Return the CPT results as a pandas DataFrame.
        """
        return pd.DataFrame(
            {
                "case_name": self.case_name,
                "test_id": self.test_id,
                "x": self.x,
                "y": self.y,
                "pile_tip_level_nap": self.pile_tip_level_nap,
                "result_name": [rd.name for rd in self.result_def],
                "result": self.result_value,
                "result_unit": [rd.unit for rd in self.result_def],
            }
        )
