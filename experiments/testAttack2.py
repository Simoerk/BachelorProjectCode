import numpy as np
import math

def laplace_noise(scale):
   return np.random.laplace(0, scale)

def generate_noisy_value(x, epsilon):
    n = laplace_noise(1 / epsilon)
    return x + n


epsilon = 1

binary_list = [1,0,0,1,1,0,0,1,1,0,1,1,0,1,0,0,1,1,1,0,1,0,0,1]
binary_sum_list = [1,1,1,2,3,3,3,4,5,5,6,7,7,8,8,8,9,10,11,11,12,12,12,13,13,14,15,16,17,17,17,18]

print(len(binary_sum_list))

for i in binary_sum_list:
    # Generate noisy value for x_plus_n_1
    x_plus_n_1 = generate_noisy_value(binary_sum_list[i], epsilon)

    # Determine x_bar
    if x_plus_n_1 < 0.5:
        x_bar1 = 0
    else:
        x_bar1 = 1
    prob1 = 1 - 0.5 * math.exp((-epsilon)*0.5)

    # Increase to next time step
    i = i+1

    # Find x_bar2
    value_2 = binary_sum_list[i] - x_bar1

    # Generate noisy value for x_plus_n_2
    x_plus_n_2 = generate_noisy_value(binary_sum_list[i], epsilon)

    # Determine x_bar2
    if x_plus_n_2 < 0.5:
        x_bar2 = 0
    else:
        x_bar2 = 1
    prob2 = 1 - 0.5 * math.exp((-epsilon)*0.5)

    





