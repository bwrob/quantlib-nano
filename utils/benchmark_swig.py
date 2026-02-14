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
    
    # 1. Determine number of business days and pre-calculate random rates
    temp_date = start_date
    business_days = []
    while temp_date < end_date:
        temp_date = calendar.advance(temp_date, 1, ql.Days)
        business_days.append(temp_date)
    
    num_iterations = len(business_days)
    # Pre-calculate random rates between 1% and 10%
    np.random.seed(42)
    random_rates = np.random.uniform(0.01, 0.10, num_iterations)
    
    print(f"Starting 100Y benchmark: {num_iterations} iterations from {start_date} to {end_date}")
    print("Logic: For each day, create NEW FlatForward curve with random rate and lookup discount.")
    
    results = []
    
    # 2. Benchmark loop
    start_time = time.perf_counter()
    
    for i in range(num_iterations):
        current_date = business_days[i]
        rate = random_rates[i]
        
        # Create NEW curve for every iteration to maximize interface overhead
        yield_curve = ql.FlatForward(start_date, rate, day_count)
        
        # Read discount factor for the current date
        df = yield_curve.discount(current_date)
        results.append((current_date.serialNumber(), df))
        
    end_time = time.perf_counter()
    
    duration = end_time - start_time
    print(f"Benchmark complete.")
    print(f"Total iterations: {num_iterations}")
    print(f"Total time: {duration:.4f} seconds")
    print(f"Time per iteration: {(duration/num_iterations)*1e6:.4f} microseconds")
    
    # Save results
    df_results = pd.DataFrame(results, columns=['serial_date', 'discount_factor'])
    df_results.to_csv('baseline_results.csv', index=False)
    
    metrics = {
        'total_time_sec': duration,
        'iterations': num_iterations,
        'avg_time_microsec': (duration/num_iterations)*1e6,
        'lib_version': ql.__version__,
        'years': years,
        'logic': 'new_curve_per_day'
    }
    
    with open('baseline_metrics.json', 'w') as f:
        json.dump(metrics, f, indent=4)

if __name__ == "__main__":
    run_benchmark()
