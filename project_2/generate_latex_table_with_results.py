"""
Generate the LaTeX code for the results tables for the Cleaning Up the Great Lakes project.
"""

import math
import json

prefix_code = r"""
\begin{table}[H]
    \centering
    \begin{tabular}{|c|c|}
    \hline
    %HEADER_ROW_1% & %HEADER_ROW_2% \\
    \hline
"""

suffix_code = r"""\end{tabular}
    %IF_CAPTION_TEXT%\caption{%CAPTION_TEXT%}%
\end{table}
"""

def draining_time(attributes):
    V = attributes["vol"]
    Q_out = attributes["outflow"]
    result = V / Q_out
    return result

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

def fill_table_with_results(header_row_1, header_row_2,formula_func, caption_text=None):
    with open(r'lakes.json', 'r') as file:
        lakes = json.load(file)

        # replace placeholders in prefix and suffix
        prefix = prefix_code.replace('%HEADER_ROW_1%', header_row_1)
        prefix = prefix.replace('%HEADER_ROW_2%', header_row_2)
        if caption_text:
            suffix = suffix_code.replace('%IF_CAPTION_TEXT%', '')
            suffix = suffix.replace('%CAPTION_TEXT%', caption_text)
        else:
            suffix = suffix_code.replace(r'%IF_CAPTION_TEXT%\caption{%CAPTION_TEXT%}%', '')

        # compute result using formula_func for each lake
        latex_table = prefix
        for lake, attributes in lakes.items():
            result = formula_func(attributes)
            # for each row, add the lake name and the result rounded to 2 decimals
            latex_table += f"{lake} & {result:.2f} \\\\\n"
            # add hline after each row
            latex_table += "\\hline\n"

        # append suffix
        latex_table += suffix

        return latex_table

if __name__ == "__main__":
    # table 1: "draining" each lake
    table = fill_table_with_results(
        "Lake",
        "Time (in years) to ``drain''",
        draining_time,
        "Time to ``drain'' each of the Great Lakes"
    )

    # table 2: time to reduce pollution to 50%
    # table = fill_table_with_results(
    #     "Lake",
    #     "Time (in years) to reduce pollution to 50\%",
    #     reduction_50_percent,
    #     "Time to reduce pollution to 50\% in each of the Great Lakes"
    # )

    # table 3: time to reduce pollution to 5%
    # table = fill_table_with_results(
    #     "Lake",
    #     "Time (in years) to reduce pollution to 5\%",
    #     reduction_5_percent,
    #     "Time to reduce pollution to 5\% in each of the Great Lakes"
    # )

    print(table)


