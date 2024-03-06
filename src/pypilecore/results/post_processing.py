import pandas as pd

from pypilecore.results import GrouperResults, MultiCPTBearingResults


def merge_grouper_and_single_bearing_results(
    grouper_results: GrouperResults,
    multi_cpt_bearing_results: MultiCPTBearingResults,
) -> pd.DataFrame:
    """
    Creates a DataFrame with the maximum net design bearing capacity (R_c_d_net) for every CPT.

    Parameters
    ----------
    grouper_results:
       The container that holds multiple SingleClusterResult objects
    multi_cpt_bearing_results:
       The container that holds multiple SingleCPTBearingResults objects

    Returns
    -------
    df:
        A DataFrame that holds the maximum net design bearing capacity (R_c_d_net) for every CPT.
    """
    data = {}
    # iterate over single cpt result
    for _key, result in multi_cpt_bearing_results.cpt_results.cpt_results_dict.items():
        # iterate over pile tip levels single cpt result
        for z, var in zip(result.table.pile_tip_level_nap, result.table.R_c_d_net):
            if result.soil_properties.x is None or result.soil_properties.y is None:
                raise ValueError(
                    f"CPT: {_key} does not have any coordinates set. Please update the SingleCPTBearingResults."
                )
            data[
                frozenset(
                    [
                        round(result.soil_properties.x, 2),
                        round(result.soil_properties.y, 2),
                        round(z, 1),
                    ]
                )
            ] = {
                "x": result.soil_properties.x,
                "y": result.soil_properties.y,
                "z": z,
                "var": var,
                "CPT": _key,
            }

    # iterate over subgroups result
    for cluster in grouper_results.clusters:
        # iterate over cpts in subgroup
        for x, y in cluster.coordinates:
            # iterate over pile tip levels group cpt result
            for z, var in zip(
                cluster.data.pile_tip_level, cluster.data.net_design_bearing_capacity
            ):
                __key = frozenset([round(x, 2), round(y, 2), round(z, 1)])
                # if group result is larger than single result, set group result.
                if var > data[__key]["var"]:
                    data[__key]["var"] = var

    return pd.DataFrame(data.values())
