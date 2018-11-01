from nltk.tree import *
import jsonrpc
from simplejson import loads
import subprocess as sp
from lstm import *

#Connecting to nltk server
server = jsonrpc.ServerProxy(jsonrpc.JsonRpc20(),jsonrpc.TransportTcpIp(addr=("0.0.0.0", 3456)))

def init(cmdDict,cmd):
	#Training the new model
	sls=lstm("bestsem.p",load=True,training=True)
	print "Pre training "
	train=pickle.load(open("myTrain3.p",'rb'))
	sls.train_lstm(train,75)	
	#Loading the command dictionary
	f=open("commands.csv")
	line=f.read().splitlines()
	for x in line:
	    c=x.split(",")
	    cmdDict[c[1].lower()]=c[0].lower()
	    details=[]
	    details.append(c[2].lower())
	    details.append(c[3].lower())
	    cmd[c[0].lower()]=details
	#tmp = sp.call('clear',shell=True)
	print "Model trained"
	return sls	

def processCommand(cmdString):
	tokens=cmdString.split(" ")
	command=""
	for x in tokens:
		if(x.startswith("<")):
			print "Enter "+x[1:-1]
			temp=raw_input()
			command=command+" "+temp	
		else:
			command=command+" "+x
	return command.strip()	

def handleQuery(user_input,cmdDict,cmd,sls):
	words=user_input.split(" ")
	qwords=[]
	for word in words:
		if(word in model.vocab):
			qwords.append(word)
		else:
			qwords.append("noun")
	query=""
	rules={}
	for x in qwords:
		query=query+" "+x
	query=query.strip() 
	for key in cmdDict.keys():
		n=sls.predict_similarity(query,key)*4.0+1.0
		rules[str(n)]=key
	dis=sorted(rules.iterkeys(),reverse=True)		
	details=cmd[cmdDict[rules[dis[0]]]]
	cmdString=details[0]
	cmdType=details[1]
	x=processCommand(cmdString)
	return x

cmdDict={}
cmd={}
sls=init(cmdDict,cmd)
query="qu"
while(query!=""):
	query=raw_input()
	command=handleQuery(query,cmdDict,cmd,sls)
