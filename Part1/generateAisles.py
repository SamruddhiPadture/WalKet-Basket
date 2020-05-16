import json
import csv

orderList = [] #list of all order numbers due to multiple files
aisleList=[]   #list of all aisle strings of multiple user--to be used for levenstein
data ={}       #mapping of orderNo and its ProductIds

#apply looping for multiple inputs after this only otherwise orderList and aisleList will get reset everytime.

#fileList=['Desktop/ord4.json','Desktop/ord2.json','Desktop/ord3.json']
fileList=["Desktop/ord4.json"]
#with open("Desktop/ord1.json", "r") as read_file:
for j in range(0,len(fileList)):
    with open(fileList[j],"r") as read_file:
        jsonInput = json.load(read_file)                    #read json input file
        #print(jsonInput)

        orderList.append(jsonInput['orderNo'])
        print("List of all ordernumbers from multiple json inputs till now:")
        print(orderList)

        productList=[]                                      #list of productIds for one user
        
        for i in jsonInput['products']:
            productList.append(i['productId'])

        data[jsonInput['orderNo']]=productList
        print("Dictionary of ordernum mapped to list of products")
        print(data)

        with open('Desktop/products.csv', 'r') as file:      #read csv file
            reader = csv.reader(file)
            aisle = []

            for i in range(0,len(productList)):
                for row in reader:
                    if row[0]==productList[i]:
                        aisle.append(row[2])
                        break
                        
            aisle = list(dict.fromkeys(aisle))
            aisleList.append(''.join(aisle))
            print(aisleList)





