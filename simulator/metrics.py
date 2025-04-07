import Time as time
import mysql.connector

database_connection=None
database_cursor=None
name=None

record_metrics=True
def update_metric(metric, value):
    """
    Update metrics with new values.
    """
    global record_metrics
    if not record_metrics: return
    global database_connection
    global database_cursor
    database_cursor.execute(f"INSERT INTO {metric} (time, {metric}) VALUES (\"{time.current_time().strftime('%Y-%m-%d %H:%M:%S')}\", {value});")
    # print(f"updated {metric} with {value}")
    database_connection.commit()

def create_metric(metric):
    """
    Create a new metric with the given id.
    """
    global record_metrics
    if not record_metrics: return
    global database_connection
    global database_cursor
    database_cursor.execute(f"CREATE TABLE {metric} (time DATETIME NOT NULL, {metric} FLOAT);")
    database_connection.commit()
     

def initialize(algorithm_name: str, run: int):
    global record_metrics
    if not record_metrics: return    
    global name
    name = f"k8_simulation_{run}_{algorithm_name}"    
    print(name)
    mydb = mysql.connector.connect(
        host="127.0.0.1",
        user="root",
        password="root",

    )
    mycursor = mydb.cursor(buffered=True)
    mycursor.execute(f"CREATE DATABASE {name}")


    global database_connection
    global database_cursor

    database_connection = mysql.connector.connect(
        host="127.0.0.1",
        user="root",
        password="root",
        database=name
    )
    database_cursor = database_connection.cursor()
