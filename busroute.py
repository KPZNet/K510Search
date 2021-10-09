# coding=utf-8

from __future__ import print_function
from simpleai.search import SearchProblem, astar
from simpleai.search.viewers import WebViewer
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
        self.linedistance = busstop['linedistance']
        self.trips = []
        for stop in busstop['stops']:
            s = BusTrip(stop)
            self.trips.append(s)

def get_destination(state) :
    stps = list ( state.split ( "," ) )
    l = len ( stps )
    stp = stps[l-1]
    return stp

class BusRoute( SearchProblem ):

    def __init__(self, busstops):
        self.bs = busstops
        super( BusRoute, self ).__init__( initial_state='brentwood' )

    def actions(self, state):
        stp = get_destination ( state )
        bst = next(x for x in self.bs if x.name == stp)
        trips = []
        for t in bst.trips:
           trips.append(t.destination)
        return trips

    def result(self, state, action):
        #stp = get_destination ( state )
        rtn = state + "," + action
        return rtn

    def is_goal(self, state):
        stp = get_destination ( state )
        return stp == GOAL

    def cost(self, state1, action, state2):
        cost = 0
        stps = list( state2.split(","))
        l = len(stps)
        if l == 1:
            bs = next(x for x in self.bs if x.name == stps[0])
            cost = bs.linedistance
        if l > 1:
            source = stps[l-2]
            dest = stps[l-1]
            sourcenode = next(x for x in self.bs if x.name == source)
            destnode = next(x for x in self.bs if x.name == dest)
            source_to_dest = next(x for x in sourcenode.trips if x.destination == dest)
            cost = source_to_dest.distance
        return cost

    def heuristic(self, state):
        distance = 0
        stps = list( state.split(","))
        l = len(stps)
        if l == 1:
            bs = next(x for x in self.bs if x.name == stps[0])
            distance = bs.linedistance
        if l > 1:
            source = stps[l-2]
            dest = stps[l-1]
            sourcenode = next(x for x in self.bs if x.name == source)
            destnode = next(x for x in self.bs if x.name == dest)
            source_to_dest = next(x for x in sourcenode.trips if x.destination == dest)
            distance = destnode.linedistance

        return distance


bspts = init_bus_schedule()

problem = BusRoute( busstops=bspts )
#result = astar(problem)
result = astar(problem, viewer=WebViewer())


print(result.state)
route = []
g = result.path()
for s in result.path():
    stp = get_destination ( s[1] )
    route.append(stp)
print(route)
