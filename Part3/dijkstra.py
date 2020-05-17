from collections import defaultdict
from math import sqrt
import matplotlib.pyplot as plt
from PIL import Image
from pylab import *

#distance calculation
def distance_between_coords(x1, y1, x2, y2):
    distance = sqrt(((x2 - x1) ** 2) + ((y2 - y1) ** 2))
    return distance

# Labelling the coordinates to use as keys for edge detection
def name_coords(coords):
    
    
    coord_count = 0
    for coord in coords:
        coord_count += 1
        coord.append(coord_count)
    return coords

# Creates a weighted and undirected graph
# Returns named coordinates and their connected edges as a dictonary
def graph(coords):
    coords = name_coords(coords)
    graph = defaultdict(list)
    edges = {}
    
    for current in coords:
        for comparer in coords:
            if comparer == current:
                continue
            else:
                weight = distance_between_coords(current[0], current[1],
                                                 comparer[0], comparer[1])
                graph[current[2]].append(comparer[2])
                edges[current[2], comparer[2]] = weight
    return coords, edges

# Returns a path to all nodes with least weight as a list of names
# from a specific node
def shortest_path(node_list, edges, start):
    neighbor = 0
    unvisited = []
    visited = []
    total_weight = 0
    current_node = start
    for node in node_list:
        if node[2] == start:
            visited.append(start)
        else:
            unvisited.append(node[2])
    while unvisited:
        for index, neighbor in enumerate(unvisited):
            if index == 0:
                current_weight = edges[start, neighbor]
                current_node = neighbor
            elif edges[start, neighbor] < current_weight:
                current_weight = edges[start, neighbor]
                current_node = neighbor
        total_weight += current_weight
        unvisited.remove(current_node)
        visited.append(current_node)
    return visited, total_weight


def main():
    coord_aisles = {"start":[123 , 436],"A1":[460 , 356],"A2":[461 , 318],"A3":[461 , 282],
    "C1":[460 , 230],"C2":[460 , 197],"C3":[460 , 157],"C4":[501 , 159],"C5":[500 , 199],"C6":[502 , 229],
    "R1":[500 , 49],"R2":[502 , 87],"R3":[502 , 119],
    "D1":[360 , 44],"D2":[403 , 44],"M1":[163 , 43],"M2":[206 , 44],"M3":[242 , 43],"M4":[288 , 44],
    "S1":[105 , 73],"B1":[63 , 129],"B2":[64 , 174],"B3":[121 , 129],"B4":[120 , 174],
    "P1":[119 , 400],"P2":[120 , 358],"P3":[120 , 299],"P4":[64 , 300],"P5":[64 , 356],"P6":[62 , 399],"P7":[65 , 257],"P8":[63 , 213],
    "G1":[202 , 236],"G2":[247 , 237],"G3":[290 , 237],"G4":[331 , 237],"G5":[375 , 237],"G7":[419 , 237],"G8":[207 , 276],"G9":[248 , 276],"G10":[289 , 276],
    "F1":[326 , 276],"F2":[375 , 272],"BG1":[162 , 236],"PG1":[161 , 277],"FD1":[411 , 273]}  
    #print("The hard-coded list for pixel positions of the aisles : " , coord_aisles)
    #order=["AB","AB","AD"]
    orders = [[['R1', 'G1', 'C1', 'D1', 'D2'], ['A1', 'C3', 'B1'], ['R1', 'S1', 'BG1', 'FA1']], [['C3', 'R1', 'M1', 'M2'], ['P1', 'P3', 'P4', 'G6', 'G7'], ['P3', 'P4', 'G6', 'G7']]]
    cnt=1
    for i in orders:
      
        order = []
        for j in i:
            for k in range(0,len(j)):
                #print(j[k]) 
                order.append(j[k])
        print("Combined list ",cnt," : ",order)
        #order=["A1","B1","A2","B3","A1","D1"]
    
        unique_list = []
        unique_list.append("start")
        for i in order: 
                
                if i not in unique_list: 
                    unique_list.append(i) 
    
        print("List of unique shelves from the order : ",unique_list)
        coords = []
        for i in unique_list :
            if i in coord_aisles :
                coords.append(coord_aisles[i])
        print("List of coordinates of the unique_list : ",coords) 
    
        dict1 = {}
        i=0
        for key in unique_list:#A dictionary to label the order with simple index values i.e mapping start = 1, A1 = 2.... 
            i= i+1
            dict1[key] = i 

        #print(dict1)
        coords, edges = graph(coords)
        sp,weight = shortest_path(coords, edges, 1)
        shortest_path_taken = []
        

        def get_key(val): 
            for key, value in dict1.items():  
                if val == value: 
                    return key 
        shortest_path_taken = []
        for i in sp :
            #print(i) 
            shortest_path_taken.append(get_key(i))
        print("Batch no : ", cnt)
        print("Path : ", shortest_path_taken)
        print("Cost : ",weight )
        print("------------------------------------------------------------------------")
        cnt+=1
       

        im = array(Image.open("C:/Users/Dhande/Pictures/Map.PNG"))

        # plot the image
        imshow(im)

        # some points
        x=[]
        y=[]
        for i in shortest_path_taken:
            if i in coord_aisles:
                
                x.append(coord_aisles[i][0])
                y.append(coord_aisles[i][1])

        # plot the points with red star-markers
        plot(x,y,'r*')

        # line plot connecting the first two points
        plot(x[:],y[:])

        # add title and show the plot
        title('Path') 
        show() 

       
main()   
'''
Output:

Combined list  1  :  ['R1', 'G1', 'C1', 'D1', 'D2', 'A1', 'C3', 'B1', 'R1', 'S1', 'BG1', 'FA1']
List of unique shelves from the order :  ['start', 'R1', 'G1', 'C1', 'D1', 'D2', 'A1', 'C3', 'B1', 'S1', 'BG1', 'FA1']
List of coordinates of the unique_list :  [[123, 436], [500, 49], [202, 236], [460, 230], [360, 44], [403, 44], [460, 356], [460, 157], [63, 129], [105, 73], [162, 236]]
Batch no :  1
Path :  ['start', 'BG1', 'G1', 'B1', 'A1', 'S1', 'C1', 'C3', 'D1', 'D2', 'R1']
Cost :  3753.9842590212097
------------------------------------------------------------------------
Combined list  2  :  ['C3', 'R1', 'M1', 'M2', 'P1', 'P3', 'P4', 'G6', 'G7', 'P3', 'P4', 'G6', 'G7']
List of unique shelves from the order :  ['start', 'C3', 'R1', 'M1', 'M2', 'P1', 'P3', 'P4', 'G6', 'G7']
List of coordinates of the unique_list :  [[123, 436, 1], [460, 157, 8], [500, 49, 2], [163, 43], [206, 44], [119, 400], [120, 299], [64, 300], [419, 237]]
Batch no :  2
Path :  ['start', 'P1', 'P3', 'P4', 'P4', 'G6', 'M1', 'M2', 'C3']
Cost :  2162.4190261115623

'''
   
  
 
  

  
 
    
    

