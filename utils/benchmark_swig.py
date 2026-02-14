import QuantLib as ql
import time
import pandas as pd
import numpy as np

def run_benchmark():
    # Setup
    start_date = ql.Date(14, 2, 2026)
    ql.Settings.instance().evaluationDate = start_date
    
    calendar = ql.TARGET()
    day_count = ql.Actual365Fixed()
    risk_free_rate = 0.05
    yield_curve = ql.FlatForward(start_date, risk_free_rate, day_count)
    yield_curve.enableExtrapolation()
    
    years = 50
    # Approximate business days in 50 years (50 * ~252)
    # We'll advance day-by-day until we hit 50 years from start
    end_date = calendar.advance(start_date, years, ql.Years)
    
    current_date = start_date
    results = []
    
    print(f"Starting benchmark: 50 years from {start_date} to {end_date}")
    
    start_time = time.perf_counter()
    
    count = 0
    while current_date < end_date:
        # Advance 1 business day
        current_date = calendar.advance(current_date, 1, ql.Days)
        # Read discount factor
        df = yield_curve.discount(current_date)
        results.append((current_date.serialNumber(), df))
        count += 1
        
    end_time = time.perf_counter()
    
    duration = end_time - start_time
    print(f"Benchmark complete.")
    print(f"Total iterations: {count}")
    print(f"Total time: {duration:.4f} seconds")
    print(f"Time per iteration: {(duration/count)*1e6:.4f} microseconds")
    
    # Save results for comparison later
    df_results = pd.DataFrame(results, columns=['serial_date', 'discount_factor'])
    df_results.to_csv('baseline_results.csv', index=False)
    
    metrics = {
        'total_time_sec': duration,
        'iterations': count,
        'avg_time_microsec': (duration/count)*1e6,
        'lib_version': ql.__version__
    }
    
    import json
    with open('baseline_metrics.json', 'w') as f:
        json.dump(metrics, f, indent=4)

if __name__ == "__main__":
    run_benchmark()
