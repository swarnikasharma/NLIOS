# sudo pip install pexpect unidecode
# git clone git://github.com/dasmith/stanford-corenlp-python.git
# cd stanford-corenlp-python
# wget http://nlp.stanford.edu/software/stanford-corenlp-full-2014-08-27.zip
# unzip stanford-corenlp-full-2014-08-27.zip

# python corenlp.py -H 0.0.0.0 -p 3456
from nltk.tree import *
import jsonrpc
from simplejson import loads
server = jsonrpc.ServerProxy(jsonrpc.JsonRpc20(),jsonrpc.TransportTcpIp(addr=("0.0.0.0", 3456)))
result = loads(server.parse("Hello world.  It is so beautiful"))
print "Result", result
sent=result[u'sentences'][0][u'parsetree']
tree=Tree.fromstring(sent)
tree.pretty_print()
np = [" ".join(i.leaves()) for i in tree.subtrees() if i.label() == 'NP']




result = loads(server.parse("display content of rohit.txt"))
sent=result[u'sentences'][0][u'parsetree']
tree=Tree.fromstring(sent)
tree.pretty_print()



result = loads(server.parse("create a new folder"))
tree=Tree.fromstring(result[u'sentences'][0][u'parsetree'])

for i in tree.subtrees():
	if(i.label()=="NP"):
		x=i