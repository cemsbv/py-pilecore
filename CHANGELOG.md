# Changelog

All notable changes to this project will be documented in this file.

## [1.1.1] - 2025-05-05

### Documentation

#### Pilecore_tension

- Adding docstrings for top_of_tension_zone_nap and ocr


## [1.1.0] - 2025-05-05

### Features

#### Pilecore_tension

- Add begemann excavation stress reducion in tension create_multi_cpt_payload


## [1.0.4] - 2025-04-30

### Documentation

#### Args

- Improving the type hints and docstrings of groundwater_level_nap and excavation_depth_nap


## [1.0.3] - 2025-04-30

### Documentation

#### Args_docstring

- Improving the docstring of the arguments of several methods

#### Create_basic_pile

- Remove types from docstrings to that they are generated from the type hints


### Miscellaneous Tasks

#### Ci

- Move from dependabot to renovate


## [1.0.2] - 2025-04-16

### Bug Fixes

#### Ci

- Use ubuntu-latest for docs CI

#### Viewers

- Fix rendering of result viewers in jupyter notebooks


### Miscellaneous Tasks

#### Deps

- Bump cfn-lint from 1.25.1 to 1.33.2


## [1.0.1] - 2025-04-15

### Bug Fixes

#### Deps

- Update cems-nuclei to get rid of the ipython dependency
- Allow future fixes of anywidget
- Require dependency patch of cems-nuclei


## [1.0.0] - 2025-04-08

### Bug Fixes

#### Deps

- Use correct dependencies for documentation
- Use version 2 of cems-nuclei
- Update and pin all dependencies to latest version


### Refactor

#### Python

- [**breaking**] Bump minimum supported Python version to 3.11


## [0.9.2] - 2025-04-08

### Features

#### Custom_chamfer

- Add custom chamfer limits and qb_max

#### Tension

- Add construction sequence to tension result payload and the example notebook


## [0.9.1] - 2025-02-19

### Bug Fixes

#### Rounding

- Fix rounding of pile tip levels to be 2 decimals


## [0.9.0] - 2025-02-14

### Bug Fixes

#### Deps

- Downgrade plotly to v5


### Features


## [0.8.3] - 2025-01-10

### Miscellaneous Tasks

#### Notebook

- Reduce the amount of requested pile tip levels in order for notebook to be usable with free account


## [0.8.2] - 2024-11-27

### Bug Fixes

#### Pile_name

- Guarantee that PileProperties.name returns a string or None


## [0.8.1] - 2024-11-20

### Features

#### Depth

- Use penetrationLength cpt trace if depth is not present


### Testing


### Deps


## [0.8.0] - 2024-10-24

### Features

#### Begemann

- Add Begemann method to compute excavation stress after excavation


## [0.7.1] - 2024-10-01

### Bug Fixes

#### Viewer_results

- Fix error of not finding color for NaN results for ViewerCptResultsPlanView


### Miscellaneous Tasks

#### Cleanup

- Remove unused file


## [0.7.0] - 2024-09-25

### Features

#### Coords

- #81 Only add coordinates to soil_properties payload when not None

#### Grouper

- #93 Throw ValueError when providing less than 2 CPTs to create_grouper_payload()


### Miscellaneous Tasks

#### Deps

- Bump peaceiris/actions-gh-pages from 3 to 4
- Bump platformdirs from 3.5.1 to 4.1.0
- Bump actions/setup-python from 4 to 5
- Bump actions/upload-artifact from 3 to 4

#### Get-super-linter-dependencies

- Add bash script to fetch superlinter dependencies for tag


### Testing

#### Multi-cpt-input

- Add minimal testcases for create_multi_cpt_payload(), using openapi-core lib


## [0.6.0] - 2024-09-13

### Documentation

#### Viewer_results

- Add the ViewerCptResults to the sphinx docs


### Features

#### Cases_multicpt

- Add class CasesMultiCPTBearingResults
- Add class CasesMultiCPTBearingResults (#76)

#### Viewer_results

- Add the results viewer ViewerCptResultsPlanView
- Add the results viewer ViewerCptGroupResults
- Add ViewerCptResults class


### Miscellaneous Tasks

#### Cases_multicpt

- Add CasesMultiCPTBearingResults to the init of the results module


### Refactor

#### Cases_multicpt

- Refactor ResultTypes to ResultDefinitions


### Testing

#### Viewer_results

- Add tests for the ViewerCptResults


## [0.5.1] - 2024-09-13

### Bug Fixes


## [0.4.2] - 2024-05-17

### Features

#### #64

- Auto convert pile-type-specification inputs to strings


## [0.4.1] - 2024-05-02

### Documentation


### Features

#### #40

- Pass soil_load=0.0 when input is None.


### Miscellaneous Tasks


## [0.4.0] - 2024-03-12

### Bug Fixes


### Features

#### Api

- Add verbose argument to functions in api module


### Miscellaneous Tasks


### Styling


## [0.3.4] - 2024-02-16

### Bug Fixes


## [0.3.3] - 2024-02-14

### Bug Fixes

#### Ci

- Use PyPi tokenless authentication


### Features

#### Individual-friction-ranges

- Set soil-properties friction-range-strategy to "manual" when providing a value in the individual-friction-range input


## [0.3.2] - 2024-01-15

### Bug Fixes


## [0.3.1] - 2024-01-04

### Bug Fixes


### Features

#### Ocr

- Add ocr input to multi-cpt bearing


## [0.3.0] - 2023-12-05

### Features


### Refactor


## [0.2.5] - 2023-12-05

### Bug Fixes

#### Grouper

- Use design value for grouper negative friction (#42)
- Make sure that pile tip levels are sorted (#38)


### Documentation

#### Notebook

- Update example notebook


### Miscellaneous Tasks


### Refactor


## [0.2.3] - 2023-11-17

### Bug Fixes


## [0.2.2] - 2023-11-17

### Documentation

#### Grouper

- Update plot a summary docstring


### Miscellaneous Tasks

#### Notebook

- Rearrangement of the PileCore_multi_cpt_grouper jupyter-notebook


### Refactor


### Testing


## [0.2.1] - 2023-11-09

### Features


## [0.2.0] - 2023-11-08

### Bug Fixes

#### Test

- Coverage warning no data was collected


### Documentation


### Features

#### Grouper

- Add grouper implementation (#7)


### Miscellaneous Tasks

#### Changelog

- Update changelog version & add auto-generate settings

#### Docs

- Update branches name
- Add docs test and deploy job


### Refactor


### Testing


### Deps


## [0.0.1] - 2023-10-20

### Documentation


### Features


### Miscellaneous Tasks


### Styling


<!-- CEMS BV. -->
