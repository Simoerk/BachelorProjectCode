import numpy as np
import pandas as pd
import math

# Function to apply the Laplace mechanism for differential privacy with sensititivy 1
def laplace_mechanism(epsilon):
    # The sensitivity of a sum query is 1
    #sensitivity = 1
    #scale = sensitivity / epsilon
    # Generate Laplace noise
    noise = np.random.laplace(0, epsilon)
    return noise


# Function to apply the Laplace mechanism for differential privacy with sensitivity
def laplace_mechanism_sensitivity(epsilon, sensitivity):
    # The sensitivity of a sum query is 1
    scale = sensitivity / epsilon
    # Generate Laplace noise
    noise = np.random.laplace(0, scale)
    return noise