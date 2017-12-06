graph = {'A': ['B', 'C', 'E'],
         'B': ['A','D', 'E'],
         'C': ['A', 'F', 'G'],
         'D': ['B'],
         'E': ['A', 'B','D'],
         'F': ['C'],
         'G': ['C']}
from collections import deque

def connect(graph,start):
    explored=[] #to keep track of the explored options
    q=deque(start)   #queue

    while q:
        node=q.popleft()
        if node not in explored:
            explored.append(node)
            neighbours=graph[node]

            for n in neighbours:
                q.append(n)

    return explored

def shortest_path(graph,start,end):
    explored=[]
    q=[[start]] #to store the paths
    if start==end:
        return 'Start =Goal'

    while q:
        path=q.pop(0)
        node=path[-1]#for the last node
        if node not in explored:
            neighbours=graph[node]

            for n in neighbours:
                new_path=list(path)
                new_path.append(n)
                q.append(new_path)
                if neighbour==end :
                    return new_path

            explored.append(node)

        return 'No path'  #if no path possible

          
