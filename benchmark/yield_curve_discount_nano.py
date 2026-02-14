import sys
import os
import time
import csv
import json

# Add build directory to path to import the generated module
sys.path.append(os.path.join(os.getcwd(), "build"))

import quantlib_nano_cpp as ql

def run_benchmark(iterations=25606):
    # Benchmark setup
    start_date = ql.Date(14, ql.Month.February, 2026)
    ql.Settings.instance().evaluationDate = start_date
    
    calendar = ql.TARGET()
    day_count = ql.Actual365Fixed()
    rate = 0.03
    
    # Pre-calculate business days for 100 years
    dates = []
    curr = start_date
    for _ in range(iterations):
        curr = calendar.advance(curr, 1, ql.TimeUnit.Days)
        dates.append(curr)
        
    # Benchmark loop
    results = []
    total_start = time.perf_counter()
    
    for d in dates:
        iter_start = time.perf_counter()
        
        # Mirror SWIG benchmark logic exactly
        # 1. Instantiate FlatForward
        yield_curve = ql.FlatForward(start_date, rate, day_count)
        
        # 2. Calculate discount factor
        df = yield_curve.discount(d)
        
        iter_end = time.perf_counter()
        results.append((iter_end - iter_start) * 1_000_000)  # microseconds
        
    total_end = time.perf_counter()
    total_duration = total_end - total_start
    
    # Calculate metrics
    avg_latency = sum(results) / len(results)
    min_latency = min(results)
    max_latency = max(results)
    p95_latency = sorted(results)[int(len(results) * 0.95)]
    p99_latency = sorted(results)[int(len(results) * 0.99)]
    
    metrics = {
        "total_duration_s": total_duration,
        "iterations": len(results),
        "avg_latency_us": avg_latency,
        "min_latency_us": min_latency,
        "max_latency_us": max_latency,
        "p95_latency_us": p95_latency,
        "p99_latency_us": p99_latency,
        "throughput_ips": len(results) / total_duration
    }
    
    return metrics, results

if __name__ == "__main__":
    print("Starting QuantLib-Nano Benchmark (100Y Daily Discount Factor)...")
    metrics, raw_results = run_benchmark()
    
    print(f"Completed {metrics['iterations']} iterations.")
    print(f"Average Latency: {metrics['avg_latency_us']:.2f} us")
    print(f"Throughput: {metrics['throughput_ips']:.2f} iterations/sec")
    
    # Save results
    os.makedirs("benchmark", exist_ok=True)
    
    with open("benchmark/yield_curve_discount_nano_metrics.json", "w") as f:
        json.dump(metrics, f, indent=4)
        
    with open("benchmark/yield_curve_discount_nano_results.csv", "w", newline='') as f:
        writer = csv.writer(f)
        writer.writerow(["iteration", "latency_us"])
        for i, res in enumerate(raw_results):
            writer.writerow([i, res])
            
    print("Results saved to benchmark/yield_curve_discount_nano_*")
