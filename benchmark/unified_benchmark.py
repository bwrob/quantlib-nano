import sys
import os
import time
import numpy as np

# Add build directory to path for nano
sys.path.append(os.path.join(os.getcwd(), "build"))

def run_swig_benchmark(iterations):
    import QuantLib as ql
    
    start_date = ql.Date(14, 2, 2026)
    ql.Settings.instance().evaluationDate = start_date
    calendar = ql.TARGET()
    day_count = ql.Actual365Fixed()
    rate = 0.03
    
    dates = []
    curr = start_date
    for _ in range(iterations):
        curr = calendar.advance(curr, 1, ql.Days)
        dates.append(curr)
        
    latencies = []
    for d in dates:
        t0 = time.perf_counter()
        yield_curve = ql.FlatForward(start_date, rate, day_count)
        _ = yield_curve.discount(d)
        t1 = time.perf_counter()
        latencies.append((t1 - t0) * 1_000_000)
        
    return latencies

def run_nano_benchmark(iterations):
    import quantlib_nano_cpp as ql
    
    start_date = ql.Date(14, ql.Month.February, 2026)
    ql.Settings.instance().evaluationDate = start_date
    calendar = ql.TARGET()
    day_count = ql.Actual365Fixed()
    rate = 0.03
    
    dates = []
    curr = start_date
    for _ in range(iterations):
        curr = calendar.advance(curr, 1, ql.TimeUnit.Days)
        dates.append(curr)
        
    latencies = []
    for d in dates:
        t0 = time.perf_counter()
        yield_curve = ql.FlatForward(start_date, rate, day_count)
        _ = yield_curve.discount(d)
        t1 = time.perf_counter()
        latencies.append((t1 - t0) * 1_000_000)
        
    return latencies

def print_rich_table(swig_lats, nano_lats):
    def get_stats(data):
        return {
            "avg": np.mean(data),
            "std": np.std(data),
            "min": np.min(data),
            "p50": np.percentile(data, 50),
            "p95": np.percentile(data, 95),
            "p99": np.percentile(data, 99),
            "max": np.max(data),
        }

    s = get_stats(swig_lats)
    n = get_stats(nano_lats)
    
    speedup = s['avg'] / n['avg']
    
    print("")
    print("=" * 70)
    print(f"{'QuantLib Binding Comparison (100Y Discount Factor)':^70}")
    print("=" * 70)
    print(f"{'Metric':<15} | {'SWIG (Official)':>15} | {'Nano (nanobind)':>15} | {'Speedup':>15}")
    print("-" * 70)
    
    metrics = [
        ("Avg Latency", "avg", "us"),
        ("Median (p50)", "p50", "us"),
        ("p95 Latency", "p95", "us"),
        ("p99 Latency", "p99", "us"),
        ("Min Latency", "min", "us"),
        ("Max Latency", "max", "us"),
        ("Std Dev", "std", "us"),
    ]
    
    for label, key, unit in metrics:
        sv = s[key]
        nv = n[key]
        rel = sv / nv if nv > 0 else 0
        print(f"{label:<15} | {sv:>12.2f} {unit} | {nv:>12.2f} {unit} | {rel:>14.1f}x")
        
    print("-" * 70)
    swig_ips = 1_000_000 / s['avg']
    nano_ips = 1_000_000 / n['avg']
    print(f"{'Throughput':<15} | {swig_ips:>10,.0f} iter/s | {nano_ips:>10,.0f} iter/s | {nano_ips/swig_ips:>14.1f}x")
    print("=" * 70)
    print(f"Summary: QuantLib-Nano is {speedup:.1f}x faster than SWIG.")
    print("=" * 70)
    print("")

if __name__ == "__main__":
    ITERATIONS = 25606
    print(f"Running benchmarks ({ITERATIONS} iterations each)...")
    
    swig_latencies = run_swig_benchmark(ITERATIONS)
    print("SWIG benchmark complete.")
    
    nano_latencies = run_nano_benchmark(ITERATIONS)
    print("Nano benchmark complete.")
    
    print_rich_table(swig_latencies, nano_latencies)
