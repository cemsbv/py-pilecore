from dataclasses import dataclass, field, fields, replace
from typing import Literal, TypeVar, Type
import pandas as pd
from pathlib import Path
import ast
import numpy as np
from pypilecore.common.norms import Norms

T = TypeVar("T", bound="InputCase")

# Custom parsers for columns with python object from strings in the input file
CUSTOM_PARSERS = {
    "pile_tip_levels_nap": lambda s: np.array(ast.literal_eval(s)),
    "individual_ocr": ast.literal_eval,
    "individual_negative_friction_range_nap": ast.literal_eval,
    "individual_positive_friction_range_nap": ast.literal_eval,
    "fixed_negative_friction_range_nap": ast.literal_eval,
    "fixed_positive_friction_range_nap": ast.literal_eval,
}

@dataclass
class InputCase:
    # Names and general information
    case_name: str = "default"
    reference: (
        Literal ["B1", "B2", "B3", "B4", "B5", "B6", "B7", "B8", 
                 "S1", "S2", "S4", "S3", "S5", "S6", "S7", 
                 "H1", "H2", 
                 "MA1", "MA2", "MB1", "MB2", "MC", "MD", "ME", "MF" ] | None) = None
    pile_name: str = "unnamed"
    installation: (
        Literal["driven", "screwed", "excavated", "vibrated", "pressed", "jetted"] | None) = None
    pile_material: (
        Literal["concrete", "steel", "wood", "grout", "grout_extorted"] | None) = None
    custom_material: dict | None = None
    # Geometry and dimensions
    pile_shape: str = "round"
    core_diameter: float | None = None
    base_diameter: float | None = None
    core_secondary_dimension: float | None = None
    core_tertiary_dimension: float | None = None
    base_secondary_dimension: float | None = None
    base_tertiary_dimension: float | None = None
    height_base: float | None = None
    pile_head_level_nap: str | float = "surface"
    pile_tip_levels_nap: list[float] = field(default_factory=list)
    groundwater_level_nap: str | float | None = None
    # Load parameters
    stiff_construction: bool = False
    pile_load_uls: float | None = None
    relative_pile_load: float = 0.7
    pile_load_sls: float | None = None
    soil_load_sls: float | None = None
    # Norms and other factors
    nen_9997_1: str = "2025"
    cur_236: str = "2023"
    gamma_r_b: float = 1.2
    gamma_r_s: float = 1.2
    gamma_f_nk: float = 1.0
    overrule_xi: dict = field(default_factory=dict)
    settlement_curve: int = 1
    # Pile parameters
    alpha_p: float | None = None
    alpha_s_clay: float | None = None
    alpha_s_sand: float | None = None
    beta_p: float | None = None
    alpha_t_clay: float | None = None
    alpha_t_sand: float | None = None
    pile_tip_factor_s: float | None = None
    is_auger: bool = False
    is_low_vibrating: bool = False
    is_prefab: bool = False
    is_open_ended: bool = False
    negative_fr_delta_factor: float | None = None
    # OCR parameters
    ocr: float | None = None
    individual_ocr: dict = field(default_factory=dict)
    # Shaft friction parameters
    negative_shaft_friction: float | None = None
    friction_range_strategy: str = "lower_bound"
    individual_negative_friction_range_nap: dict = field(default_factory=dict)
    individual_positive_friction_range_nap: dict = field(default_factory=dict)
    fixed_negative_friction_range_nap: list[float] = field(default_factory=list)
    fixed_positive_friction_range_nap: list[float] = field(default_factory=list)
    adhesion: float | None = None
    # Excavation parameters
    excavation_depth_nap: float | None = None
    excavation_param_t: float = 1.0
    excavation_stress_reduction_method: str = "constant"
    excavation_width: float | None = None
    excavation_edge_distance: float | None = None
    # CPT limits
    use_almere_rules: bool = False
    apply_qc3_reduction: bool = False
    qc_z_a_lesser_1m: float | None = None
    qc_z_a_greater_1m: float | None = None
    qb_max_limit: float | None = None
    chamfered: float | None = None

    def __post_init__(self):
        """Force validation of each new instance
        """        
        self.validate_case()

    @classmethod
    def from_globals(cls: Type[T], globals_dict: dict) -> T:
        """
        Create an InputCase instance from a dictionary of global variables.

        Args:
            globals_dict (dict): A dictionary containing global variables.
        """
        return cls(**{f.name: globals_dict[f.name] for f in fields(cls) if f.name in globals_dict})
    
    @classmethod
    def from_row(cls: Type[T], base: T, row: pd.Series) -> T:
        """
        Create an InputCase instance from a base InputCase and a dictionary of row data.

        Args:
            row (dict): A dictionary containing row data to override the base instance.
        """
        overrides = _normalize(row)
        _warn_unknown(overrides, cls)
        new_case = replace_case(base, **overrides)
        return new_case

    @classmethod
    def from_file(cls: Type[T], base: T, file_name: str) -> list[T]:
        """
        Create a list of InputCase instances from a CSV file.

        Args:
            file_name (str): The path to the CSV file containing input cases.
        """
        input_cases_df = read_input_cases(file_name)
        input_cases = [base]  # Start with the base case
        if not input_cases_df.empty:
            for _, row in input_cases_df.iterrows():
                new_case = cls.from_row(base, row)
                input_cases.append(new_case)
        return input_cases
    
    def validate_case(self) -> None:
        """
        Check the validity of the InputCase instance.
        Raises ValueError if any attribute is invalid.
        """
        #TODO: Add more checks to perform on the input case. For now, just check some basic things.
        if self.pile_shape not in ["round", "square"]:
            raise ValueError(f"Invalid pile_shape: {self.pile_shape}. Must be 'round' or 'square'.")
        if self.core_diameter is not None and self.core_diameter <= 0:
            raise ValueError(f"core_diameter must be positive. Got: {self.core_diameter}")
        if self.base_diameter is not None and self.base_diameter <= 0:
            raise ValueError(f"base_diameter must be positive. Got: {self.base_diameter}")
        if self.pile_load_uls is not None and self.pile_load_uls < 0:
            raise ValueError(f"pile_load_uls must be non-negative. Got: {self.pile_load_uls}")
        if self.gamma_r_b <= 0:
            raise ValueError(f"gamma_r_b must be positive. Got: {self.gamma_r_b}")

    @property
    def basic_pile_kwargs(self) -> dict:
        """Returns kwargs for calling the `create_basic_pile` function

        Returns
        -------
        dict
            Kwargs for calling the `create_basic_pile` function
        """        
        return {
            "pile_shape": self.pile_shape,
            "pile_name": self.pile_name,
            "reference": self.reference,
            "installation": self.installation,
            "height_base": self.height_base,
            "core_secondary_dimension": self.core_secondary_dimension,
            "core_tertiary_dimension": self.core_tertiary_dimension,
            "base_secondary_dimension": self.base_secondary_dimension,
            "base_tertiary_dimension": self.base_tertiary_dimension,
            "core_diameter": self.core_diameter,
            "base_diameter": self.base_diameter,
            "pile_material": self.pile_material,
            "custom_material": self.custom_material,
            "settlement_curve": self.settlement_curve,
            "adhesion": self.adhesion,
            "alpha_p": self.alpha_p,
            "alpha_s_clay": self.alpha_s_clay,
            "alpha_s_sand": self.alpha_s_sand,
            "beta_p": self.beta_p,
            "alpha_t_clay" : self.alpha_t_clay,
            "alpha_t_sand" : self.alpha_t_sand,
            "pile_tip_factor_s": self.pile_tip_factor_s,
            "is_auger": self.is_auger,
            "is_low_vibrating": self.is_low_vibrating,
            "is_prefab" : self.is_prefab,
            "is_open_ended" : self.is_open_ended,
            "negative_fr_delta_factor": self.negative_fr_delta_factor,
            "qc_z_a_lesser_1m": self.qc_z_a_lesser_1m,
            "qc_z_a_greater_1m": self.qc_z_a_greater_1m,
            "qb_max_limit": self.qb_max_limit,
            "chamfered" : self.chamfered
        }
    
    @property
    def multi_cpt_payload_kwargs(self) -> dict:
        """Return kwargs for calling the `create_multi_cpt_payload` function

        Returns
        -------
        dict
            Kwargs for calling the `create_multi_cpt_payload` function
        """        
        return {
            "groundwater_level_nap": self.groundwater_level_nap,
            "friction_range_strategy": self.friction_range_strategy,
            "excavation_depth_nap": self.excavation_depth_nap,
            "individual_negative_friction_range_nap": self.individual_negative_friction_range_nap,
            "individual_positive_friction_range_nap": self.individual_positive_friction_range_nap,
            "excavation_param_t": self.excavation_param_t,
            "excavation_stress_reduction_method": self.excavation_stress_reduction_method,
            "excavation_width": self.excavation_width,
            "excavation_edge_distance": self.excavation_edge_distance,
            "pile_head_level_nap": self.pile_head_level_nap,
            "pile_load_sls": self.pile_load_sls,
            "pile_tip_levels_nap": self.pile_tip_levels_nap,
            "relative_pile_load" : self.relative_pile_load,
            "apply_qc3_reduction" : self.apply_qc3_reduction,
            "negative_shaft_friction": self.negative_shaft_friction,
            "fixed_negative_friction_range_nap": self.fixed_negative_friction_range_nap,
            "fixed_positive_friction_range_nap": self.fixed_positive_friction_range_nap,
            "norms" : Norms(
                nen_9997_1=self.nen_9997_1,
                cur_236=self.cur_236,),
            "gamma_f_nk": self.gamma_f_nk,
            "gamma_r_b": self.gamma_r_b,
            "gamma_r_s": self.gamma_r_s,
            "overrule_xi": self.overrule_xi,
            "soil_load_sls": self.soil_load_sls,
            "use_almere_rules" : self.use_almere_rules,
            "stiff_construction" : self.stiff_construction,
            "ocr" : self.ocr,
            "individual_ocr" : self.individual_ocr,
        }

