from benchmark.yield_curve_discount_swig import run_benchmark
import os

def test_benchmark_runs():
    # Run the benchmark (should not raise error)
    run_benchmark()
    
    # Check if files were created
    assert os.path.exists('benchmark/yield_curve_discount_swig_results.csv')
    assert os.path.exists('benchmark/yield_curve_discount_swig_metrics.json')
