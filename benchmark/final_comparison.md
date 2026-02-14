Running benchmarks (25606 iterations each)...
SWIG benchmark complete.
Nano benchmark complete.

======================================================================
          QuantLib Binding Comparison (100Y Discount Factor)          
======================================================================
Metric          | SWIG (Official) | Nano (nanobind) |         Speedup
----------------------------------------------------------------------
Avg Latency     |         3.00 us |         0.82 us |            3.6x
Median (p50)    |         2.79 us |         0.79 us |            3.5x
p95 Latency     |         3.08 us |         0.88 us |            3.5x
p99 Latency     |         6.08 us |         1.04 us |            5.8x
Min Latency     |         2.46 us |         0.67 us |            3.7x
Max Latency     |        99.63 us |        36.58 us |            2.7x
Std Dev         |         1.78 us |         0.44 us |            4.1x
----------------------------------------------------------------------
Throughput      |    332,999 iter/s |  1,215,061 iter/s |            3.6x
======================================================================
Summary: QuantLib-Nano is 3.6x faster than SWIG.
======================================================================

