
import textdistance
import numpy as np



def batch(orig_order_ids, orig_aisles, orig_shelves_list):

    aisles = sorted(orig_aisles, key = orig_aisles.count, 
                                    reverse = True) 
    length = len(aisles)

    indexes = []
    indexes_done = []
    for i in range(0,length):
        for j in range(0,length):
            if aisles[i] == orig_aisles[j] and j not in indexes_done:
                indexes.append(j)
                indexes_done.append(j)
    print("******indexes****",indexes)
    order_ids = []
    shelves_list = []
    leven_matrix = np.zeros((length,length),dtype=int)                            #initialise an empty matrix 

    for ind in indexes:
        order_ids.append(orig_order_ids[ind])
        shelves_list.append(orig_shelves_list[ind])
    print("****sorted***")
    print(aisles)
    print(order_ids)
    print(shelves_list)
    
    
    leven_matrix = np.zeros((length,length),dtype=int)                            #initialise an empty matrix 


    def invalidate(start,id,col):               #once aisles of user are processed, mark them as 999 so that they won't be 
        if col:                                 #considered for further batches 
            for i in range(start,length):
                leven_matrix[id][i] = 999
            for j in range(0,length):
                leven_matrix[j][id] = 999
        else:                                   #we don't want to overwrite the current index column.
            for i in range(start,length):
                leven_matrix[id][i] = 999


    for i in range(0,length):                   #mark the diagnoals 999
        for j in range(0,length):
            if i == j:
                leven_matrix[i][j] = 999

    n = 3
    done = []                                   #list of processed elements
    batches = []                                #list of aisles in group of n
    order_batches = []                          #list of orders in group of n
    shelves_batches = []                        #list of shelves corresponding to n order_ids
    for i in range(0,length):
        if i not in done and length-len(done)>=n:
            current = aisles[i]
            col = []
            top_n = []
            order_n = []
            shelves_n = []

            for j in range(0,length):
                if i == j:
                    col.append(leven_matrix[i][j])
                else:
                    if j not in done:
                        dst = textdistance.levenshtein(current,aisles[j])
                        leven_matrix[j][i] = dst
                        col.append(dst)
                    else:
                        col.append(leven_matrix[j][i])      #999              
                    
            sorted_list = sorted(range(len(col)), key=lambda k: col[k])    #sort the column values and get indexes of sorted values.
            top_indexes = sorted_list[:n-1]                                #select top n-1 indexes  
            
            top_n.append(current)
            order_n.append(order_ids[i])
            shelves_n.append(shelves_list[i])
        
            for id in top_indexes:
                done.append(id)                    #mark it as "processed"
                invalidate(i+1,id,True)
                top_n.append(aisles[id])
                order_n.append(order_ids[id])
                shelves_n.append(shelves_list[id])
                
                
            if i not in done: done.append(i)
            invalidate(i+1,i,False)

            batches.append(top_n)
            order_batches.append(order_n)
            shelves_batches.append(shelves_n)

    left_aisles = []
    left_orders = []
    left_shelves = []
    print("\n Final matrix values: \n")

    print(leven_matrix)            #print final matrix

    for i in range(0,length):
        '''
        as batches of three, if the total number of orders received are not a multiple of n,
        orders will be left, add it to "left_aisles" and left_orders
        '''
        if i not in done:           
            left_aisles.append(aisles[i])
            left_orders.append(order_ids[i])
            left_shelves.append(shelves_list[i])

    if len(left_aisles) != 0:
        batches.append(left_aisles)
        order_batches.append(left_orders)
        shelves_batches.append(left_shelves)


    print("\nAisles grouped together:\n",batches)                 #final batches
    print("\nOrder ids grouped together:\n",order_batches)           #orders batches 
    print("\nShelves grouped together:\n",shelves_batches)         #shelves batches
    return batches, order_batches, shelves_batches


'''
Output:

(base) F:\WalKet-Basket\Part2>python lavenstein.py

 Final matrix values:

[[999. 999. 999. 999. 999. 999.]
 [  3. 999. 999. 999. 999. 999.]
 [  3. 999. 999. 999. 999. 999.]
 [  4. 999. 999. 999. 999. 999.]
 [  3. 999. 999.   3. 999. 999.]
 [  3. 999. 999.   3. 999. 999.]]

Aisles grouped together:
 [['RGCD', 'ACB', 'RSBA'], ['CRM', 'PG', 'PG']]

Order ids grouped together:
 [['5269129170', '4269129163', '3269129163'], ['6269129163', '7269129163', '8269129155']]

Shelves grouped together:
 [[['R1', 'G1', 'C1', 'D1', 'D2'], ['A1', 'C3', 'B1'], ['R1', 'S1', 'BG1', 'FA1']], [['C3', 'R1', 'M1', 'M2'], ['P1', 'P3', 'P4', 'G6', 'G7'], ['P3', 'P4', 'G6', 'G7']]]
'''
