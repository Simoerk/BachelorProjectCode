import math
import matplotlib.pyplot as plt

# Define values
thetas = [0.1, 0.2, 0.4, 0.5, 0.6, 1, 1.5, 2]
epsilons = [0.1, 0.2, 0.5, 1, 1.5, 2]
ts = list(range(1, 1098))  # Start at t=1 to avoid log(0) which is undefined

# Define colors for clearer distinction
colors = ['blue', 'green', 'red', 'cyan', 'magenta', 'yellow', 'orange', 'purple']

def calculate_growth_rate_theta(theta, epsilon):
    return 1 / (theta * epsilon)

def calculate_growth_rate_log(theta, t):
    return math.log(t) ** (1.5 + theta)

# Create a figure with multiple subplots, one for each epsilon
fig, axes = plt.subplots(nrows=1, ncols=len(epsilons), figsize=(20, 5), sharey=True)
fig.suptitle('Growth Rate Functions for Different Theta, Epsilon, and t')

# Plot each subplot
for i, epsilon in enumerate(epsilons):
    for j, theta in enumerate(thetas):
        product_rates = [calculate_growth_rate_log(theta, t) * calculate_growth_rate_theta(theta, epsilon)*math.log(1/0.1) for t in ts]
        axes[i].plot(ts, product_rates, label=f"Theta={theta}", color=colors[j])
    axes[i].set_title(f"Epsilon={epsilon}")
    axes[i].set_xlabel('t')
    axes[i].set_xlim(1, 1098)  # Ensure x-axis starts at 1
    axes[i].set_xticks([1, 500, 1000])  # Set custom ticks to ensure t=1 is marked
    axes[i].grid(True)
    if i == 0:
        axes[i].set_ylabel('Growth Rate')
    axes[i].legend()

plt.tight_layout()
plt.show()
