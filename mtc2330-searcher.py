import lucene
import sys
import os
import re
import math
from java.io import File
from collections import Counter
from java.io import StringReader


lucene.initVM()

#Pylucene Imports
from org.apache.lucene.analysis.standard import StandardAnalyzer
from org.apache.lucene.store import FSDirectory
from org.apache.lucene.index import DirectoryReader
from java.io import File
from org.apache.lucene.analysis.tokenattributes import CharTermAttribute
from org.apache.lucene.index import Term


#Access the index files stored in the index path
indexpath=File(sys.argv[1]).toPath()    


#Create objects and set globals= variables
analyzer=StandardAnalyzer()                                  #Setting the analyzer as standard analyzer
directory = FSDirectory.open(indexpath)                      #set the indexpath for pylucene searcher
reader=DirectoryReader.open(directory)                       #Create an object of directory reader pointing to index directory
CS_C=reader.numDocs()                                        #Number of documents in the collection
ADL=reader.getSumTotalTermFreq("CONTENT")/CS_C               #Average Document Length Of The Collection


#Method used to parse the contents using Standard Analyzer
def Analyse(text):
    analyzer2=StandardAnalyzer() 
    stream=analyzer2.tokenStream("",StringReader(text))
    stream.reset()
    tokens=[]
    while stream.incrementToken():
        tokens.append(stream.getAttribute(CharTermAttribute.class_).toString())
    return tokens    



#Method To Get The Term Frequency In The Document
def getTF(words,term):
    frequency=Counter(words)
    return frequency[term]



#Method To Count The AVG_Term_Frequency of all terms in the document
def get_AVGTF(words):
    frequency=Counter(words)
    total_frequency=0
    for word in frequency:
        total_frequency+=frequency[word]
    return total_frequency/len(frequency) 


#Method to calculate the MATF score for each term
def GET_MATF_SCORE(TF,Qlen,DOC_FREQ,CTF,DOCLEN,AVGTF):
    global CS_C,ADL
    TFF,TDF=0,0
    w=2/(1 + math.log2(1 + Qlen ))
    RITF=math.log2(1+TF)/math.log2(1+AVGTF)
    LRTF=TF*(math.log2(1+(ADL/DOCLEN)))
    BRITF=RITF/(1+RITF)
    BLRTF=LRTF/(1+LRTF)
    TFF=(w*BRITF) + (1-w)*BLRTF        #Term Frequency Factor
    IDF=math.log((CS_C+1)/DOC_FREQ)    #Inverse Doc Frequency
    AEF=CTF/DOC_FREQ
    TDF=IDF*(AEF/(1+AEF))              #Term Discriminating Factor
    return TFF*TDF


#Access the queries one by one and rank the documents
def search_docs(query):
    DOC_Scores,tokens=[],[]                                                            #List containg the docscores and tokens of this query
    Qlen=len(query.split()) 
    try:
        token_stream = analyzer.tokenStream("CONTENT", query)
        char_term_attribute = token_stream.addAttribute(CharTermAttribute.class_)
        token_stream.reset()
        while(token_stream.incrementToken()):
            tokens.append(char_term_attribute.toString().lower())                      #Append the tokens to list in lowercase                 
    finally:
        token_stream.close()    
    Qlen=len(tokens)                                                                    #Setting the number of terms in this query
    for docID in range(reader.maxDoc()):
        doc = reader.document(docID)
        DOCNO,CONTENT=doc.get('DOCNO'),doc.get('CONTENT')
        flag=False
        for token in tokens:
            if(CONTENT.lower().find(token)!=-1):                                        #Check if atleast one token is prsent in the doc then proceed else not
                    flag=True
                    break
        if(not flag):                                                                    
           DOC_Scores.append((DOCNO,0))
           continue                                                                     #If None of the term is present then no need to check the doc                             
        CONTENT=Analyse(CONTENT)                                                        #Parse the content using analyzer
        DOCLEN=len(CONTENT)                                                             #Get the Doc Length in terms of the terms
        AVGTF=get_AVGTF(list(map(lambda x:x.lower(),CONTENT)))                          #Get The Average Term Frequency
        DOCSCORE=0                                                                      #Set Initial Doc Score as 0
        try:
            token_stream2 = analyzer.tokenStream("CONTENT", query)                       #Create Tokens using Standard Analyzer
            char_term_attribute = token_stream2.addAttribute(CharTermAttribute.class_)   #Allows access to the toen text
            token_stream2.reset()  
            while token_stream2.incrementToken():
                obterm=Term("CONTENT",char_term_attribute.toString())                   #Create a Term object
                if(char_term_attribute.toString().lower() not in  list(map(lambda x:x.lower(),CONTENT))):
                    DOCSCORE+=0                                                         #Term not present in the document
                    continue
                DOC_FREQ=reader.docFreq(obterm)                                         #Document Frequency Of a term in the collection
                CTF=reader.totalTermFreq(obterm)                                        #Total occurence of the term in the entire collection
                TF=getTF(list(map(lambda x:x.lower(),CONTENT)),char_term_attribute.toString().lower())                #Get the term Frequency Of The Term In The Document
                Score=GET_MATF_SCORE(TF,Qlen,DOC_FREQ,CTF,DOCLEN,AVGTF)                 #Get The MatF score of this document for this term
                DOCSCORE+=Score                                                         #Add score for individual terms                                                    
        finally:
            DOC_Scores.append((DOCNO,DOCSCORE))                                         #Append The tuple containg Docno and Score for this document to Doc_Scores list
            token_stream2.close()
    top_1000_docs=sorted(DOC_Scores,key=lambda x:x[1],reverse=True)[:1000]
    return top_1000_docs



#Acess the query one by one and send for document retrieval
Query_File_Path='/'+sys.argv[2]
for files in os.listdir(Query_File_Path):
    path=Query_File_Path+'/'+files
    content=open(path,'r')
    Query_num=0
    while True:
        line=content.readline()
        if not line:                #End of file reached
            break
        if(line.startswith('<num>')):
            Query_num=re.search(r'\d+', line).group()
        elif(line.startswith('<title>')):
            sindex,eindex=line.find('>'),line.rfind('<')
            query=line[sindex+2:eindex-1]
            result=search_docs(query)
            for i in range(len(result)):
                print(f"{Query_num}\t Q0\t {result[i][0]}\t {i+1} \t {result[i][1]}\t CS2330")
    content.close()