import numpy as np
import math

def laplace_noise(scale):
    return np.random.laplace(0, scale)

def generate_noisy_value(x, epsilon):
    n = laplace_noise(1 / epsilon)
    return x + n

def determine_interval(value, intervals):
    for i, (start, end) in enumerate(intervals):
        if start <= value < end:
            return i
    # If the value is exactly 1, assign it to the last interval
    if value == 1:
        return len(intervals) - 1
    return None

def perform_attack(values, intervals, epsilon, num_samples):
    attack_results = {x: [] for x in values}
    
    for x in values:
        for _ in range(num_samples):
            noisy_value = generate_noisy_value(x, epsilon)
            interval_index = determine_interval(noisy_value, intervals)
            if interval_index is not None:
                attack_results[x].append(interval_index)
    
    return attack_results

def analyze_results(attack_results, intervals):
    analysis = {}
    num_intervals = len(intervals)
    
    for x, noisy_intervals in attack_results.items():
        interval_counts = [0] * num_intervals
        for interval_index in noisy_intervals:
            interval_counts[interval_index] += 1
        
        total = len(noisy_intervals)
        interval_probs = [count / total for count in interval_counts]
        
        analysis[x] = {
            "counts": interval_counts,
            "probs": interval_probs,
        }
    
    return analysis

def infer_original_intervals(attack_results, intervals, epsilon):
    analysis = analyze_results(attack_results, intervals)
    inferred_intervals = {}
    
    for x, data in analysis.items():
        max_prob = max(data["probs"])
        inferred_interval_index = data["probs"].index(max_prob)
        inferred_intervals[x] = intervals[inferred_interval_index]
    
    return inferred_intervals

def attack_continuous_dataset(values, intervals, epsilon, num_samples):
    attack_results = perform_attack(values, intervals, epsilon, num_samples)
    inferred_intervals = infer_original_intervals(attack_results, intervals, epsilon)
    
    for x, inferred_interval in inferred_intervals.items():
        print(f"Original x = {x:.3f}, Inferred interval = {inferred_interval}")
    
    return inferred_intervals

# Parameters
epsilon = 1
num_samples = 1000
# Example values between 0 and 1
values = np.linspace(0, 1, 10)
# Define intervals
intervals = [(0, 0.2), (0.2, 0.4), (0.4, 0.6), (0.6, 0.8), (0.8, 1)]

# Perform attack on continuous dataset
inferred_intervals = attack_continuous_dataset(values, intervals, epsilon, num_samples)

print(1 - 0.5 * math.exp((-epsilon)*0.5))