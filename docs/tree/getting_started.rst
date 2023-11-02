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