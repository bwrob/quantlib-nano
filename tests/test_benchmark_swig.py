from utils.benchmark_swig import run_benchmark
import os

def test_benchmark_runs():
    # Run the benchmark (should not raise error)
    run_benchmark()
    
    # Check if files were created
    assert os.path.exists('baseline_results.csv')
    assert os.path.exists('baseline_metrics.json')
