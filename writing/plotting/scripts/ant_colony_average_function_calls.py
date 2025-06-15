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

mydb = mysql.connector.connect(
    host="127.0.0.1",
    user="root",
    password="root",
    database=f"k8_simulation_{run_id}_ant_colony"
)

mycursor = mydb.cursor()
mycursor.execute(f"SELECT num_eval_func_calls as k8_simulation_{run_id}_ant_colony, time FROM num_eval_func_calls")
results = mycursor.fetchall()
print(sum([x[0] for x in results]) / len(results))
