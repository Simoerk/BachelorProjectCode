import numpy as np
import pandas as pd
import math

# Function to apply the Laplace mechanism along with the value for differential privacy 
def laplace_mechanism(value, sensitivity, epsilon):
    # The sensitivity of a sum query is 1
    scale = sensitivity / epsilon
    # Generate Laplace noise
    noise = np.random.laplace(0, scale)
    return value + noise

# Function to apply the Laplace mechanism for differential privacy with sensititivy 1
def laplace_mechanism_2(sensitivity, epsilon):
    # The sensitivity of a sum query is 1
    #sensitivity = 1
    scale = sensitivity / epsilon
    # Generate Laplace noise
    noise = np.random.laplace(0, scale)
    return noise


# Function to apply the Laplace mechanism for differential privacy with sensitivity
def laplace_mechanism_sensitivity(epsilon, sensitivity):
    # The sensitivity of a sum query is 1
    scale = sensitivity / epsilon
    # Generate Laplace noise
    noise = np.random.laplace(0, scale)
    return noise

# Define the ai function based on Corollary 4.4
def ai(i, theta):
    # Implementing ai as per Corollary 4.4
    return (i + 1)**(1 + theta)