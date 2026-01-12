import numpy as np
from scipy.optimize import fsolve
import json
import os
import math

# load lake data
with open('lakes.json', 'r') as file:
    data = json.load(file)

# extract lake attributes
V_S = data["Superior"]["vol"]
V_M = data["Michigan"]["vol"]
V_H = data["Huron"]["vol"]
V_E = data["Erie"]["vol"]
V_O = data["Ontario"]["vol"]

k_S = data["Superior"]["outflow"] / V_S
k_M = data["Michigan"]["outflow"] / V_M
k_H = data["Huron"]["outflow"] / V_H
k_E = data["Erie"]["outflow"] / V_E
k_O = data["Ontario"]["outflow"] / V_O

# equations for each lake
# Superior
def y_S(t, p=1):
    return V_S * p * np.exp(-k_S * t)

# Michigan
def y_M(t, p=1):
    return V_M * p * np.exp(-k_M * t)

# Huron
def y_H(t, p=1):
    return (200.5 * p * np.exp(-k_S * t) + 
            795.03 * p * np.exp(-k_M * t) - 
            145.53 * p * np.exp(-k_H * t))

# Erie
def y_E(t, p=1):
    return (22.04 * p * np.exp(-k_S * t) + 
            90.79 * p * np.exp(-k_M * t) - 
            17.83 * p * np.exp(-k_H * t) + 
            21 * p * np.exp(-k_E * t))

# Ontario
def y_O(t, p=1):
    return (65.45 * p * np.exp(-k_S * t) + 
            302.80 * p * np.exp(-k_M * t) - 
            76 * p * np.exp(-k_H * t) - 
            32 * p * np.exp(-k_E * t) + 
            132.75 * p * np.exp(-k_O * t))

# computing reduction times assuming clean water inflow
def reduction_50_percent(attributes):
    V = attributes["vol"]
    Q_out = attributes["outflow"]
    result = - (V / Q_out) * math.log(0.5)
    return result

def reduction_5_percent(attributes):
    V = attributes["vol"]
    Q_out = attributes["outflow"]
    result = - (V / Q_out) * math.log(0.05)
    return result

# finding time t when y(t) = target_percentage * initial_mass
def find_time_for_percentage(lake_func, initial_mass, target_percentage, initial_guess=100):
    def equation(t):
        # express equation as lake_func(t) - target_percentage * initial_mass = 0
        return lake_func(t) - target_percentage * initial_mass
    
    solution = fsolve(equation, initial_guess)
    return solution[0]

# lakes and their functions
lakes = {
    "Superior": (y_S, V_S),
    "Michigan": (y_M, V_M),
    "Huron": (y_H, V_H),
    "Erie": (y_E, V_E),
    "Ontario": (y_O, V_O)
}

# p = 1 for simplicity (cancels out anyway)
p = 1

print("Time to reduce pollution to 50%:")
for lake_name, (lake_func, volume) in lakes.items():
    initial_mass = volume * p
    initial_guess = reduction_50_percent(data[lake_name])
    t_50 = find_time_for_percentage(lake_func, initial_mass, 0.5, initial_guess=initial_guess)
    print(f"{lake_name:10s}: {t_50:8.2f} years")

print("\nTime to reduce pollution to 5%:")
for lake_name, (lake_func, volume) in lakes.items():
    initial_mass = volume * p
    initial_guess = reduction_5_percent(data[lake_name])
    t_5 = find_time_for_percentage(lake_func, initial_mass, 0.05, initial_guess=initial_guess)
    print(f"{lake_name:10s}: {t_5:8.2f} years")