# Specification: Establish SWIG Baseline & Benchmark Design

## Goal
Establish a performance baseline using the official QuantLib SWIG bindings and identify the minimum set of C++ headers required to replicate the benchmark with nanobind.

## Scope
- Set up a Python environment with the official `QuantLib` package.
- Design and implement a 50-year benchmark script (Daily Calendar advancement + Discount Factor lookup).
- Document the exact C++ classes and headers used in the benchmark.
- Record baseline performance metrics (time, memory).

## Success Criteria
- Benchmark script runs successfully with official bindings.
- A list of required QuantLib C++ headers is generated for the next track.
- Performance baseline is recorded in the project.
