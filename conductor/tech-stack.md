# Technology Stack - quantlib-nano

## C++ Core

- **Language Standard:** C++17 (Aligning with QuantLib 1.41+).
- **Core Library:** QuantLib (v1.41+) managed via **Git Submodules**.
- **Binding Engine:** `nanobind` for high-performance Python/C++ interoperability.
- **Binding Generator:** `litgen` (Literate Generator) for automated binding creation.

## Build System & Infrastructure

- **C++ Build System:** CMake.
- **Python Build Backend:** `scikit-build-core` (to bridge CMake and Python packaging).
- **Python Package Manager:** `uv` for environment management and dependency resolution.
- **Compiler:** System-provided (GCC, Clang, or MSVC) with mandatory **-O3** and **-march=native** (or equivalent) for performance benchmarking.

## Configuration & Meta-data

- **Configuration Format:** **TOML** for storing binding generation rules, version-specific overrides, and project metadata (separated from scripts to allow for future multi-version support).

## Python Environment

- **Target Versions:** Python 3.10+ (to support modern type annotations and ensure longevity).
- **Dependencies:** `nanobind`, `litgen`, `nanobind-stubgen`, `numpy` (for benchmarking).
