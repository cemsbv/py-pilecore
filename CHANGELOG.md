# Changelog

All notable changes to this project will be documented in this file.

## [0.3.2] - 2024-01-15

### Bug Fixes

- Don't filter NaN values in the table result from SingleCPTBearingResultsContainer.get_results_per_cpt()

## [0.3.1] - 2024-01-04

### Bug Fixes

- Update ocr parameters & height_base in multi-cpt-grouper notebook
- Fix response variable scope

### Features

- *(ocr)* Add ocr input to multi-cpt bearing

## [0.3.0] - 2023-12-05

### Features

- Extract R_s_d and R_b_d from group_results_table (requires PileCore-API >= 2.9.0)

### Refactor

- Pass payload properties explicitly in `from_api_response` methods, instead of dumping the content as keyword arguments

## [0.2.5] - 2023-12-05

### Bug Fixes

- *(grouper)* Use design value for grouper negative friction (#42)
- *(grouper)* Make sure that pile tip levels are sorted (#38)

### Documentation

- *(notebook)* Update example notebook

### Miscellaneous Tasks

- Update gitignore

### Refactor

- Reword GrouperResults.plot docstring

## [0.2.3] - 2023-11-17

### Bug Fixes

- Get-task-status doesn't return traceback, but status_code

## [0.2.2] - 2023-11-17

### Documentation

- *(grouper)* Update plot a summary docstring

### Miscellaneous Tasks

- *(notebook)* Rearrangement of the PileCore_multi_cpt_grouper jupyter-notebook
- Add coveralls badge to readme

### Refactor

- Replace relative imports

### Testing

- Add tests for multi_cpt_result and soil_properties result objects

## [0.2.1] - 2023-11-09

### Features

- Minor fixups in PileCore_multi_cpt notebook
- Validate excavation and pile-load input in function create_multi_cpt_payload
- Accept None for `relative_pile_load`

## [0.2.0] - 2023-11-08

### Bug Fixes

- Notebook and grouper workflow (#18)
- Assure that `CPTTable.depth_nap` attribute always has a dimension to satisfy pandas
- Plot empty cone resistance `qc` in CPTTable.plot_friction_ratio()
- Plot empty friction ratio in CPTTable.plot_friction_ratio()
- Correctly create MultiCPTResults object from api response with cascading from_api_response class_methods strategy
- Check arbitrary arrays for nan values with pd.isnull() instead of np.isnan() for better consistency
- Fix adding diameter_shaft property logic
- *(test)* Coverage warning no data was collected

### Co-authored-by

- Thijs Lukkezen <t.lukkezen@cemsbv.io>

### Documentation

- Add missing create_multi_cpt_payload arguments docstrings
- Update `getting started`
- Add items to reference & fix docstrings & typing
- Add single- & multi-cpt-results docstrings
- Init pages (#10)

### Features

- Cast property getter responses of PileProperties & child objects
- Add `name` property to PileProperties object
- Add _shape class-attribute to Round- & RectPileProperties
- Raise ValueError for invalid pile_properties `height_base` input.
- Add notebook example (#17)
- Cast CPTGroupResultsTable attributes to numpy arrays
- *(grouper)* Add grouper implementation (#7)

### Miscellaneous Tasks

- Parse each commit message line as commit for changelog
- Add public/ to .gitignore
- Add pypi release job to ci (#14)
- *(docs)* Update branches name
- *(docs)* Add docs test and deploy job
- *(changelog)* Update changelog version & add auto-generate settings

### Refactor

- Don't use relative imports
- [**breaking**] Use classify dict not dataframe (#13)

### Testing

- Add create_multi_cpt_payload unit-tests
- Add soilproperties tests
- Omit tests folder in superlinter
- Add multi-cpt-results tests
- Refactor pile_properties tests
- Add results/test_pile_properties tests
- Move grouper tests to "results" folder
- Add create_pile_properties_payload tests
- Rename test_soil to test_input

### Deps

- Update mypy==1.6.1 & black==23.10.1

## [0.0.1] - 2023-10-20

### Documentation

- Add docstrings to "create_payload" functions
- Update README

### Features

- Clone "pylecore" module content from nuclei-notebooks: nuclei/core/pilecore/api_workflow/pylecore
- Rename module folder name to "py_pilecore"
- Add empty module __init__.py

### Miscellaneous Tasks

- Init pyproject.toml
- Update .gitignore

### Styling

- Add github workflow job "lint" & update superlinter to v5
- Add .flake8 file
- Add run_super_linters.sh bash script

<!-- CEMS BV. -->
