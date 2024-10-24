# Changelog

All notable changes to this project will be documented in this file.

## [0.8.0] - 2024-10-24

### Features

- *(begemann)* Add Begemann method to compute excavation stress after excavation

## [0.7.1] - 2024-10-01

### Bug Fixes

- *(viewer_results)* Fix error of not finding color for NaN results for ViewerCptResultsPlanView

### Miscellaneous Tasks

- *(cleanup)* Remove unused file

## [0.7.0] - 2024-09-25

### Features

- *(grouper)* #93 Throw ValueError when providing less than 2 CPTs to create_grouper_payload()
- *(coords)* #81 Only add coordinates to soil_properties payload when not None

### Miscellaneous Tasks

- Clear nb outputs
- *(deps)* Bump peaceiris/actions-gh-pages from 3 to 4
- *(deps)* Bump peaceiris/actions-gh-pages from 3 to 4
- *(deps)* Bump peaceiris/actions-gh-pages from 3 to 4
- *(deps)* Bump peaceiris/actions-gh-pages from 3 to 4
- *(deps)* Bump peaceiris/actions-gh-pages from 3 to 4
- *(deps)* Bump peaceiris/actions-gh-pages from 3 to 4
- *(deps)* Bump peaceiris/actions-gh-pages from 3 to 4
- *(deps)* Bump peaceiris/actions-gh-pages from 3 to 4
- *(deps)* Bump peaceiris/actions-gh-pages from 3 to 4
- *(deps)* Bump peaceiris/actions-gh-pages from 3 to 4
- *(deps)* Bump peaceiris/actions-gh-pages from 3 to 4
- Dependabot[bot] <support@github.com>
- *(get-super-linter-dependencies)* Add bash script to fetch superlinter dependencies for tag
- *(deps)* Bump platformdirs from 3.5.1 to 4.1.0
- *(deps)* Bump platformdirs from 3.5.1 to 4.1.0
- *(deps)* Bump platformdirs from 3.5.1 to 4.1.0
- *(deps)* Bump platformdirs from 3.5.1 to 4.1.0
- *(deps)* Bump platformdirs from 3.5.1 to 4.1.0
- *(deps)* Bump platformdirs from 3.5.1 to 4.1.0
- *(deps)* Bump platformdirs from 3.5.1 to 4.1.0
- *(deps)* Bump platformdirs from 3.5.1 to 4.1.0
- *(deps)* Bump platformdirs from 3.5.1 to 4.1.0
- *(deps)* Bump platformdirs from 3.5.1 to 4.1.0
- *(deps)* Bump platformdirs from 3.5.1 to 4.1.0
- Dependabot[bot] <support@github.com>
- *(deps)* Bump actions/setup-python from 4 to 5
- *(deps)* Bump actions/setup-python from 4 to 5
- *(deps)* Bump actions/setup-python from 4 to 5
- *(deps)* Bump actions/setup-python from 4 to 5
- *(deps)* Bump actions/setup-python from 4 to 5
- *(deps)* Bump actions/setup-python from 4 to 5
- *(deps)* Bump actions/setup-python from 4 to 5
- *(deps)* Bump actions/setup-python from 4 to 5
- *(deps)* Bump actions/setup-python from 4 to 5
- *(deps)* Bump actions/setup-python from 4 to 5
- Dependabot[bot] <support@github.com>
- *(deps)* Bump actions/upload-artifact from 3 to 4
- *(deps)* Bump actions/upload-artifact from 3 to 4
- *(deps)* Bump actions/upload-artifact from 3 to 4
- *(deps)* Bump actions/upload-artifact from 3 to 4
- *(deps)* Bump actions/upload-artifact from 3 to 4
- *(deps)* Bump actions/upload-artifact from 3 to 4
- *(deps)* Bump actions/upload-artifact from 3 to 4
- *(deps)* Bump actions/upload-artifact from 3 to 4
- *(deps)* Bump actions/upload-artifact from 3 to 4
- *(deps)* Bump actions/upload-artifact from 3 to 4
- Dependabot[bot] <support@github.com>

### Testing

- *(multi-cpt-input)* Add minimal testcases for create_multi_cpt_payload(), using openapi-core lib

## [0.6.0] - 2024-09-13

### Documentation

- *(viewer_results)* Add the ViewerCptResults to the sphinx docs

### Features

