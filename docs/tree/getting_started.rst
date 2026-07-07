Getting started
===============


Installation
-------------
To install `py-PileCore`, we strongly recommend using Python Package Index (PyPI).
You can install `py-PileCore` with:

.. code-block:: bash

    pip install py-pilecore


Guided usage
-------------
Getting started with :code:`pypilecore` is easy done by importing the :code:`pypilecore` library:

.. ipython:: python

    import pypilecore

or any equivalent :code:`import` statement.

Create payload
...............

If you're not so comfortable with creating your own schema's the SDK
provides usefully functions to creates a dictionary with the payload
content for the PileCore endpoints. You can find the function at
:code:`pypilecore.input`. Please read the reference page for more information:

- :ref:`bearingCalculationInput`
- :ref:`cptGrouperInput`

.. code-block:: python

    from pypilecore.input import create_multi_cpt_payload

    multi_cpt_payload, passover = create_multi_cpt_payload(
        pile_tip_levels_nap: [0, -1, -2, -3],
        cptdata_objects: [cpt],
        classify_tables: classify,
        groundwater_level_nap: -1,
        friction_range_strategy: "lower_bound",
        pile_type: "A",
        specification: "concrete",,
        installation: "1",
        pile_shape: "rect",
    )


Call endpoint
...............

With the created payload and `nuclei.client
<https://cemsbv.github.io/nuclei/tree/what_is.html>`_
it is possible to create a request. SDK provides functions to assist
with this process:

- :ref:`API`


.. code-block:: python

    from nuclei.client import NucleiClient

    from pypilecore.api import get_multi_cpt_api_result


    client = NucleiClient()
    response = get_multi_cpt_api_result(client, multi_cpt_payload)

Create results
...............

To help the user with generating tables and plots based on the response
of the API call the SDK provides classes that store the data in a structured
way.

- :ref:`bearingCalculationResults`
- :ref:`cptGrouperResults`


.. code-block:: python

    from pypilecore.results import MultiCPTBearingResults

    result = MultiCPTBearingResults.from_api_response(response, passover)


Grouper with custom (externally-computed) bearing results
---------------------------------------------------------

The Grouper does not require you to compute your pile bearing capacities in PileCore. If
you already have per-CPT bearing capacities from other software, you can feed those
"bring-your-own" numbers into the whole Grouper flow — payload, response wrapping,
viewers and report — with a :code:`CustomBearingResults` object, as a near drop-in for a
PileCore-computed :code:`MultiCPTCompressionBearingResults`.

There are two capability tiers:

- **Tier 1 (numbers + coordinates only):** per CPT/pile-tip-level the four bearing
  numbers (:code:`R_b_cal`, :code:`R_s_cal`, :code:`F_nk_d`, :code:`R_c_d_net`) plus the
  CPT coordinates (:code:`x`/:code:`y`). This unlocks the payload, API call, response
  wrapping, the table/scatter/plan viewers and the report.
- **Tier 2 (optional enrichment):** additionally attach a raw CPT trace + soil layers (a
  full :code:`SoilProperties`) to a CPT, which unlocks its per-CPT bearing-overview plot.

Build the custom bearing results
................................

Assemble one :code:`CustomCptBearingResult` per CPT — flat arrays over one shared
pile-tip-level grid — and collect them in a :code:`CustomBearingResults`. All arrays for a
CPT must have the same length, coordinates are required, and the values must be NaN-free
(validated at construction).

.. code-block:: python

    from pypilecore.results import CustomBearingResults, CustomCptBearingResult

    custom_bearing_results = CustomBearingResults(
        [
            CustomCptBearingResult(
                test_id="CPT-1",
                x=122901.28,
                y=484464.34,
                pile_tip_level_nap=[-10.0, -11.0, -12.0],
                R_b_cal=[900.0, 1000.0, 1100.0],
                R_s_cal=[300.0, 320.0, 340.0],
                F_nk_d=[50.0, 50.0, 50.0],
                R_c_d_net=[850.0, 950.0, 1050.0],
            ),
            CustomCptBearingResult(
                test_id="CPT-2",
                x=122916.22,
                y=484415.22,
                pile_tip_level_nap=[-10.0, -11.0, -12.0],
                R_b_cal=[880.0, 980.0, 1080.0],
                R_s_cal=[290.0, 310.0, 330.0],
                F_nk_d=[50.0, 50.0, 50.0],
                R_c_d_net=[830.0, 930.0, 1030.0],
            ),
            # ... at least 2 CPTs, all on the same pile-tip-level grid
        ]
    )

