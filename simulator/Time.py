"""
This file is designed to simulate time
"""

from datetime import datetime, timedelta


saved_state=None
simulated_time = datetime(2020, 1, 1, 00, 00, 00)
time_step = 0


def increment_time():
    """
    incrementing will automattimestepically increment by 15 mintutes
    """
    global simulated_time 
    global time_step
    simulated_time += timedelta(minutes=1)
    time_step += 1

def current_time() -> datetime:
    """
    returns the current time as a datetime
    """
    return simulated_time

def current_time_step() -> int:
    """
    returns the current timestep as an integer
    """
    return time_step

def timestep_to_time(timestep) -> datetime:
    """
    converts an integer timestep into a python time object
    """
    return datetime(2020, 1, 1, 00, 00, 00) + timedelta(minutes=timestep*1)

def time_to_timestep(time) -> int:
    """
    converts time object into an integer timestep
    """
    return int((time - Configurations.start_time).total_seconds() / 60 /15)

def sql_time(time_obj):
    """
    converts a time object into valid sql time
    """
    return time_obj.strftime("%Y-%m-%d %H:%M:%S")

def reset_time():
    """
    resets the time to the starting time given in the simulation and the timestep to 0
    """
    global simulated_time
    global time_step
    simulated_time = Configurations.start_time
    time_step = 0