- *(viewer_results)* Add the results viewer ViewerCptResultsPlanView
- *(viewer_results)* Add the results viewer ViewerCptGroupResults
- *(viewer_results)* Add ViewerCptResults class
- *(cases_multicpt)* Add class CasesMultiCPTBearingResults
- *(cases_multicpt)* Add class CasesMultiCPTBearingResults (#76)
- *(cases_multicpt)* Add class CasesMultiCPTBearingResults (#76)
- *(cases_multicpt)* Add class CasesMultiCPTBearingResults (#76)
- *(cases_multicpt)* Add class CasesMultiCPTBearingResults (#76)
- *(cases_multicpt)* Add class CasesMultiCPTBearingResults (#76)
- *(cases_multicpt)* Add class CasesMultiCPTBearingResults (#76)
- Pablo Vasconez <p.vasconez@cemsbv.io>

### Miscellaneous Tasks

- *(cases_multicpt)* Add CasesMultiCPTBearingResults to the init of the results module

### Refactor

- *(cases_multicpt)* Refactor ResultTypes to ResultDefinitions

### Testing

- *(viewer_results)* Add tests for the ViewerCptResults

## [0.5.1] - 2024-09-13

### Bug Fixes

- Use correct axis to remove missing values (resolve #73)

## [0.5.0] - 2024-07-22

### Miscellaneous Tasks

- !refactor: pile properties in line with pilecore api v3 definition (#72)
- * chore(deps): Regenerate requirements.txt with pip-compile & python3.9
- * !feat: Refactor PileProperties object & schema mapping to API-V3.0
- * chore: Update mypy settings
- * fix: RectangleGeometryComponent.plot() offset fix
- * chore: Import pile objects in parent modules
- * docs: Update PileProperties objects in docs
- * chore: fix linting
- * perf(deps): bump nuclei to v1.0.0 and fix API version in NUCLEI CLIENT
- * docs(notebook): add pile geometry definitions figure to notebook
- * chore(deps): bump dependencies with pip-compile
- * chore(docs): add image to git trace
- * fix: resolve Matplotlib deprecation warning
- * fix: resolve runtime warning, close figures
- * build: bump python version to 9.10 for docs jobs
- ---------
- Thijs Lukkezen <t.lukkezen@cemsbv.io>
- Robin Wimmers <r.wimmers@cemsbv.io>

## [0.4.2] - 2024-05-17

### Features

- *(#64)* Auto convert pile-type-specification inputs to strings
- Bandwidth of attribute; resolve #69 (#70)
- Bandwidth of attribute; resolve #69 (#70)
- Bandwidth of attribute; resolve #69 (#70)
- Bandwidth of attribute; resolve #69 (#70)
- Bandwidth of attribute; resolve #69 (#70)

## [0.4.1] - 2024-05-02

### Documentation

- Add SingleCPTBearingResults reference to docs
- Update warning description

### Features

- *(#40)* Pass soil_load=0.0 when input is None.
- Delaunay tessellation (#63)
- Delaunay tessellation (#63)
- Delaunay tessellation (#63)
- Delaunay tessellation (#63)
- Delaunay tessellation (#63)
- Delaunay tessellation (#63)
- Delaunay tessellation (#63)
- Delaunay tessellation (#63)

### Miscellaneous Tasks

- Upgrade dependencies with pip-compile

## [0.4.0] - 2024-03-12

### Bug Fixes

- Final max-bearing fixups & Add unittests
- Do array comparison on float with np.isclose()
- Remove dataclass hash & to_pandas caching
- Make sure that all pile tip levels have same order
- Remove dataclass hash & to_pandas caching
- Fix MaxBearingResults initiation & refactor
- Update unit test
- Add missing pile definitions plot

### Features

- Rotate x-labels in 2D max-bearing plot
- Add lru_cache on MaxBearingResults.to_pandas
- Make SingleCPTBearingResultsContainer.cpt_results_dict a read-only property
- Add methods to MaxBearingResults to align signature with SingleCPTBearingResultsContainer
- Denote CPT name in MaxBeraingTable.origin attribute
- Add delaunay map
- Resolve comments in mr
- Add result bearing 3d plots to notebook
- Add 3D plots for bearing results
- Combine grouper and single results
- *(api)* Add verbose argument to functions in api module

### Miscellaneous Tasks

- Update example notebook
- Revert

### Styling

- Lint file
- Format file and fix typing errors

## [0.3.4] - 2024-02-16

### Bug Fixes

- Raise RuntimeError with /get-task-status response "msg" value instead of "status_code" when "state"=="FAILURE"

## [0.3.3] - 2024-02-14

### Bug Fixes

- *(ci)* Use PyPi tokenless authentication

### Features

- *(individual-friction-ranges)* Set soil-properties friction-range-strategy to "manual" when providing a value in the individual-friction-range input

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
- *(grouper)* Make sure that pile tip levels are sorted (#38)
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
- Notebook and grouper workflow (#18)
- Notebook and grouper workflow (#18)
- Notebook and grouper workflow (#18)
- Notebook and grouper workflow (#18)
- Notebook and grouper workflow (#18)
- Notebook and grouper workflow (#18)
- Notebook and grouper workflow (#18)
- Notebook and grouper workflow (#18)
- Notebook and grouper workflow (#18)
- Notebook and grouper workflow (#18)
- Notebook and grouper workflow (#18)
- Notebook and grouper workflow (#18)
- Notebook and grouper workflow (#18)
- Notebook and grouper workflow (#18)
- Notebook and grouper workflow (#18)
- Notebook and grouper workflow (#18)
- Notebook and grouper workflow (#18)
- Notebook and grouper workflow (#18)
- Notebook and grouper workflow (#18)
- Notebook and grouper workflow (#18)
- Notebook and grouper workflow (#18)
- Notebook and grouper workflow (#18)
- Notebook and grouper workflow (#18)
- Notebook and grouper workflow (#18)
- Notebook and grouper workflow (#18)
- Notebook and grouper workflow (#18)
- Thijs Lukkezen <t.lukkezen@cemsbv.io>
- Assure that `CPTTable.depth_nap` attribute always has a dimension to satisfy pandas
- Plot empty cone resistance `qc` in CPTTable.plot_friction_ratio()
- Plot empty friction ratio in CPTTable.plot_friction_ratio()
- Correctly create MultiCPTResults object from api response with cascading from_api_response class_methods strategy
- Check arbitrary arrays for nan values with pd.isnull() instead of np.isnan() for better consistency
- Fix adding diameter_shaft property logic
- *(test)* Coverage warning no data was collected

### Documentation

- Add missing create_multi_cpt_payload arguments docstrings
- Update `getting started`
- Add items to reference & fix docstrings & typing
- Add single- & multi-cpt-results docstrings
- Init pages (#10)
- Init pages (#10)
- Init pages (#10)
- Init pages (#10)
- Init pages (#10)
- Init pages (#10)
- Init pages (#10)
- Init pages (#10)
- Init pages (#10)
- Init pages (#10)
- Init pages (#10)
- Init pages (#10)
- Init pages (#10)
- Init pages (#10)
- Init pages (#10)
- Init pages (#10)
- Init pages (#10)
- Init pages (#10)
- Init pages (#10)
- Init pages (#10)
- Init pages (#10)
- Init pages (#10)
- Init pages (#10)
- Init pages (#10)
- Init pages (#10)
- Init pages (#10)
- Init pages (#10)
- Init pages (#10)
- Init pages (#10)
- Init pages (#10)
- Init pages (#10)
- Init pages (#10)

### Features

- Cast property getter responses of PileProperties & child objects
- Add `name` property to PileProperties object
- Add _shape class-attribute to Round- & RectPileProperties
- Raise ValueError for invalid pile_properties `height_base` input.
- Add notebook example (#17)
- Add notebook example (#17)
- Cast CPTGroupResultsTable attributes to numpy arrays
- *(grouper)* Add grouper implementation (#7)
- *(grouper)* Add grouper implementation (#7)
- *(grouper)* Add grouper implementation (#7)
- *(grouper)* Add grouper implementation (#7)
- *(grouper)* Add grouper implementation (#7)
- *(grouper)* Add grouper implementation (#7)
- *(grouper)* Add grouper implementation (#7)
- *(grouper)* Add grouper implementation (#7)
- *(grouper)* Add grouper implementation (#7)
- *(grouper)* Add grouper implementation (#7)
- *(grouper)* Add grouper implementation (#7)
- *(grouper)* Add grouper implementation (#7)
- *(grouper)* Add grouper implementation (#7)
- *(grouper)* Add grouper implementation (#7)
- *(grouper)* Add grouper implementation (#7)
- *(grouper)* Add grouper implementation (#7)
- *(grouper)* Add grouper implementation (#7)
- *(grouper)* Add grouper implementation (#7)

### Miscellaneous Tasks

- Parse each commit message line as commit for changelog
- Add notebook example (#17)
- Add public/ to .gitignore
- Add pypi release job to ci (#14)
- *(docs)* Update branches name
- Init pages (#10)
- Init pages (#10)
- Init pages (#10)
- Init pages (#10)
- Init pages (#10)
- Init pages (#10)
- Init pages (#10)
- Init pages (#10)
- Init pages (#10)
- Init pages (#10)
- Init pages (#10)
- Init pages (#10)
- *(docs)* Add docs test and deploy job
- *(grouper)* Add grouper implementation (#7)
- *(grouper)* Add grouper implementation (#7)
- *(grouper)* Add grouper implementation (#7)
- *(grouper)* Add grouper implementation (#7)
- *(changelog)* Update changelog version & add auto-generate settings

### Refactor

- Don't use relative imports
- [**breaking**] Use classify dict not dataframe (#13)
- [**breaking**] Use classify dict not dataframe (#13)
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
