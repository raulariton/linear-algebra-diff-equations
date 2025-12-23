import numpy as np
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use("pgf")
plt.rcParams.update({
    "pgf.texsystem": "pdflatex",
    "font.family": "sans-serif",
    "text.usetex": False,
    "pgf.rcfonts": False,
})

data = {
    "Superior": {
        "vol": 2900,
        "outflow": 15
    },
    "Michigan": {
        "vol": 1180,
        "outflow": 38
    },
    "Huron": {
        "vol": 850,
        "outflow": 68
    },
    "Erie": {
        "vol": 116,
        "outflow": 85
    },
    "Ontario": {
        "vol": 393,
        "outflow": 99
    }
}

plt.figure()

t_max = 700  # years
t = np.linspace(0, t_max, 500)

for lake, values in data.items():
    k = values["outflow"] / values["vol"] # k = Q_out / V
    P = np.exp(-k * t) * 100 # e^(-kt), in percentage
    plt.plot(t, P, label=f"Lake {lake}")

# Add horizontal lines for 50% and 5%
plt.axhline(50, color='blue', linestyle='--', linewidth=1, label="50% remaining")
plt.axhline(5, color='red', linestyle='--', linewidth=1, label="5% remaining")

# Plot for P_0 = 3 (example: Lake Superior)
# lake = "Superior"
# values = data[lake]
# k = values["outflow"] / values["vol"]
# P0 = 3
# P = P0 * np.exp(-k * t)
# plt.plot(t, P, '--', label=f"{lake} (P_0=3)")

plt.xlabel("Time (years)")
plt.ylabel("Pollution Concentration (% of initial)")
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.savefig("assets/pollution_decay.pgf")
