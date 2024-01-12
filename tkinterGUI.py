import stanfordnlp
import nltk
import logging
import json
from re import *
from nltk.parse import CoreNLPParser
from stanfordnlp.server import CoreNLPClient
from tkinter import *
import py_compile
py_compile.compile('tkinterGUI.py')
nlp = stanfordnlp.Pipeline(lang='zh',processors='tokenize,mwt,pos')
window = Tk()
window.title("GUI Test")
label = Label(window, text="Enter sentence here", font=("Arial", 16))
window.geometry('1000x1000')
label.grid(column=0, row=0)
content = StringVar()

txt = Entry(window, width=75, textvariable=content)
txt.focus_force()
#txt.pack(side = TOP, ipadx = 30, ipady = 6)

txt.grid(column=1, row=0)
andUTF = b'\xe5\x92\x8c'

#CC_CLAUSE:
#{<NP><CC><NP>}

#IN_CLAUSE:
#{<NP><IN><NP>}

def getPOS(doc):
    taggedList = []
    for sentence in doc.sentences:
        for word in sentence.words:
            wordPOSTuple = (word.text, word.pos)
            taggedList.append(wordPOSTuple)
    return taggedList

def detectAndConstruction(text):
    hasAnd = False
    andIsCC = False
    andIsIN = False
    hasError = False

    for word in text:
        if word.encode('UTF8') == andUTF:
            hasAnd = True

    if hasAnd:
        res = nlp(text)
        postag = getPOS(res)

        grammar = r"""
        NP:
        {<NN.*>}
        {<NN.*><DEC?><NN.*>}
        {<NN.*><DEC?><PRP>}
        {<CD><NNB><NN.*>}
        {<JJ><DEC?><NN.*>}
        {<JJ><DEC?><PRP>}
        {<VV><DEC?><NN.*>}
        {^<VV><DEC?><NN.*>}
        {<DT><DEC?><NN.*>}
        {<IN><NN.*><NN.*>}
        {<IN><PRP><NN.*>}
        {<PRP><DEC?><NN.*>}
        {<PRP><DEC?><PRP>}
        {<PRP>}
        {<DT><NN.*>}
        {<DT><PRP>}


        CC_CLAUSE:
        {<NP><CC><NP>}

        IN_CLAUSE:
        {<NP><IN><NP>}


        """


        cp = nltk.RegexpParser(grammar)
        print(cp)
        chunked = cp.parse(postag)
        print(chunked)
        chunkedList = []
        subtreeList = []


        for subtree in chunked.subtrees(filter=lambda t: t.label() == 'CC_CLAUSE'):
            print(subtree)
            if subtree[1][0].encode('UTF8') == andUTF and subtree[1][1] == 'CC':
                andIsCC = True
                subtreeList.append(subtree)
                #print(andIsCC)

        for subtree in chunked.subtrees(filter=lambda t: t.label() == 'IN_CLAUSE'):
            print(subtree)
            if subtree[1][0].encode('UTF8') == andUTF and subtree[1][1] == 'IN':
                andIsIN = True
                subtreeList.append(subtree)

        chunkedList.append(chunked)

        with open('userInputandOutput.txt', 'a') as f:
            f.write("Input: "  + text)
            for chunk in chunkedList:
                f.write("%s\n"%(chunk))
            for subtree in subtreeList:
                f.write("%s\n"%(subtree))

            f.close()


    else:
        requestLabel = Label(window, text="Please enter a sentence with 和", font=("Arial", 16))
        requestLabel.grid(column=1, row=3)

    if andIsCC or andIsIN:
        #for chunk in chunked:
            #if chunk.encode('UTF8') == andUTF:
        correctToReturn = "The use of 和 in this sentence/phrase seems to be correct: "
        correctToReturn += "\n" + txt.get()
        chunkLabel = Label(window, text=correctToReturn, font=("Arial", 16))
        chunkLabel.grid(column=1, row=2)
    else:
        #for chunk in chunked:
        mistakeToReturn = "This sentence/phrase seems to be incorrect with the use of 和: "
        mistakeToReturn += "\n" + txt.get()
        mistakeToReturn += "\n" + "Hint: remember that 和 must be used between two noun phrases."
        andUsageLabel = Label(window, text=mistakeToReturn, font=("Arial", 16))
        andUsageLabel.grid(column=1, row=3)



def clicked():
    res = txt.get()
    detectAndConstruction(res)

#create more complex regexp
#look at specific corpus examples - try with more of those grammar constructs

#preprocessing - if "and" is not there - print message
#once recieving the output, check the CC to see if it is the right CC

#break sentence into multiple phrases
#keep notes and track of the text files - whether they have mistakes

bt = Button(window, text = "Enter", command=clicked)
bt.grid(column=1, row=1)
window.mainloop()


#save files that students input and the output of the input
#save as much as needed to diagnose what has happened
#list of forms and documents for students receiving the payments and experiment

#next week's meeting outline for presentation (word doc, slides) - big topics, what am i going to say
#similar content as last term - more space/time to talk about details

#have some sample set that isn't looked at - have varied range from different countries
#provide feedback for errors and notification in the interface

#look at patterns that there are ands but cannot identify a CC clause, there must be a mistakes
#there is a problem with the use of "and", if there is a common mistake - write a pattern for that
#see if that pattern matches  (it's wrong because of that specific construction) - if the information
#isn't correct may be better to just say there is something wrong. Can note: here's how to use "and".
#
