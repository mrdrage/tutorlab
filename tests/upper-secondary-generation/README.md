# Upper Secondary Generation v0.8 tests

Run the complete TutorLab local suite from repository root:

```bash
python3 tools/run_local_validation.py
```

The v0.8-specific checks are:

```bash
python3 tools/check_upper_secondary_schemas.py
python3 tools/check_upper_secondary_architecture.py
python3 tools/check_upper_secondary_capability_boundary.py
python3 tools/check_cross_stage_recovery_bridge.py
python3 tools/check_upper_secondary_generation_coverage.py
python3 tools/check_upper_secondary_generation_quality.py
python3 tools/check_upper_secondary_generator_alignment.py
python3 tools/check_upper_secondary_vertical_slices.py
```

No GitHub Actions workflow is used. A merge is acceptable only after the v0.8-specific checks have either been executed on a complete local checkout or their modified runtime boundaries have been equivalently exercised and the execution limitation is documented in the PR.
