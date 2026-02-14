# Implementation Plan: Establish SWIG Baseline & Benchmark Design

## Phase 1: Environment & Baseline Setup [checkpoint: a45f7b2]

- [x] Task: Set up \`uv\` environment with official \`QuantLib\` and \`pandas/numpy\` for benchmarking. (uv sync complete)
- [x] Task: Create a prototype script to verify official binding functionality (Date, Calendar, YieldCurve). (.help/verify_quantlib.py)
- [x] Task: Conductor - User Manual Verification 'Phase 1: Environment & Baseline Setup' (Protocol in workflow.md)

## Phase 2: Benchmark Design & Execution [checkpoint: 1e05762]

- [x] Task: Implement the 50-year daily advancement benchmark script. (utils/benchmark_swig.py)
- [x] Task: Execute the benchmark and record performance results (JSON/CSV). (baseline_metrics.json)
- [x] Task: Analyze the benchmark script to extract the list of required C++ headers for nanobind. (required_headers.txt)
- [x] Task: Conductor - User Manual Verification 'Phase 2: Benchmark Design & Execution' (Protocol in workflow.md)
