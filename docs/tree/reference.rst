.. _reference:

Reference
=========

.. _API:
Application programming interface (API)
---------------------------------------

.. autofunction:: pypilecore.api.get_multi_cpt_api_result

.. autofunction:: pypilecore.api.get_multi_cpt_api_report

.. autofunction:: pypilecore.api.get_groups_api_result

.. autofunction:: pypilecore.api.get_groups_api_report


.. _bearingCalculationInput:
Bearing calculation: Input
--------------------------

.. autofunction:: pypilecore.input.multi_cpt.create_multi_cpt_payload

.. autofunction:: pypilecore.input.multi_cpt.create_multi_cpt_report_payload


.. _bearingCalculationResults:
Bearing calculation: Results
----------------------------

.. autoclass:: pypilecore.results.cases_multi_cpt_results.CasesMultiCPTBearingResults
    :members:
    :inherited-members:
    :member-order: bysource

    .. automethod:: __init__

.. autoclass:: pypilecore.results.multi_cpt_results.MultiCPTBearingResults
    :members:
    :inherited-members:
    :member-order: bysource

.. autoclass:: pypilecore.results.multi_cpt_results.SingleCPTBearingResultsContainer
    :members:
    :inherited-members:
    :member-order: bysource

.. autoclass:: pypilecore.results.single_cpt_results.SingleCPTBearingResults
    :members:
    :inherited-members:
    :member-order: bysource

.. autoclass:: pypilecore.results.multi_cpt_results.CPTGroupResultsTable
    :members:
    :inherited-members:
    :member-order: bysource


.. _bearingCalculationViewers:
Bearing calculation: Result Viewers
-----------------------------------

.. autoclass:: pypilecore.viewers.viewer_cpt_results.ViewerCptResults
    :members:
    :inherited-members:
    :member-order: bysource

    .. automethod:: __init__

.. autoclass:: pypilecore.viewers.viewer_cpt_results_plan_view.ViewerCptResultsPlanView
    :members:
    :inherited-members:
    :member-order: bysource

    .. automethod:: __init__

.. autoclass:: pypilecore.viewers.viewer_cpt_group_results.ViewerCptGroupResults
    :members:
    :inherited-members:
    :member-order: bysource

    .. automethod:: __init__

Pile properties: Results
------------------------

.. autofunction:: pypilecore.common.piles.create_basic_pile

.. autoclass:: pypilecore.common.piles.PileProperties
    :members:
    :inherited-members:
    :member-order: bysource

.. autoclass:: pypilecore.common.piles.type.PileType
    :members:
    :inherited-members:
    :member-order: bysource

.. autoclass:: pypilecore.common.piles.geometry.PileGeometry
    :members:
    :inherited-members:
    :member-order: bysource

.. autoclass:: pypilecore.common.piles.geometry._BasePileGeometryComponent
    :members:
    :inherited-members:
    :member-order: bysource

.. autoclass:: pypilecore.common.piles.geometry.PrimaryPileComponentDimension
    :members:
    :inherited-members:
    :member-order: bysource

.. autoclass:: pypilecore.common.piles.geometry.PileMaterial
    :members:
    :inherited-members:
    :member-order: bysource

.. autoclass:: pypilecore.common.piles.geometry.Color
    :members:
    :inherited-members:
    :member-order: bysource


Soil properties: Results
------------------------

.. autoclass:: pypilecore.results.soil_properties.SoilProperties
    :members:
    :inherited-members:
    :member-order: bysource

.. autoclass:: pypilecore.results.soil_properties.CPTTable
    :members:
    :inherited-members:
    :member-order: bysource

.. autoclass:: pypilecore.results.soil_properties.LayerTable
    :members:
    :inherited-members:
    :member-order: bysource




.. _cptGrouperInput:
CPT grouper: Input
------------------

.. autofunction:: pypilecore.input.grouper_properties.create_grouper_payload

.. autofunction:: pypilecore.input.grouper_properties.create_grouper_report_payload


.. _cptGrouperResults:
CPT grouper: Results
--------------------

.. autoclass:: pypilecore.results.grouper_result.GrouperResults
    :members:
    :inherited-members:
    :member-order: bysource

.. autoclass:: pypilecore.results.grouper_result.SingleClusterResult
    :members:
    :inherited-members:
    :member-order: bysource

.. autoclass:: pypilecore.results.grouper_result.SingleClusterData
    :members:
    :inherited-members:
    :member-order: bysource


Post-Processing: Results
-------------------------

.. autoclass:: pypilecore.results.post_processing.MaxBearingResults
    :members:
    :inherited-members:
    :member-order: bysource

.. autoclass:: pypilecore.results.post_processing.MaxBearingResult
    :members:
    :inherited-members:
    :member-order: bysource

.. autoclass:: pypilecore.results.post_processing.MaxBearingTable
    :members:
    :inherited-members:
    :member-order: bysource