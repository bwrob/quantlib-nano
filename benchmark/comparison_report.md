
# Benchmark Results: QuantLib-SWIG vs QuantLib-Nano
**Scenario:** 100-Year Daily Discount Factor (25,606 iterations)
**Logic:** In-loop instantiation of Calendar, DayCounter, and FlatForward.

| Metric | QuantLib-SWIG (Official) | QuantLib-Nano (nanobind) | Improvement |
| :--- | :--- | :--- | :--- |
| **Avg Latency** | 6.66 µs | 0.93 µs | **7.2x faster** |
| **Throughput** | 150,221 iter/s | 993,315 iter/s | +561.2% |

**Summary:**
QuantLib-Nano achieved a **7.2x** speedup over the official SWIG bindings, reducing average latency from 6.66µs to 0.93µs. This represents a **86.0%** reduction in per-iteration overhead.
