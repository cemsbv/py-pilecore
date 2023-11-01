
Reference
=========

Application programming interface (API)
---------------------------------------

.. autofunction:: pypilecore.api.get_multi_cpt_api_result

.. autofunction:: pypilecore.api.get_multi_cpt_api_report

.. autofunction:: pypilecore.api.get_groups_api_result

.. autofunction:: pypilecore.api.get_optimize_groups_api_result

.. autofunction:: pypilecore.api.get_groups_api_report


Bearing calculation: Input
--------------------------

.. autofunction:: pypilecore.input.multi_cpt.create_multi_cpt_payload

.. autofunction:: pypilecore.input.multi_cpt.create_multi_cpt_report_payload

Bearing calculation: Results
----------------------------

.. autoclass:: pypilecore.results.multi_cpt_results.MultiCPTBearingResults
    :members:
    :inherited-members:
    :member-order: bysource

.. autoclass:: pypilecore.results.multi_cpt_results.SingleCPTBearingResultsContainer
    :members:
    :inherited-members:
    :member-order: bysource

.. autoclass:: pypilecore.results.multi_cpt_results.CPTGroupResultsTable
    :members:
    :inherited-members:
    :member-order: bysource

Pile properties: Results
------------------------

.. autoclass:: pypilecore.results.pile_properties.RoundPileProperties
    :members:
    :inherited-members:
    :member-order: bysource

.. autoclass:: pypilecore.results.pile_properties.RectPileProperties
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


CPT grouper: Input
------------------

.. autofunction:: pypilecore.input.grouper_properties.create_grouper_payload

.. autofunction:: pypilecore.input.grouper_properties.create_grouper_report_payload


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
