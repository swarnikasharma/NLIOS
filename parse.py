# import subprocess as sp
# for i in range(0,10):
# 	print i

# tmp = sp.call('clear',shell=True)

# for i in range(11,20):
# 	print i

import pickle
f=open("tuning.csv")

train=[]

for line in f:
	sent=line[:-1].split(",")
	for i in range(1,len(sent)):
		if sent[i]:
			row=[]
			row.append(sent[0].lower())
			row.append(sent[i].lower())
			row.append(4.6)
			row.append('NEUTRAL')
			train.append(row)		

pickle.dump( train, open( "myTrain3.p", "wb" ) )

