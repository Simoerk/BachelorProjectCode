import numpy as np
import pandas as pd
import math

# Function to apply the Laplace mechanism for differential privacy
def laplace_mechanism(epsilon):
    # The sensitivity of a sum query is 1
    sensitivity = 1
    scale = sensitivity / epsilon
    # Generate Laplace noise
    noise = np.random.laplace(0, scale)
    return noise
