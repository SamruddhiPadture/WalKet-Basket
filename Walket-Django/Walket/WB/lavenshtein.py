
import textdistance
import numpy as np



def batch(order_to_products_mapping, order_ids, aisles, shelves_list):
    length = len(aisles)
    leven_matrix = np.zeros((length,length))                            #initialise an empty matrix 


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


    done = []                                   #list of processed elements
    batches = []                                #list of aisles in group of 3
    order_batches = []                          #list of orders in group of 3
    shelves_batches = []                        #list of shelves corresponding to 3 order_ids
    for i in range(0,length):
        if i not in done and len(batches)!=3:
            current = aisles[i]
            col = []
            top3 = []
            order_3 = []
            shelves_3 = []

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
            
            id1,id2 = sorted_list[:2]           #get top 2 indexes
            done.append(id1)                    #mark it as "processed"
            invalidate(i+1,id1,True)            #mark row and column values to 999
            done.append(id2)                    
            invalidate(i+1,id2,True)
            
            top3.append(current)
            top3.append(aisles[id1])
            top3.append(aisles[id2])

            order_3.append(order_ids[i])
            order_3.append(order_ids[id1])
            order_3.append(order_ids[id2])

            shelves_3.append(shelves_list[i])
            shelves_3.append(shelves_list[id1])
            shelves_3.append(shelves_list[id2])

            if i not in done: done.append(i)
            invalidate(i+1,i,False)

            batches.append(top3)
            order_batches.append(order_3)
            shelves_batches.append(shelves_3)

    left_aisles = []
    left_orders = []
    left_shelves = []
    print("\n Final matrix values: \n")

    print(leven_matrix)            #print final matrix

    for i in range(0,length):
        '''
        as batches of three, if the total number of orders received are not a multiple of three,
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
