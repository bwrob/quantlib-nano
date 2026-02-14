# Implementation Plan: Minimal Binding Infrastructure for Benchmarking

## Phase 1: Core C++ & Build Setup

- [ ] Task: Integrate QuantLib 1.41 as a git submodule in the `external/` directory.
- [ ] Task: Set up the initial `CMakeLists.txt` for building the C++ extension with `nanobind`.
- [ ] Task: Configure `pyproject.toml` with `scikit-build-core` and project metadata.
- [ ] Task: Conductor - User Manual Verification 'Phase 1: Core C++ & Build Setup' (Protocol in workflow.md)

## Phase 2: Binding Generation Infrastructure

- [ ] Task: Write Tests: Verification of TOML configuration loading for `litgen`.
- [ ] Task: Implement: The binding generation script (`generate_bindings.py`) using `litgen`.
- [ ] Task: Write Tests: Mock generation of a simple C++ class to verify `litgen` integration.
- [ ] Task: Implement: Logic to handle the `benchmark_scope.toml` and map it to `litgen` calls.
- [ ] Task: Conductor - User Manual Verification 'Phase 2: Binding Generation Infrastructure' (Protocol in workflow.md)

## Phase 3: Exposing Core Classes & Verification

- [ ] Task: Finalize `benchmark_scope.toml` based on the output of `baseline_benchmark_20260214`.
- [ ] Task: Execute the binding generation for the target QuantLib classes (`Date`, `Calendar`, etc.).
- [ ] Task: Compile the extension module and generate `.pyi` type stubs.
- [ ] Task: Implement: A verification script (`verify_bindings.py`) to test basic instantiation and methods in Python.
- [ ] Task: Conductor - User Manual Verification 'Phase 3: Exposing Core Classes & Verification' (Protocol in workflow.md)
