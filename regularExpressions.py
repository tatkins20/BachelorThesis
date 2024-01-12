import stanfordnlp
import nltk
import logging
import json
from re import *
from nltk.parse import CoreNLPParser
from stanfordnlp.server import CoreNLPClient
#parser = CoreNLPParser('http://localhost:9001')
#list(parser.tokenize(u"我家没有电脑。"))
#list(parser.parse(parser.tokenize(u"我家没有电脑。")))
nlp = stanfordnlp.Pipeline(lang='zh',processors='tokenize,mwt,pos')
doc = nlp("我家没有电脑。")
text = "我家没有电脑。"
andUTF = b'\xe5\x92\x8c'

def getPOS(doc):
    taggedList = []
    for sentence in doc.sentences:
        for word in sentence.words:
            wordPOSTuple = (word.text, word.pos)
            taggedList.append(wordPOSTuple)
    return taggedList

print(getPOS(doc))

#sentence = [('我', 'JJ'), ('电脑','NN'), ('和','CC'), ('手机','NN')]
corpusDoc = nlp(open('/Users/trekkatkins/Downloads/JCLCv2/F00003.txt','r').read())
pos = getPOS(corpusDoc)
#adjnounphrase = "NP : {<DT>?<JJ>+<DEC><NN><CC><DT>?<VV>+<DEC><NN>}"
adjnounphrase = "NP : {<NN><和><VV>}"
cp = nltk.RegexpParser(adjnounphrase)
result = cp.parse(pos)
print(result)
#result.draw()

#try calling nlp multiple times to see, if you don't want to run server multiple times

#print(*[f'word: {word.text+" "}\tupos: {word.upos}\txpos: {word.xpos}' for sent in doc.sentences for word in sent.words], sep='\n')
#words = open('/Users/trekkatkins/Downloads/JCLCv2/F00003.txt','r').read()
#r = compile(r'和',MULTILINE)
#print(r.findall(words))
