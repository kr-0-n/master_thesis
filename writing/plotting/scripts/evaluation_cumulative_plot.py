#!/usr/bin/python3
import mysql.connector
import datetime
import matplotlib.dates as mdates
import matplotlib.pyplot as plt
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

fig = plt.figure()
ax = plt.subplot(111)

for i, run in enumerate(results):
    cumulative_evaluation = [sum(x[0] for x in run[:j+1]) for j in range(len(run))]
    ax.plot([x[1] for x in run], cumulative_evaluation, label=runs_postfix[i], linewidth=0.8, marker='o', markersize=2)


plt.xlim([datetime.date(2020, 1, 1), datetime.date(2020, 1, 2)])  # Adjust the range as needed

plt.grid(True)
plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%H:%M'))


plt.xlabel('Time')
plt.ylabel('Cumulative Evaluation')
plt.gcf().set_size_inches(14, 5)

box = ax.get_position()
ax.set_position([box.x0, box.y0 + box.height * 0.2,
                 box.width, box.height * 0.9])

ax.legend(loc='upper center', bbox_to_anchor=(0.5, -0.2),
          fancybox=True, shadow=False, ncol=5)

plt.savefig(f"../plots/cumulative_evaluation_over_time_{run_id}_no_title.pdf", bbox_inches='tight')
# plt.show()

