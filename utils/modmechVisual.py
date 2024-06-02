import math
import matplotlib.pyplot as plt

# Visualize the modified mechanism error bounds for different theta, epsilon, and t, same delta

# Define values
thetas = [0.1, 0.2, 0.5, 1, 1.5]
epsilons = [0.1, 0.2, 0.5, 1, 1.5]
ts = list(range(1, 101))  # Generate a range of t from 1 to 100

# Define a color for each theta
colors = {
    0.1: 'blue', 
    0.2: 'green', 
    0.5: 'red', 
    1: 'cyan', 
    1.5: 'magenta', 
    2: 'yellow'
}

def calculate_growth_rate_theta(theta, epsilon):
    return 1 / (theta * epsilon)

def calculate_growth_rate_log(theta, t):
    if t > 0:
        return math.log(t) ** (1.5 + theta)
    else:
        return 0  # Prevent math domain error if t is 0

# Create a figure with multiple subplots, one for each epsilon
fig, axes = plt.subplots(nrows=1, ncols=len(epsilons), figsize=(20, 4), sharey=True)
fig.suptitle('Comparison of Growth Rate Functions for Different Theta, Epsilon, and t')

# Plot each subplot
for i, epsilon in enumerate(epsilons):
    for theta in thetas:
        color = colors[theta]  # Get color for the current theta
        growth_rates_log = [calculate_growth_rate_log(theta, t) for t in ts]
        growth_rate_theta = calculate_growth_rate_theta(theta, epsilon)
        axes[i].plot(ts, growth_rates_log, label=f"log(t)^(1.5+{theta})", color=color)
        axes[i].axhline(y=growth_rate_theta, color=color, linestyle='--', label=f"1/(theta*epsilon)" if theta == thetas[0] else "")
    axes[i].set_title(f"Epsilon={epsilon}")
    axes[i].set_xlabel('t')
    axes[i].set_xlim(1, 100)  # Explicitly set x-axis limits from 1 to 100
    axes[i].set_xticks([1, 20, 40, 60, 80, 100])  # Set custom ticks to ensure t=1 is marked
    axes[i].grid(True)
    if i == 0:
        axes[i].set_ylabel('Growth Rate')
    axes[i].set_ylim(0, 110)  # Adjusting y-axis limit for better visibility of all lines

# Add a legend to the first subplot for clarity
axes[0].legend()

plt.tight_layout(rect=[0, 0.03, 1, 0.95])
plt.show()
