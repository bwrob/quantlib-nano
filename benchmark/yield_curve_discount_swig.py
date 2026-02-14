import QuantLib as ql
import time
import pandas as pd
import numpy as np
import json

def run_benchmark():
    # Setup
    start_date = ql.Date(14, 2, 2026)
    ql.Settings.instance().evaluationDate = start_date
    
    calendar = ql.TARGET()
    day_count = ql.Actual365Fixed()
    
    years = 100
    end_date = calendar.advance(start_date, years, ql.Years)
    
    # Pre-calculate random rates with safe overhead (approx 252 * 100 = 25,200 days)
    # 40,000 is plenty of overhead.
    np.random.seed(42)
    random_rates = np.random.uniform(0.01, 0.10, 40000)
    
    print(f"Starting 100Y benchmark: from {start_date} to {end_date}")
    print("Logic: Inside loop: advance day -> create NEW curve with random rate -> lookup discount.")
    
    results = []
    current_date = start_date
    
    # Benchmark loop
    start_time = time.perf_counter()
    
    count = 0
    while current_date < end_date:
        # Advance 1 business day (INSIDE loop as requested)
        current_date = calendar.advance(current_date, 1, ql.Days)
        
        # Use pre-calculated random rate
        rate = random_rates[count]
        
        # Create NEW curve for every iteration
        yield_curve = ql.FlatForward(start_date, rate, day_count)
        
        # Read discount factor for the current date
        df = yield_curve.discount(current_date)
        results.append((current_date.serialNumber(), df))
        count += 1
        
    end_time = time.perf_counter()
    
    duration = end_time - start_time
    print(f"Benchmark complete.")
    print(f"Total iterations: {count}")
    print(f"Total time: {duration:.4f} seconds")
    print(f"Time per iteration: {(duration/count)*1e6:.4f} microseconds")
    
    # Save results
    df_results = pd.DataFrame(results, columns=['serial_date', 'discount_factor'])
    df_results.to_csv('benchmark/yield_curve_discount_swig_results.csv', index=False)
    
    metrics = {
        'total_time_sec': duration,
        'iterations': count,
        'avg_time_microsec': (duration/count)*1e6,
        'lib_version': ql.__version__,
        'years': years,
        'logic': 'advance_and_new_curve_per_day'
    }
    
    with open('benchmark/yield_curve_discount_swig_metrics.json', 'w') as f:
        json.dump(metrics, f, indent=4)

if __name__ == "__main__":
    run_benchmark()
