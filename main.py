# ----------------------------------------------------------
# Simulation of a metro network to find the shortest 
# path between two nodes
#
# (C) 2022 Claudio Campuzano, Quilpue, Chile
# Released under GNU Public License (GPL)
# email claudio.capuzano.b@gmail.com
# ----------------------------------------------------------

import json
from collections import defaultdict
from math import inf
import copy

class subwayNetwork():
    def __init__(self, fileNetwork):
        """Initialization of metro network 
        
        The different storage structures are initialized,
        and then the different networks are loaded.
        
        Args:
            fileNetwork (str): Path to topology file
        
        Return:
            no value
        """
        
        self._networkWhite = defaultdict(set)
        self._networkRed = defaultdict(set)
        self._networkGreen = defaultdict(set)
        self.generateNetwork(fileNetwork)
    
    def generateNetwork(self, fileNetwork):
        """Generation of the three types networks.
        
        Based on the topology file, which includes the structure, 
        and the special stations, network is loaded into the script
        
        Args:
            fileNetwork (str): Path to topology file

        Return:
            no value
        """
        
        try:
            with open(fileNetwork, 'r') as jsonFile:
                networkTopololy = json.load(jsonFile)
                jsonFile.close()
                
            for initialStation,adjacentStations in networkTopololy['adjacentStations'].items():
                setAdjacentStations = set(adjacentStations.strip().split(','))
                self._networkWhite[initialStation] = setAdjacentStations

            self._networkRed = self.__generateCustomNetwork(networkTopololy['greenStation'])
            self._networkGreen = self.__generateCustomNetwork(networkTopololy['redStation'])
                    
        except Exception as e:
            print('Error when generating the network: ',e)
            return('Error')

    def __generateCustomNetwork(self, specialStations):
        """Customized network generation.
        
        Using the common white network as a basis, special red 
        and green networks are generated.
        
        Args:
            specialStations (str): Special stations (red or green) 
                                   separated by commas

        Return:
            networkCopy (set): Custom network
        """
        
        networkCopy = copy.deepcopy(self._networkWhite)
        for specialStation in specialStations.strip().split(','):
            newInterconnections = set()
            for station in networkCopy[specialStation]:
                networkCopy[station].remove(specialStation)
                newInterconnections.add(station)
            del networkCopy[specialStation]    

            for newInterconnection in newInterconnections:
                networkCopy[newInterconnection].update(newInterconnections-set(newInterconnection))
        return networkCopy
            
    def findShortestPath(self, initialStation, endStation, trainColor):
        """Shortest route calculation between two stations.
        
        Implementation of BSF algorithm for shortest path finding
        for unweighted networks.
        
        Args:
            initialStation (str): Initial station to simulate
            endStation (str): End station to simulate
            trainColor (str): color of the train to simulate
        
        Return:
            str: Search result
        """
                
        if trainColor != "" and trainColor not in ['green','red']: 
            return('Wrong train color, available green and red')
            
                
        if trainColor == 'green': networkUse = self._networkGreen
        elif trainColor == 'red': networkUse = self._networkRed
        else: networkUse = self._networkWhite
        
        if len(networkUse) == 0: return('Empty path, apparently the topology file was not loaded')
            
        if not all (station in networkUse.keys() for station in (initialStation,endStation)): 
            return('Out-of-route stations, check network topology')
            
        
        if initialStation == endStation: return("Station starts and ends the same")
            
        explored = []
        queue = [[initialStation]]
        while queue:
            path = queue.pop(0)
            station = path[-1]
         
            if station not in explored:
                adjacentStations = list(networkUse[station])

                for adjacentStation in adjacentStations:
                    new_path = list(path)
                    new_path.append(adjacentStation)
                    queue.append(new_path)
                    
                    if adjacentStation == endStation:
                        path = '->'.join([str(path) for path in new_path])
                        return("Shortest path = "+ path)
                        
                explored.append(station)
        return("Connecting path doesn't exist")
        

if __name__ == '__main__':
    var = subwayNetwork('')

    initialStation = input('Enter initial station: ')
    endStation = input('Enter end station: ')
    trainColor = input('Enter train color (red, green or press enter to skip): ')

    print(var.findShortestPath(initialStation,endStation,trainColor))
