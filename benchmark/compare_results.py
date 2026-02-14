import json
import os

def generate_report():
    swig_metrics_path = "benchmark/yield_curve_discount_swig_metrics.json"
    nano_metrics_path = "benchmark/yield_curve_discount_nano_metrics.json"
    
    if not os.path.exists(swig_metrics_path) or not os.path.exists(nano_metrics_path):
        print("Error: Metrics files not found.")
        return

    with open(swig_metrics_path, "r") as f:
        swig = json.load(f)
        
    with open(nano_metrics_path, "r") as f:
        nano = json.load(f)
        
    swig_avg = swig["avg_time_microsec"]
    nano_avg = nano["avg_latency_us"]
    
    speedup = swig_avg / nano_avg
    time_saved = (swig_avg - nano_avg) / swig_avg * 100
    
    # Throughput for SWIG if not present
    swig_ips = swig.get("throughput_ips", swig["iterations"] / swig["total_time_sec"])
    nano_ips = nano["throughput_ips"]
    
    report = f"""
# Benchmark Results: QuantLib-SWIG vs QuantLib-Nano
**Scenario:** 100-Year Daily Discount Factor (25,606 iterations)
**Logic:** In-loop instantiation of Calendar, DayCounter, and FlatForward.

| Metric | QuantLib-SWIG (Official) | QuantLib-Nano (nanobind) | Improvement |
| :--- | :--- | :--- | :--- |
| **Avg Latency** | {swig_avg:.2f} µs | {nano_avg:.2f} µs | **{speedup:.1f}x faster** |
| **Throughput** | {swig_ips:,.0f} iter/s | {nano_ips:,.0f} iter/s | +{((nano_ips/swig_ips)-1)*100:.1f}% |

**Summary:**
QuantLib-Nano achieved a **{speedup:.1f}x** speedup over the official SWIG bindings, reducing average latency from {swig_avg:.2f}µs to {nano_avg:.2f}µs. This represents a **{time_saved:.1f}%** reduction in per-iteration overhead.
"""
    print(report)
    with open("benchmark/comparison_report.md", "w") as f:
        f.write(report)

if __name__ == "__main__":
    generate_report()
