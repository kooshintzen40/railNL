import csv
import math
import random
from critical_connections import check_list
from itertools import chain

class Station:
    def __init__(self, node):
        self.id = node
        self.adjacent = {}

    def __str__(self):
        return str(self.id) + ' is adjacent to: ' + str([x.id for x in self.adjacent])

    def add_neighbor(self, neighbor, distance=0):
        self.adjacent[neighbor] = distance

    def get_connections(self):
        return self.adjacent.keys()

    def get_graph(self):
        return self.adjacent

    def get_id(self):
        return self.id

    def get_distance(self, neighbor):
        return self.adjacent[neighbor]

class Graph:
    def __init__(self):
        self.vert_dict = {}
        self.num_stations = 0

    def __iter__(self):
        return iter(self.vert_dict.values())

    def add_station(self, node):
        self.num_stations = self.num_stations + 1
        if node not in self.vert_dict:
            new_station = Station(node)
            self.vert_dict[node] = new_station
            return new_station
        else:
            return None

    def get_station(self, n):
        if n in self.vert_dict:
            return self.vert_dict[n]
        else:
            return None

    def add_connection(self, frm, to, distance = 0):
        if frm not in self.vert_dict:
            self.add_station(frm)
        if to not in self.vert_dict:
            self.add_station(to)

        self.vert_dict[frm].add_neighbor(self.vert_dict[to], distance)
        self.vert_dict[to].add_neighbor(self.vert_dict[frm], distance)

    def get_stations(self):
        return self.vert_dict.keys()

class Score:
    def __init__(self, p, train, min):
        self.p = p
        self.train = train
        self.min = min

    def get_score(self):
        return self.p*10000 - (self.train*20 + self.min/10)


# for v in g:
#     for w in v.get_connections():
#         vid = v.get_id()
#         wid = w.get_id()
#         print('( %s , %s, %3d)'  % ( vid, wid, v.get_distance(w)))

#
# for v in g:
#     print('g.vert_dict[%s]=%s' %(v.get_id(), g.vert_dict[v.get_id()]))

# dijkstra greedy algorithm
def dijkstra(begin):


    # making new graph
    g = Graph()


    # loading in stations and connections
    with open('ConnectiesHolland.csv', 'r') as csvfile:
        nlreader = csv.reader(csvfile)
        for row in nlreader:
            g.add_station(row[0])
            g.add_station(row[1])
            g.add_connection(row[0], row[1], int(row[2]))



    shortest_distance = {}
    previous = {}
    unvisited_stations = g.vert_dict
    infinity = math.inf
    path = []



    for station in unvisited_stations:
        shortest_distance[station] = infinity
    shortest_distance[begin] = 0

    breaker = False
    while unvisited_stations:
        min_node = None
        for node in unvisited_stations:
            if min_node is None:
                min_node = node
            elif shortest_distance[node] < shortest_distance[min_node]:
                min_node = node


        for neighbor, distance in g.vert_dict[min_node].adjacent.items():

            if distance + shortest_distance[min_node] < shortest_distance[neighbor.id]:
                shortest_distance[neighbor.id] = distance + shortest_distance[min_node]
                previous[neighbor.id] = min_node
                goal = previous[neighbor.id]

            if shortest_distance[neighbor.id] > 120:
                shortest_distance.pop(neighbor.id)
                #previous.pop(neighbor.id)
                #print(neighbor.id)
                #print(previous)
                goal = previous[neighbor.id]
                breaker = True
                break



        if breaker:
            break
        #print(g.vert_dict)
        unvisited_stations.pop(min_node)


    current = goal
    while current != begin:

        try:
            connection = []
            connection.insert(0, current)
            current = previous[current]
            connection.insert(0, current)
            path.insert(0, connection)

        except KeyError:
            print("path not reachable")
            break


    if shortest_distance[goal] != infinity:
        print("shortest distance is " + str(shortest_distance[goal]))
        print("the path is" + str(path))
    # else:

    # make p for score function

    # append to p_path to get p
    p_path.append(path)


    # make list of minutes per trajectory
    minutes.append(shortest_distance[goal])



# calling of dijkstra algorithm

list_stations = []
with open('C:/Users/Koos Hintzen/Documents/GitHub/railNL/railNL/Data/StationsHolland.csv', 'r') as stationsfile:
    stationreader = csv.reader(stationsfile)
    for row in stationreader:
        list_stations.append(row[0])

p_path = []
minutes = []
score_list = []
#print(check_list)



dijkstra('Den Helder')

for j in range(1):
    for i in range(5):
        dijkstra(random.choice(list_stations))
    print(j)
    p_list = list(chain.from_iterable(p_path))
    path_set = set(map(tuple, p_list))
    check_set = set(map(tuple, check_list))
    p_dif = path_set.symmetric_difference(check_set)
    p = (len(check_list) - len(p_dif))/len(check_list)
    print(p)
    score = Score( p, 5, sum(minutes))
    score_list.append(score.get_score())

archive_file = open('archivefile.csv', 'a')

print(max(score_list))

print("DONE")
