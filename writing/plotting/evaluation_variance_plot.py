#!/usr/bin/python3

import mysql.connector
import datetime
import matplotlib.dates as mdates
import matplotlib.pyplot as plt
import numpy as np
import matplotlib as mpl
import sys

if len(sys.argv) < 2:
    print("Specify a runid as argument")
    exit(1)

run_id = sys.argv[1]

mpl.rcParams.update({

        "text.usetex": True,
    "font.family": "serif",
    "font.serif": ["Computer Modern Roman"],
    "font.size": 20,  
    "axes.labelsize": 25,
    "axes.titlesize": 35,
    "xtick.labelsize": 20,
    "ytick.labelsize": 20,
    "legend.fontsize": 21,
})




runs_postfix = ["ant_colony", "evolutionary", "simulated_annealing", "kubernetes_default"]
runs = [f"k8_simulation_{run_id}_{postfix}" for postfix in runs_postfix]

results = []
for i, run in enumerate(runs):
    mydb = mysql.connector.connect(
        host="127.0.0.1",
        user="root",
        password="root",
        database=run
    )

    mycursor = mydb.cursor()

    mycursor.execute(f"SELECT evaluation as {runs_postfix[i]}, time FROM evaluation")
    results.append(mycursor.fetchall())

averages = []
variances = []
for i, run in enumerate(results):
    evaluations = [x[0] for x in run]

    averages.append(np.mean(evaluations))
    variances.append(np.var(evaluations))

print("Averages:", dict(zip(runs_postfix, averages)))

print("Variances:", dict(zip(runs_postfix, variances)))
print("\\begin{tabular}{l|r|r}")
# print("\\hline")
print("Algorithm & Average & Variance\\\\")
print("\\hline")
for i, postfix in enumerate(runs_postfix):
    print(f"{postfix.replace('_', '\\_')} & {averages[i]:.2f} & {variances[i]:.2f}\\\\")
# print("\\hline")
print("\\end{tabular}")
# Get default color cycle from matplotlib
color_cycle = plt.rcParams['axes.prop_cycle'].by_key()['color']
# Plotting boxplot
fig, ax = plt.subplots()

data = [np.array([x[0] for x in run]) for run in results]
box = ax.boxplot(data, labels=runs_postfix, patch_artist=True)

# Apply matching default matplotlib colors
for patch, color in zip(box['boxes'], color_cycle[:len(runs_postfix)]):
    patch.set_facecolor(color)

for line in box['medians']:
    line.set_color('black')

plt.xlabel('Algorithm')
plt.ylabel('Evaluation')
plt.title('Evaluation Boxplot for Different Algorithms')
plt.gcf().set_size_inches(14, 5)

plt.grid(True)

plt.savefig(f"boxplot_evaluation_{run_id}.pdf", bbox_inches='tight', dpi=300)
# plt.show()

