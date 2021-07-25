from collections import deque
import copy

class Node:
    def __init__(self, i, j):
        self.__score = 0
        self.__type = ""
        self.__name = "node_" + str(i) + "_" + str(j)

    
    def getName(self):
        return self.__name


    def getScore(self):
        return self.__score
    
    def setScore(self,value):
        if type(value) != int:
            raise TypeError("The score must be of type <int>")
        
        self.__score = value


    def getType(self):
        return self.__type

    def setType(self, value):
        if type(value) != str:
            raise TypeError("The score must be of type <str>")
        #the possible values that type can accept are "match", "mismatch","gap_s1","gap_s2"
        self.__type = value


    def __str__(self):
        return str(self.__name)



class Graph:
    def __init__(self):
        self.__nodes = dict()
        #self.__lastNode = Node(0,0)

    def getLastNode(self):
        return self.__lastNode

    def insertNode(self, node):
        if type(node) != Node:
            raise TypeError("the node to be inserted must be of type <Node>")
        
        if node not in self.__nodes:
            self.__nodes[node] = dict()

    def insertEdge(self, fromNode, toNode, weight = 0):
        self.insertNode(fromNode)
        self.insertNode(toNode)
        self.__nodes[fromNode][toNode] = weight


    def getAllNodes(self):
        return self.__nodes.keys()
    
    def nodeIterator(self):
        for n in self.__nodes:
            yield n
    
    def edgeIterator(self):
        for n in self.__nodes:
            for e in self.__nodes[n]:
                yield (n,e,self.__nodes[n][e])
    
    def adjacentNodes(self, node):
        if node in self.__nodes.keys():
            return self.__nodes[node]
    

    def BFS(self, node):

        """
        This is the function that returns all the possible paths starting from 
        a specific node until the last node of the graph
        """

        Q = deque()
        paths = []
        Q.append([node])

        while len(Q) > 0:
            
            currentPath = Q.popleft()
            lastNodeInPath = currentPath[-1]

            if self.adjacentNodes(lastNodeInPath) == {}:
                paths.append(currentPath)   

            else:
                for node in self.adjacentNodes(lastNodeInPath):
                    
                    tmpPath = copy.deepcopy(currentPath)
                    tmpPath.append(node)
                    Q.append(tmpPath)       
        
        #for path in paths:
        #    print([x.getName() for x in path])
        
        return paths
    
    def DFS(self,root):

        """
        This is a DFS function that breaks once it finds the last node of the graph
        """

        #paths = []
        S = deque()
        S.append(root)
        visited = set()

        while len(S) > 0:
            node = S.pop()
            if node not in visited:
                print("visiting {}".format(node))
                visited.add(node)
                for n in self.adjacentNodes(node):
                    S.append(n)

                """if self.adjacentNodes(node) == {}:
                    self.__lastNode = node
                    return self.getLastNode()
                else:
                    for n in self.adjacentNodes(node):
                        S.append(n)"""
    
        

    def __str__(self):
        #out_str = "Nodes:\n" + ",".join(self.__nodes)
        #out_str += "\nEdges:\n"

        out_str = ""

        for n in self.__nodes:
            for v in self.__nodes[n]:
                out_str += "{} (type: {}) ----> {} (type: {})\n".format(n,n.getType(),v,v.getType())
            if len(self.__nodes[n]) == 0:
                out_str += "{} (type: {})\n".format(n, n.getType())
        
        return out_str

if __name__ == "__main__":
    n1 = Node(1,1)
    n2 = Node(2,2)
    n3 = Node(3,3)
    n4 = Node(4,4)
    n5 = Node(5,5)

    g = Graph()
    g.insertEdge(n1,n2)
    g.insertEdge(n2,n3)
    g.insertEdge(n2,n4)
    g.insertEdge(n4,n5)
    g.insertEdge(n3,n5)
    
    print(g)
    #print(g.adjacentNodes(n3))
    g.BFS2(n1)
    #g.DFS(n1)