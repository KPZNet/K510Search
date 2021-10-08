# coding=utf-8

from __future__ import print_function
from simpleai.search import SearchProblem, astar
import json
from datetime import datetime

GOAL = 'HELLO WORLD'

def extract_time(datetimestring):
    dti = datetime.strptime(datetimestring, '%Y-%m-%d %H:%M')
    return dti

class BusTrip():
    def __init__(self, stop):
        self.name = stop['name']
        self.destination = stop['destination']
        self.departuretime = extract_time(stop['departuretime'])
        self.arrivaltime = extract_time(stop['arrivaltime'])
        self.triptime = (self.arrivaltime - self.departuretime).total_seconds() / 60

class BusStop():
    def __init__(self, stops):
        self.trips = []
        for stop in stops:
            s = BusTrip(stop)
            self.trips.append(s)



class HelloProblem(SearchProblem):

    def actions(self, state):
        if len(state) < len(GOAL):
            return list(' ABCDEFGHIJKLMNOPQRSTUVWXYZ')
        else:
            return []

    def result(self, state, action):
        return state + action

    def is_goal(self, state):
        return state == GOAL

    def heuristic(self, state):
        # how far are we from the goal?
        wrong = sum([1 if state[i] != GOAL[i] else 0
                    for i in range(len(state))])
        missing = len(GOAL) - len(state)
        return wrong + missing


def read_schedule():
    with open("bus_stops.json", "r") as rf:
        decoded_data = json.load(rf)
        return decoded_data


dc = read_schedule()

stops = dc['stop']

dtm = BusStop(stops)





problem = HelloProblem(initial_state='')
result = astar(problem)

print(result.state)
print(result.path())
