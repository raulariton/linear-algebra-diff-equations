import math

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

# # Start LaTeX table
# latex_table = """
# \\begin{tabular}{|c|c|}\n
# \\hline\n
# Lake & Time (in years) to ``drain'' \\\\\n
# \\hline\n
# """

# for lake, values in data.items():
#     result = values["vol"] / values["outflow"]
#     latex_table += f"{lake} & {result:.2f} \\\\\n"
#     # add hline after each row
#     latex_table += "\\hline\n"

# latex_table += "\\end{tabular}"

# Start LaTeX table
latex_table = """
\\begin{tabular}{|c|c|}\n
\\hline\n
Lake & Time (in years) to reduce pollution to 50\% \\\\\n
\\hline\n
"""

for lake, values in data.items():
    result = - (values["vol"] / values["outflow"]) * (math.log(0.05))
    latex_table += f"{lake} & {result:.2f} \\\\\n"
    # add hline after each row
    latex_table += "\\hline\n"

latex_table += "\\end{tabular}"

print(latex_table)
