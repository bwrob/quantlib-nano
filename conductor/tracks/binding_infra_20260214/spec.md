# Specification: Minimal Binding Infrastructure for Benchmarking

## Overview
Prepare a simple, focused binding infrastructure using `nanobind` and `litgen` to expose the minimal set of QuantLib 1.41 classes required for the 50-year discount factor benchmark on macOS. This track depends on the results of the "Establish SWIG Baseline & Benchmark Design" track to finalize the exact C++ scope.

## Dependencies
- **Track:** `baseline_benchmark_20260214` (Establish SWIG Baseline & Benchmark Design). The exact C++ classes and headers to be exposed will be determined by the output of this dependency.

## Functional Requirements
- **QuantLib Integration:** Integrate QuantLib 1.41 as a git submodule.
- **Binding Generation:** Implement a generation script using `litgen` and `nanobind` driven by a single `benchmark_scope.toml` file.
- **Scope of Exposure (Initial estimate, to be finalized by dependency):**
    - \`Date\` class and basic arithmetic.
    - \`Calendar\` (specifically \`TARGET\`).
    - \`DayCounter\` (specifically \`Actual365Fixed\`).
    - \`YieldTermStructure\` (specifically \`FlatForward\` and templated \`PiecewiseYieldCurve\` with common interpolators).
- **Template Handling:** Develop a strategy in \`litgen\` for instantiating common QuantLib templates (e.g., \`InterpolatedYieldCurve<Linear>\`) to ensure functional parity.
- **Build System:** Configure \`CMake\` and \`scikit-build-core\` to compile the extension module.
- **Type Safety:** Automatically generate `.pyi` type stubs for all exposed classes.

## Non-Functional Requirements
- **Performance:** Ensure minimal call overhead in the generated bindings.
- **Platform:** Target macOS as the primary development and benchmarking environment.
- **Simplicity:** Keep the infrastructure minimal, focusing only on the requirements for the benchmark.

## Acceptance Criteria
- Extension module successfully compiles on macOS.
- Python script can import the module and instantiate the core classes identified in the benchmark design.
- Type stubs (`.pyi`) are generated and recognized by IDEs/type checkers.

## Out of Scope
- Exposing the full QuantLib API.
- Support for non-macOS platforms (in this track).
