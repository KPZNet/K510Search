# coding=utf-8

from __future__ import print_function
from simpleai.search import SearchProblem, astar
from simpleai.search.viewers import WebViewer
import json
from datetime import datetime
from bus_schedules import bus_sch

GOAL = 'pitt'

def extract_time(datetimestring):
    dti = datetime.strptime(datetimestring, '%Y-%m-%d %H:%M')
    return dti

def read_schedule():
    decoded_data = bus_sch
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
        self.linedistance = busstop['linedistance']
        self.trips = []
        for stop in busstop['stops']:
            s = BusTrip(stop)
            self.trips.append(s)

class BusRoute( SearchProblem ):

    def __init__(self, busstops):
        self.bs = busstops
        super( BusRoute, self ).__init__( initial_state='brentwood' )

    def actions(self, state):
        bst = self.get_node ( state )
        trips = []
        for t in bst.trips:
           trips.append(t.destination)
        print("------------------")
        print("Actions: ", trips)
        return trips

    def result(self, state, action):
        rtn = action
        print("Result: ", rtn)
        return rtn

    def is_goal(self, state):
        g = state == GOAL
        print("\tGOAL: ", g)
        if g:
            print("\n*** GOAL FOUND STOP ***")
        return g

    def cost(self, state1, action, state2):
        sourcenode = self.get_node ( state1 )
        source_to_dest = next(x for x in sourcenode.trips if x.destination == state2)
        cost = source_to_dest.triptime
        print("\tCOST: ", cost)
        return cost

    def get_node(self, node_name) :
        return next ( x for x in self.bs if x.name == node_name )

    def print_node(self, node_name):
        n = self.get_node(node_name)
        s = n.name
        print(s)

    def heuristic(self, state):
        destnode = self.get_node ( state )
        distance = destnode.linedistance
        print("\tHEURISTIC: ", distance)
        return distance

bspts = init_bus_schedule()

problem = BusRoute( busstops=bspts )
result = astar(problem)
#result = astar(problem, viewer=WebViewer())

route = []
g = result.path()
#print("RESULT PATH: ", g)
for s in result.path():
    state = s[1]
    n = problem.get_node(state)
    str = n.name + " --> "
    route.append(str)
route.append(" END")
print("Bus Route Recommended:")
print(route)
