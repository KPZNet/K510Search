# coding=utf-8

from __future__ import print_function
from simpleai.search import SearchProblem, astar
import json
from datetime import datetime

GOAL = 'pitt'

def extract_time(datetimestring):
    dti = datetime.strptime(datetimestring, '%Y-%m-%d %H:%M')
    return dti

def read_schedule():
    with open("bus_stops.json", "r") as rf:
        decoded_data = json.load(rf)
        return decoded_data

def init_bus_schedule():
    dc = read_schedule()
    bspts = []
    for busstop in dc['busstops']:
        bs = BusStop(busstop)
        bspts.append(bs)
    return bspts

class BusTrip():
    def __init__(self, stop):
        self.destination = stop['destination']
        self.departuretime = extract_time(stop['departuretime'])
        self.arrivaltime = extract_time(stop['arrivaltime'])
        self.triptime = (self.arrivaltime - self.departuretime).total_seconds() / 60
        self.distance = stop['distance']

class BusStop():
    def __init__(self, busstop):
        self.name = busstop['name']
        self.distance = busstop['distance']
        self.trips = []
        for stop in busstop['stops']:
            s = BusTrip(stop)
            self.trips.append(s)


class HelloProblem(SearchProblem):

    def __init__(self, busstops):
        self.bs = busstops

        super(HelloProblem, self).__init__(initial_state='brentwood')

    def actions(self, state):
        bs = next(x for x in self.bs if x.name == state)
        return bs.trips

    def result(self, state, action):
        bs = next(x for x in self.bs if x.name == state)
        res = []
        return action.destination


    def is_goal(self, state):
        bs = next(x for x in self.bs if x.name == state)
        return state == GOAL

    def heuristic(self, state):

        bs = next(x for x in self.bs if x.name == state)
        distance = bs.distance
        return distance




bspts = init_bus_schedule()

problem = HelloProblem(busstops=bspts)
result = astar(problem)

print(result.state)
route = []
for s in result.path():
    route.append(s[1])
print(route)
