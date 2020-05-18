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
    
    #print("cooredsss -- ",coords)
    coord_count = 0
    for coord in coords:
        coord_count += 1
        coord.append(coord_count)
    
    return coords

# Creates a weighted and undirected graph
# Returns named coordinates and their connected edges as a dictonary
def graph(coords):
    #print("coord : ",coords)
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
    #print(coords,edges)
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
            #print("index = ",index) 
            #print("neighbor = ",neighbor)
            #print("Edge = ", edges[start, neighbor]," from ", start, neighbor)
            
            if index == 0:
                current_weight = edges[start, neighbor]
                current_node = neighbor
                #print("current_weight = ",current_weight)
            elif edges[start, neighbor] < current_weight:
                current_weight = edges[start, neighbor]
                current_node = neighbor
                #print("curent node = ",current_node)
                #print("current_weight = ",current_weight)
        #print("current_weight = ",current_weight)
        total_weight += current_weight
        start = current_node
        #print("Total weight = ",total_weight)
       
        unvisited.remove(current_node)
        visited.append(current_node)
    return visited, total_weight 


def main():
      
    #print("The hard-coded list for pixel positions of the aisles : " , coord_aisles)
    #order=["AB","AB","AD"]
    orders = [[['R1', 'G1', 'C1', 'D1', 'D2'], ['A1', 'C3', 'B1'], ['R1', 'S1', 'BG1', 'FA1']], [['C3', 'R1', 'M1', 'M2'], ['P1', 'P3', 'P4', 'G6', 'G7'], ['P3', 'P4', 'G6', 'G7']]]
    #orders = [[['P1' , 'P2', 'PG1' , 'G8'],['G10','F1', 'F2' , 'A3'],['M1','M2','D1','R3','C1']]]
    cnt=1 
    for i in orders:
        
        coord_aisles = {"start":[123 , 436],"A1":[460 , 356],"A2":[461 , 318],"A3":[461 , 282],
        "C1":[460 , 230],"C2":[460 , 197],"C3":[460 , 157],"C4":[501 , 159],"C5":[500 , 199],"C6":[502 , 229],
        "R1":[455 , 49],"R2":[455 , 84],"R3":[455 , 119],
        "D1":[360 , 44],"D2":[403 , 44],"M1":[163 , 43],"M2":[206 , 44],"M3":[242 , 43],"M4":[288 , 44],
        "S1":[105 , 73],"B1":[63 , 129],"B2":[64 , 174],"B3":[121 , 129],"B4":[120 , 174],
        "P1":[119 , 400],"P2":[120 , 358],"P3":[120 , 299],"P4":[64 , 300],"P5":[64 , 356],"P6":[62 , 399],"P7":[65 , 257],"P8":[63 , 213],
        "G1":[202 , 236],"G2":[247 , 237],"G3":[290 , 237],"G4":[331 , 237],"G5":[375 , 237],"G7":[419 , 237],"G8":[207 , 276],"G9":[248 , 276],"G10":[289 , 276],
        "F1":[326 , 276],"F2":[375 , 272],"BG1":[162 , 236],"PG1":[161 , 277],"FD1":[411 , 273]} 
        #print("coord_aisles == ",coord_aisles)  
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
                 
                if i not in unique_list and i in coord_aisles: 
                    unique_list.append(i)
        
                  
    
        print("List of unique shelves from the order : ",unique_list)
        list_coords = []
       
        for i in unique_list :
            if i in coord_aisles :
                list_coords.append(coord_aisles[i])
                #print("list == ",coord_aisles[i])
        print("List of coordinates of the unique_list : ",list_coords)
        
    
        dict1 = {}
        i=0
        for key in unique_list:#A dictionary to label the order with simple index values i.e mapping start = 1, A1 = 2.... 
            i= i+1
            dict1[key] = i 

        print(dict1)
        #print("List ---  ",list_coords)
        coords, edges = graph(list_coords)
        #print("coords == ",coords) 
        
        
        sp,weight = shortest_path(coords, edges, 1)
        shortest_path_taken = []
        print(sp)
        

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
       

        im = array(Image.open("C:/Users/Home/Pictures/Map.PNG"))

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
List of unique shelves from the order :  ['start', 'R1', 'G1', 'C1', 'D1', 'D2', 'A1', 'C3', 'B1', 'S1', 'BG1']
List of coordinates of the unique_list :  [[123, 436], [500, 49], [202, 236], [460, 230], [360, 44], [403, 44], [460, 356], [460, 157], [63, 129], [105, 73], [162, 236]]
{'start': 1, 'R1': 2, 'G1': 3, 'C1': 4, 'D1': 5, 'D2': 6, 'A1': 7, 'C3': 8, 'B1': 9, 'S1': 10, 'BG1': 11}
cooredsss --  [[123, 436], [500, 49], [202, 236], [460, 230], [360, 44], [403, 44], [460, 356], [460, 157], [63, 129], [105, 73], [162, 236]]
Edge =  540.2758554664459  from  1 2
current_weight =  540.2758554664459
Edge =  215.03720608304042  from  1 3
curent node =  3
current_weight =  215.03720608304042
Edge =  394.9746827329569  from  1 4
Edge =  458.0753213173572  from  1 5
Edge =  481.7302149543871  from  1 6
Edge =  346.36541397778154  from  1 7
Edge =  437.50428569329466  from  1 8
Edge =  312.80824797309936  from  1 9
Edge =  363.4460069941614  from  1 10
Edge =  203.7670238286853  from  1 11
curent node =  11
current_weight =  203.7670238286853
current_weight =  203.7670238286853
Total weight =  203.7670238286853
Edge =  540.2758554664459  from  1 2
current_weight =  540.2758554664459
Edge =  215.03720608304042  from  1 3
curent node =  3
current_weight =  215.03720608304042
Edge =  394.9746827329569  from  1 4
Edge =  458.0753213173572  from  1 5
Edge =  481.7302149543871  from  1 6
Edge =  346.36541397778154  from  1 7
Edge =  437.50428569329466  from  1 8
Edge =  312.80824797309936  from  1 9
Edge =  363.4460069941614  from  1 10
current_weight =  215.03720608304042
Total weight =  418.8042299117257
Edge =  540.2758554664459  from  1 2
current_weight =  540.2758554664459
Edge =  394.9746827329569  from  1 4
curent node =  4
current_weight =  394.9746827329569
Edge =  458.0753213173572  from  1 5
Edge =  481.7302149543871  from  1 6
Edge =  346.36541397778154  from  1 7
curent node =  7
current_weight =  346.36541397778154
Edge =  437.50428569329466  from  1 8
Edge =  312.80824797309936  from  1 9
curent node =  9
current_weight =  312.80824797309936
Edge =  363.4460069941614  from  1 10
current_weight =  312.80824797309936
Total weight =  731.612477884825
Edge =  540.2758554664459  from  1 2
current_weight =  540.2758554664459
Edge =  394.9746827329569  from  1 4
curent node =  4
current_weight =  394.9746827329569
Edge =  458.0753213173572  from  1 5
Edge =  481.7302149543871  from  1 6
Edge =  346.36541397778154  from  1 7
curent node =  7
current_weight =  346.36541397778154
Edge =  437.50428569329466  from  1 8
Edge =  363.4460069941614  from  1 10
current_weight =  346.36541397778154
Total weight =  1077.9778918626066
Edge =  540.2758554664459  from  1 2
current_weight =  540.2758554664459
Edge =  394.9746827329569  from  1 4
curent node =  4
current_weight =  394.9746827329569
Edge =  458.0753213173572  from  1 5
Edge =  481.7302149543871  from  1 6
Edge =  437.50428569329466  from  1 8
Edge =  363.4460069941614  from  1 10
curent node =  10
current_weight =  363.4460069941614
current_weight =  363.4460069941614
Total weight =  1441.4238988567681
Edge =  540.2758554664459  from  1 2
current_weight =  540.2758554664459
Edge =  394.9746827329569  from  1 4
curent node =  4
current_weight =  394.9746827329569
Edge =  458.0753213173572  from  1 5
Edge =  481.7302149543871  from  1 6
Edge =  437.50428569329466  from  1 8
current_weight =  394.9746827329569
Total weight =  1836.398581589725
Edge =  540.2758554664459  from  1 2
current_weight =  540.2758554664459
Edge =  458.0753213173572  from  1 5
curent node =  5
current_weight =  458.0753213173572
Edge =  481.7302149543871  from  1 6
Edge =  437.50428569329466  from  1 8
curent node =  8
current_weight =  437.50428569329466
current_weight =  437.50428569329466
Total weight =  2273.9028672830195
Edge =  540.2758554664459  from  1 2
current_weight =  540.2758554664459
Edge =  458.0753213173572  from  1 5
curent node =  5
current_weight =  458.0753213173572
Edge =  481.7302149543871  from  1 6
current_weight =  458.0753213173572
Total weight =  2731.9781886003766
Edge =  540.2758554664459  from  1 2
current_weight =  540.2758554664459
Edge =  481.7302149543871  from  1 6
curent node =  6
current_weight =  481.7302149543871
current_weight =  481.7302149543871
Total weight =  3213.7084035547637
Edge =  540.2758554664459  from  1 2
current_weight =  540.2758554664459
current_weight =  540.2758554664459
Total weight =  3753.9842590212097
[1, 11, 3, 9, 7, 10, 4, 8, 5, 6, 2]
Batch no :  1
Path :  ['start', 'BG1', 'G1', 'B1', 'A1', 'S1', 'C1', 'C3', 'D1', 'D2', 'R1']
Cost :  3753.9842590212097
------------------------------------------------------------------------
Combined list  2  :  ['C3', 'R1', 'M1', 'M2', 'P1', 'P3', 'P4', 'G6', 'G7', 'P3', 'P4', 'G6', 'G7']
List of unique shelves from the order :  ['start', 'C3', 'R1', 'M1', 'M2', 'P1', 'P3', 'P4', 'G7']
List of coordinates of the unique_list :  [[123, 436], [460, 157], [500, 49], [163, 43], [206, 44], [119, 400], [120, 299], [64, 300], [419, 237]]
{'start': 1, 'C3': 2, 'R1': 3, 'M1': 4, 'M2': 5, 'P1': 6, 'P3': 7, 'P4': 8, 'G7': 9}
cooredsss --  [[123, 436], [460, 157], [500, 49], [163, 43], [206, 44], [119, 400], [120, 299], [64, 300], [419, 237]]
Edge =  437.50428569329466  from  1 2
current_weight =  437.50428569329466
Edge =  540.2758554664459  from  1 3
Edge =  395.0303785786607  from  1 4
curent node =  4
current_weight =  395.0303785786607
Edge =  400.6906537467526  from  1 5
Edge =  36.22154055254967  from  1 6
curent node =  6
current_weight =  36.22154055254967
Edge =  137.03284277865654  from  1 7
Edge =  148.24641648282767  from  1 8
Edge =  356.67492202284143  from  1 9
current_weight =  36.22154055254967
Total weight =  36.22154055254967
Edge =  437.50428569329466  from  1 2
current_weight =  437.50428569329466
Edge =  540.2758554664459  from  1 3
Edge =  395.0303785786607  from  1 4
curent node =  4
current_weight =  395.0303785786607
Edge =  400.6906537467526  from  1 5
Edge =  137.03284277865654  from  1 7
curent node =  7
current_weight =  137.03284277865654
Edge =  148.24641648282767  from  1 8
Edge =  356.67492202284143  from  1 9
current_weight =  137.03284277865654
Total weight =  173.2543833312062
Edge =  437.50428569329466  from  1 2
current_weight =  437.50428569329466
Edge =  540.2758554664459  from  1 3
Edge =  395.0303785786607  from  1 4
curent node =  4
current_weight =  395.0303785786607
Edge =  400.6906537467526  from  1 5
Edge =  148.24641648282767  from  1 8
curent node =  8
current_weight =  148.24641648282767
Edge =  356.67492202284143  from  1 9
current_weight =  148.24641648282767
Total weight =  321.5007998140339
Edge =  437.50428569329466  from  1 2
current_weight =  437.50428569329466
Edge =  540.2758554664459  from  1 3
Edge =  395.0303785786607  from  1 4
curent node =  4
current_weight =  395.0303785786607
Edge =  400.6906537467526  from  1 5
Edge =  356.67492202284143  from  1 9
curent node =  9
current_weight =  356.67492202284143
current_weight =  356.67492202284143
Total weight =  678.1757218368753
Edge =  437.50428569329466  from  1 2
current_weight =  437.50428569329466
Edge =  540.2758554664459  from  1 3
Edge =  395.0303785786607  from  1 4
curent node =  4
current_weight =  395.0303785786607
Edge =  400.6906537467526  from  1 5
current_weight =  395.0303785786607
Total weight =  1073.206100415536
Edge =  437.50428569329466  from  1 2
current_weight =  437.50428569329466
Edge =  540.2758554664459  from  1 3
Edge =  400.6906537467526  from  1 5
curent node =  5
current_weight =  400.6906537467526
current_weight =  400.6906537467526
Total weight =  1473.8967541622885
Edge =  437.50428569329466  from  1 2
current_weight =  437.50428569329466
Edge =  540.2758554664459  from  1 3
current_weight =  437.50428569329466
Total weight =  1911.4010398555831
Edge =  540.2758554664459  from  1 3
current_weight =  540.2758554664459
current_weight =  540.2758554664459
Total weight =  2451.676895322029
[1, 6, 7, 8, 9, 4, 5, 2, 3]
Batch no :  2
Path :  ['start', 'P1', 'P3', 'P4', 'G7', 'M1', 'M2', 'C3', 'R1']
Cost :  2451.676895322029
------------------------------------------------------------------------
'''
























































































































































































































































































































































































































































































































