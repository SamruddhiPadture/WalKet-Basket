import json
import csv

def generate(filenames):
    base_dir = "F:\\Walket-Django\\Walket\\media\\"
    orderList = []   #list of all order numbers due to multiple files
    aisleList = []   #list of all aisle strings of multiple user--to be used for levenstein
    shelfList = []   #list of all shelves
    data = {}       #mapping of orderNo and its ProductIds

    #apply looping for multiple inputs after this only otherwise orderList and aisleList will get reset everytime.
    fileList = []

    for i in range(0,len(filenames)):
        fileList.append(base_dir+filenames[i])

    # fileList=['Desktop/ord1.json','Desktop/ord2.json','Desktop/ord3.json']
    #fileList=["Desktop/ord4.json"]
    #with open("Desktop/ord1.json", "r") as read_file:
    for j in range(0,len(fileList)):
        with open(fileList[j],"r") as read_file:
            jsonInput = json.load(read_file)                    #read json input file
            #print(jsonInput)

            orderList.append(jsonInput['orderNo'])
            # print("List of all ordernumbers from multiple json inputs till now:")
            # print(orderList)

            productList=[]                                      #list of productIds for one user
            
            for i in jsonInput['products']:
                productList.append(i['productId'])

            data[jsonInput['orderNo']]=productList
            # print("Dictionary of ordernum mapped to list of products")
            # print(data)

            with open('F:\\Walket-Django\\Walket\\WB\\products.csv', 'r') as file:      #read csv file
                reader = csv.reader(file)
                aisle = []
                shelf = []
                for i in range(0,len(productList)):
                    for row in reader:
                        if row[0]==productList[i]:
                            aisle.append(row[2])
                            shelf.append(row[3])
                            break
                shelfList.append(shelf)
                aisle = list(dict.fromkeys(aisle))
                aisleList.append(''.join(aisle))
                
    print("\nOrder to products mapping:\n",data)
    print("\nList of orders:\n",orderList)
    print("\nList of aisles:\n",aisleList)
    print("\nList of shelves:\n",shelfList)

    return data, orderList, aisleList, shelfList



'''
output
(base) F:\WalKet-Basket\Part1>python generateAisles.py

Order to products mapping:
 {'5269129170': ['PR12ERT45', 'PR45GHT98', 'PR04DEF04', 'PR13JKL13', 'PR14JKL14'], '4269129163': ['PR01ABC01', 'PR06DEF06', 'PR22STU22'], '3269129163': ['PR12ERT45', 'PR20PQR20', 'PR35ERT35', 'PR39GHT39'], '6269129163': ['PR06DEF06', 'PR10GHI10', 'PR15MNO15', 'PR16MNO16'], '7269129163': ['PR26XYZ26', 'PR28XYZ28', 'PR29XYZ29', 'PR48GHT48', 'PR49GHT49'], '8269129155': ['PR28XYZ28', 'PR29XYZ29', 'PR48GHT48', 'PR49GHT49']}

List of orders:
 ['5269129170', '4269129163', '3269129163', '6269129163', '7269129163', '8269129155']

List of aisles
 ['RGCD', 'ACB', 'RSBA', 'CRM', 'PG', 'PG']
 
'''




"""
List of all ordernumbers from multiple json inputs till now:
['3269129163']
Dictionary of ordernum mapped to list of products
{'3269129163': ['PR12ERT45', 'PR45GHT98']}
['RG']
List of all ordernumbers from multiple json inputs till now:
['3269129163', '4269129163']
Dictionary of ordernum mapped to list of products
{'3269129163': ['PR12ERT45', 'PR45GHT98'], '4269129163': ['PR01ABC01', 'PR06DEF06', 'PR22STU22']}
['RG', 'ACB']
List of all ordernumbers from multiple json inputs till now:
['3269129163', '4269129163', '3269129163']
Dictionary of ordernum mapped to list of products
{'3269129163': ['PR12ERT45', 'PR20PQR20', 'PR35ERT35', 'PR39GHT39'], '4269129163': ['PR01ABC01', 'PR06DEF06', 'PR22STU22']}
['RG', 'ACB', 'RSBA']
"""




