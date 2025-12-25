import numpy as np
import matplotlib.pyplot as plt
import matplotlib
import json
import os
import PyQt6

# use pgf to input plots directly in latex
# comment both lines to show plot in a window instead
matplotlib.use("pgf")
plt.rcParams.update({
    "pgf.texsystem": "pdflatex",
    "font.family": "sans-serif",
    "text.usetex": False,
    "pgf.rcfonts": False,
})

plt.figure()

# max years to be shown
t_max = 700  # years
# number of points on x axis (time) to be computed (500 numbers from 0 to t_max)
t = np.linspace(0, t_max, 500)

# load data from json
# use os to get absolute path to the json file
with open(os.path.join(os.path.dirname(__file__), 'lakes.json'), 'r') as file:
    data = json.load(file)

    for lake, values in data.items():
        k = values["outflow"] / values["vol"] # k = Q_out / V
        P = np.exp(-k * t) * 100 # e^(-kt), in percentage
        plt.plot(t, P, label=f"Lake {lake}")

# Add horizontal lines for 50% and 5%
plt.axhline(50, color='blue', linestyle='--', linewidth=1, label=r"50% remaining")
plt.axhline(5, color='red', linestyle='--', linewidth=1, label=r"5% remaining")

plt.xlabel("Time (years)")
plt.ylabel("Pollution Concentration (% of initial)")
plt.legend()
plt.grid(True)
plt.tight_layout()

# show plot
# plt.show()

# save as pgf
plt.savefig("assets/pollution_decay.pgf")


