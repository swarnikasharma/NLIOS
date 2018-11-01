#Tree('ROOT', [Tree('S', [Tree('VP', [Tree('VB', ['create']), Tree('NP', [Tree('NN', ['folder']), Tree('NN', ['rohit'])]), Tree('PP', [Tree('IN', ['under']), Tree('NP', [Tree('NP', [Tree('NNS', ['downloads'])]), Tree('PP', [Tree('IN', ['with']), Tree('NP', [Tree('DT', ['all']), Tree('JJ', ['open']), Tree('NNS', ['permissions'])])])])])])])])

from nltk.tree import *
import jsonrpc
from simplejson import loads
server = jsonrpc.ServerProxy(jsonrpc.JsonRpc20(),jsonrpc.TransportTcpIp(addr=("0.0.0.0", 3456)))

def getNoun(noun):
	nlist=[]
	for i in noun.subtrees():
		if(i.label()=="NN"):
			np =" ".join(i.leaves())
			nlist.append(np)
	return nlist



query="hello"
while(query!=""):
	query=raw_input()
	result = loads(server.parse("create folder rohit inside downloads"))
	tree=Tree.fromstring(result[u'sentences'][0][u'parsetree'])
	mTree=tree[0][0]
	child=[]
	for i in mTree:
		child.append(i)
	for x in child:
		if(x.label().startswith('V')):
			for i in x.subtrees():
				verbPhrase =" ".join(i.leaves())
		elif(x.label().startswith('N')):
			nounPhrase=getNoun(x)
	stat=str(verbPhrase)+" "+str(nounPhrase[0])
	cmd="mkdir "+str(nounPhrase[1])
	print stat