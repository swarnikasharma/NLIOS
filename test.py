f=open("testdata.csv")

train=[]

for line in f:
	sent=line[:-1].split(",")
	row=[]
	row.append(sent[0].lower())
	row.append(sent[1].lower())
	train.append(row)