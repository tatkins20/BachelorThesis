import os
import csv
import stanfordnlp
import nltk
from re import *
from nltk.parse import CoreNLPParser
from stanfordnlp.server import CoreNLPClient
parser = CoreNLPParser('http://localhost:9001')
nlp = stanfordnlp.Pipeline(lang='zh',processors='tokenize,mwt,pos')
path = '/Users/trekkatkins/Downloads/JCLCv2'
path2 = '/Users/trekkatkins/Downloads/JCLCv2/index'
#path = '/Users/trekkatkins/Desktop/ChineseCharacterCountTest'
all_files = os.listdir(path)
dictOfTxts = {}

andUTF = b'\xe5\x92\x8c'
locationUTF = b'\xe5\x9c\xa8'

def getPOS(doc):
    taggedList = []
    for sentence in doc.sentences:
        for word in sentence.words:
            wordPOSTuple = (word.text, word.pos)
            taggedList.append(wordPOSTuple)
    return taggedList

for root, dirs, files in os.walk(path):
    for file in files:
        with open('/Users/trekkatkins/Downloads/JCLCv2/index.csv') as index_csv:
            csv_reader = csv.DictReader(index_csv)


            if file.endswith('.txt'):
                with open(os.path.join(root,file), 'r') as f:
                    text = f.read()
                    for row in csv_reader:
                        andFrequency = 0
                        totalWords = 0
                        if row["country"] == "USA" or row["country"] == "UK" or row["country"] == "Germany" or row["country"] == "Costa Rica" or row["country"] == "Peru" or row["country"] == "France":
                            for word in text:
                                #print(word.encode('utf8'))
                                totalWords += 1
                                if word.encode('utf8') == andUTF:
                                    andFrequency += 1
                                    string = "" + str(totalWords) + ", " + str(andFrequency)
                                    dictOfTxts.update({file:string})
                f.close()


with open('test.csv', 'w') as f:
    for key in dictOfTxts.keys():
        f.write("%s,%s\n"%(key,dictOfTxts[key]))
f.close()



#check more broadly and see patterns that will negate adverbial phrases
#with verb-object phrases and other constructions

#regular expressions allow for negative things - not allow VV in front of NN.

#beginning of week 9 and end of week 9 to test with Chinese students
#email Chinese professor -
#what arrangements to make with students

#language mentors - help set up, Hu Zuyi (more time for students to try)

#Audrey in the language center - to work with multiple computers
#check if I can run the software on the language center computers
#pyc - compiled files save, copy and run the files on those computers
#alternatively use PASTA


grammar = r"""
        NP:
        {<NN.*><DEC?><NN.*>}
        {<NN.*><DEC?><PRP>}
        {<CD><NNB><NN.*>}
        {<JJ><DEC?><NN.*>}
        {<JJ><DEC?><PRP>}
        {<VV><DEC?><NN.*>}
        {^<VV><DEC?><NN.*>}
        {<DT><DEC?><NN.*>}
        {<IN><NN><NN.*>}
        {<IN><PRP><NN.*>}
        {<PRP><DEC?><NN.*>}
        {<PRP><DEC?><PRP>}
        {<DT><NN.*>}
        {<DT><PRP>}
        {<NN.*>}
        {<PRP>}

        CC_CLAUSE:
        {<NP><CC><NP>}

        IN_CLAUSE:
        {<NP><IN><NP>}

        """
i = 0
txtFiles = [keys for keys in dictOfTxts.keys()]
#print(txtFiles)
resultList = []
subtreeList = []
andIsCC = False
andIsIN = False

while i < len(txtFiles)/2:
    corpusDoc = nlp(open('/Users/trekkatkins/Downloads/JCLCv2/' + txtFiles[i], 'r').read())
    pos = getPOS(corpusDoc)
    cp = nltk.RegexpParser(grammar)
    result = cp.parse(pos)

    for subtree in result.subtrees(filter=lambda t: t.label() == 'CC_CLAUSE'):
        #print(subtree)
        if subtree[1][0].encode('UTF8') == andUTF and subtree[1][1] == 'CC':
            andIsCC = True
            subtreeList.append(subtree)
    for subtree in result.subtrees(filter=lambda t: t.label() == 'IN_CLAUSE'):
        #print(subtree)
        if subtree[1][0].encode('UTF8') == andUTF and subtree[1][1] == 'IN':
            andIsIN = True
            subtreeList.append(subtree)
    resultList.append(result)
    i += 1

with open('andClauses.txt', 'w') as f:
    if andIsIN or andIsCC:
        for parse in subtreeList:
            f.write("%s\n"%(parse))
    f.close()

with open('andSentences.txt','w') as k:
    if andIsCC or andIsIN:
        for result in resultList:
            k.write("%s\n"%(result))
    f.close()




#do a few manually, randomly select a few files, split and select and few sentences
#circumvent user interface, work out patterns if they come up with certain files
#then writes out result of whether it is correct or not

#see how many errors there are in the corpus text, go by hand and see if system actually catches the
#ones made by hand

#use a different text - go through and see the precision/recall evaluation on the texts
#calculate the error rate - required for presentation and paper
#look at and identify the texts you are using until running the experiment, don't change code by the time of evaluation

#
#print(\xe5\x92\x8c.decode('utf8'))
#
