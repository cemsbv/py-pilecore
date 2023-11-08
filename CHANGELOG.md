# Changelog

All notable changes to this project will be documented in this file.

## [0.2.0] - 2023-11-08

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

### Documentation

- Add missing create_multi_cpt_payload arguments docstrings
- Update `getting started`
- Add items to reference & fix docstrings & typing
- Add single- & multi-cpt-results docstrings
- Init pages (#10)

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

### Deps

- Update mypy==1.6.1 & black==23.10.1

### Refactor

- Don't use relative imports
- [**breaking**] Use classify dict not dataframe (#13)

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

## [0.0.1] - 2023-10-20

### Documentation

- Add docstrings to "create_payload" functions
- Update README

### Styling

- Add github workflow job "lint" & update superlinter to v5
- Add .flake8 file
- Add run_super_linters.sh bash script

### Features

- Clone "pylecore" module content from nuclei-notebooks: nuclei/core/pilecore/api_workflow/pylecore
- Rename module folder name to "py_pilecore"
- Add empty module __init__.py

### Miscellaneous Tasks

- Init pyproject.toml
- Update .gitignore

<!-- CEMS BV. -->