def replace_case(base: T, **overrides) -> T:
    """
    Returns a new InputCase instance with updated attributes (uses built-in dataclass.replace function).

    Args:
        base (InputCase): The base InputCase instance to copy from.
        **overrides: Keyword arguments representing attributes to override in the new instance.
    """
    return replace(base, **overrides)

def _normalize(row: pd.Series) -> dict:
    #TODO: Implement robust normalization logic for missing (nan's) columns resulting from parsing of the input_file
    parsed_row = {}
    for colname, colvalue in row.to_dict().items():
        if colname in CUSTOM_PARSERS and pd.notnull(colvalue):
            try:
                parsed_row[colname] = CUSTOM_PARSERS[colname](colvalue)
            except (ValueError, SyntaxError) as e:
                print(f"Warning: Failed to parse column '{colname}' with value '{colvalue}': {e}")
        elif pd.notnull(colvalue):
            parsed_row[colname] = colvalue
    return parsed_row

def _warn_unknown(row: dict, cls: Type[T]) -> None:
    """
    Warn about unknown keys in the row dictionary that are not attributes of the InputCase class.

    Args:
        row (dict): A dictionary containing row data.
        cls (Type[InputCase]): The InputCase class type.
    """
    # TODO: Check types - is row a dictionary?
    known_fields = {f.name for f in fields(cls)}
    unknown_keys = set(row.keys()) - known_fields
    if unknown_keys:
        print(f"Warning: Unknown keys in input case data: {unknown_keys}")

def read_input_cases(file_name: str) -> pd.DataFrame:
    """
    Read input cases from a CSV file and return them as a pandas DataFrame.

    Args:
        file_name (str): The path to the CSV file containing input cases.
    Returns:
        pd.DataFrame: A DataFrame containing the input cases read from the file. Possibly empty if the file does not exist.
    """
    input_file_path = Path(file_name)
    if input_file_path.is_file():
        print(f"Reading input cases from {input_file_path}")
        input_cases_df = pd.read_csv(input_file_path)
        return input_cases_df
    else:
        print(f"Calculating base case only, no input file found at {input_file_path}")
        return pd.DataFrame()
