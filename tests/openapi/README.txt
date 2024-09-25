The openapi.yaml file is used for testing/validation of py-pilecore and should be a modified copy of the latest PileCore-API openapi.yaml file.

Required modifications:
    - Remove all security settings (components/SecuritySchemes + security property on each endpoint)