from django.shortcuts import render,redirect
from WB.generate import generate
from WB.lavenshtein import batch
from django.core.files.storage import FileSystemStorage

# Create your views here.

def upload(request):
	return render(request,"Walket.html")


def output(request):
	if request.method == 'POST':
		
		jsonfiles = request.FILES.getlist('jsonfiles')
		cnt = len(jsonfiles)
		print(cnt)
		filenames = []
		fs = FileSystemStorage()
		if cnt == 0: return render(request,'Walket.html')
		for f in jsonfiles:
			if fs.exists(f.name): fs.delete(f.name)
			fs.save(f.name,f)
			filenames.append(str(f))
		print(filenames)
		data, orderList, aisleList, shelfList = generate(filenames)
		batches, order_batches, shelves_batches = batch(data, orderList, aisleList, shelfList)
		length = len(batches)
		table = []
		cell = []
		for i in range(0,length):
			cell = []
			cell.append(order_batches[i])
			cell.append(batches[i])
			cell.append(shelves_batches[i])
				
			table.append(cell)
		print("*********")
		print(table)
	return render(request,'Output.html',{'table':table})