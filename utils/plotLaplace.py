import numpy as np
import matplotlib.pyplot as plt

def laplace_distribution(x, sensitivity, epsilon):
    b = sensitivity / epsilon
    return (1 / (2 * b)) * np.exp(-np.abs(x) / b)

# Define sensitivity and epsilon values
sensitivities = [0.5, 1, 2, 3]
epsilons = [0.2, 0.5, 1, 1.5, 2]

# Generate x values
x = np.linspace(-10, 10, 400)

# Create the plot
plt.figure(figsize=(10, 6))


# Plot the Laplace distributions for each sensitivity
for sensitivity, epsilon in zip(sensitivities, epsilons):
    y = laplace_distribution(x, sensitivity, epsilon)
    plt.plot(x, y, label=f'sensitivity = {sensitivity}')
    plt.plot(x, y, label=f'epsilon = {epsilon}')
        

# Add title and labels
plt.title('Laplace Distribution for Different Epsilon Values')
plt.xlabel('x')
plt.ylabel('Density')
plt.legend()
plt.grid(True)

# Show the plot
plt.show()