Create the payload and call the endpoint
........................................

Use :code:`create_grouper_payload_from_bearing_results` — the source-agnostic sibling of
:code:`create_grouper_payload` — and call the Grouper endpoint exactly as in the PileCore
workflow.

.. code-block:: python

    from nuclei.client import NucleiClient

    from pypilecore.api import get_groups_api_result
    from pypilecore.input import create_grouper_payload_from_bearing_results

    grouper_payload = create_grouper_payload_from_bearing_results(custom_bearing_results)

    client = NucleiClient()
    grouper_response = get_groups_api_result(client, grouper_payload)

Wrap the response and inspect the results
.........................................

Wrap the response with :code:`GrouperResults.from_grouper_response`, passing your custom
object as the :code:`bearing_results`. The folded :code:`cpt_results` (max net design
bearing capacity per CPT/pile-tip-level) and the case viewers work exactly as for the
PileCore path.

.. code-block:: python

    from pygef.common import Location

    from pypilecore.results import CasesGrouperResults, GrouperResults
    from pypilecore.viewers.viewer_grouper_results_per_cpt_table import (
        ViewerGrouperResultsPerCptTable,
    )

    grouper_results = GrouperResults.from_grouper_response(
        grouper_response,
        pile_load_uls=100,
        bearing_results=custom_bearing_results,
    )

    # Folded max-bearing results: scatter (plot) and plan (map) views.
    max_bearing_results = grouper_results.cpt_results
    max_bearing_results.plot()
    max_bearing_results.map(pile_tip_level_nap=-11.0)

    # Subgroup summary and map.
    grouper_results.plot()
    grouper_results.map()

    # Compare cases in a table viewer.
    cpt_locations = {
        "CPT-1": Location(srs_name="RD", x=122901.28, y=484464.34),
        "CPT-2": Location(srs_name="RD", x=122916.22, y=484415.22),
    }
    cases = CasesGrouperResults(
        results_per_case={"my_case": grouper_results},
        cpt_locations=cpt_locations,
    )
    ViewerGrouperResultsPerCptTable(cases).display()

Generate the report
...................

The report needs nothing from the bearing results beyond the grouper payload and
response, so Tier-1 usage is enough to produce the standard Grouper report.

.. code-block:: python

    from pypilecore.api import get_groups_api_report
    from pypilecore.input import create_grouper_report_payload

    report_payload = create_grouper_report_payload(
        grouper_payload=grouper_payload,
        grouper_response=grouper_response,
        project_name="My project",
        project_id="PRJ-001",
        author="Jane Engineer",
    )
    report = get_groups_api_report(client, report_payload)

Optional: Tier-2 overview plots
...............................

To also produce the per-CPT bearing-overview plot for a CPT, attach a full
:code:`SoilProperties` (raw CPT trace + soil layers) to its record via the
:code:`soil_properties` argument. Its :code:`test_id`/:code:`x`/:code:`y` must match the
values you declared for that CPT. Without it, requesting an overview plot raises a clear
"requires soil data" error, while every Tier-1 flow above keeps working.

.. code-block:: python

    # `soil_properties` is a full pypilecore SoilProperties (with cpt_table + layer_table).
    record = CustomCptBearingResult(
        test_id="CPT-1",
        x=122901.28,
        y=484464.34,
        pile_tip_level_nap=[-10.0, -11.0, -12.0],
        R_b_cal=[900.0, 1000.0, 1100.0],
        R_s_cal=[300.0, 320.0, 340.0],
        F_nk_d=[50.0, 50.0, 50.0],
        R_c_d_net=[850.0, 950.0, 1050.0],
        soil_properties=soil_properties,
    )

    # Unlocks the per-CPT overview plot on the folded result:
    grouper_results.cpt_results["CPT-1"].plot_bearing_overview()