# Implementation Plan: Establish SWIG Baseline & Benchmark Design

## Phase 1: Environment & Baseline Setup

- [x] Task: Set up \`uv\` environment with official \`QuantLib\` and \`pandas/numpy\` for benchmarking. (uv sync complete)
- [x] Task: Create a prototype script to verify official binding functionality (Date, Calendar, YieldCurve). (.help/verify_quantlib.py)
- [ ] Task: Conductor - User Manual Verification 'Phase 1: Environment & Baseline Setup' (Protocol in workflow.md)

## Phase 2: Benchmark Design & Execution

- [ ] Task: Implement the 50-year daily advancement benchmark script.
- [ ] Task: Execute the benchmark and record performance results (JSON/CSV).
- [ ] Task: Analyze the benchmark script to extract the list of required C++ headers for nanobind.
- [ ] Task: Conductor - User Manual Verification 'Phase 2: Benchmark Design & Execution' (Protocol in workflow.md)
