from nltk.tree import *
import jsonrpc
from simplejson import loads
import subprocess as sp
from lstm import *

#Connecting to nltk server
server = jsonrpc.ServerProxy(jsonrpc.JsonRpc20(),jsonrpc.TransportTcpIp(addr=("0.0.0.0", 3456)))

#Function to get noun list
def getNoun(noun):
	nlist=[]
	for i in noun.subtrees():
		if(i.label()=="NN"):
			np =" ".join(i.leaves())
			nlist.append(np)
	return nlist


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

def processCommand(cmdString,nounPhrase):
	tokens=cmdString.split(" ")
	command=""
	for x in tokens:
		if(x.startswith("<")):
			if(len(nounPhrase)<2):
				print "Missing "+x[1:-1]+" Please enter now "
				temp=raw_input()
				command=command+" "+temp
			else:
				command=command+" "+str(nounPhrase[1])	
		else:
			command=command+" "+x
	return command.strip()	

def cmdGenerateTypeOne(user_input,cmdString):
	result = loads(server.parse(user_input))
	tree=Tree.fromstring(result[u'sentences'][0][u'parsetree'])
	mTree=tree[0][0]
	child=[]
	for i in mTree:
		child.append(i)
	for x in child:
		if(x.label().startswith('N')):
			nounPhrase=getNoun(x)
	return processCommand(cmdString,nounPhrase)

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
	# if(dis[0][2:-2]<4.0):
	# 	return "ERROR:Unable to generate command"
	details=cmd[cmdDict[rules[dis[0]]]]
	cmdString=details[0]
	cmdType=details[1]
	x=""
	if(cmdType=='1'):
		print "Type 1 command"
		x=cmdGenerateTypeOne(user_input,cmdString)
	elif(cmdType==0):
		x=cmdString
	return x
    	

cmdDict={}
cmd={}
sls=init(cmdDict,cmd)
query="qu"
while(query!=""):
	query=raw_input()
	command=handleQuery(query,cmdDict,cmd,sls)
