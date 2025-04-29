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


    mycursor.execute(f"SELECT pods_online as {runs_postfix[i]}, time FROM pods_online")
    results.append(mycursor.fetchall())

# calculate and print total up minutes per algorithm
print("\\begin{tabular}{l|c}")
print(" Algorithm & Total Uptime (min) \\\\")
print("\\hline")
for i, run in enumerate(runs):
    total_uptime = 0
    for value, _ in results[i]:
        total_uptime += value
    print(f"{runs_postfix[i].replace('_', '\\_')} & {total_uptime} \\\\")
print("\\end{tabular}")


