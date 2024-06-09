import sys
import os
import lucene
from java.io import File


# Indexer imports:
from org.apache.lucene.analysis.standard import StandardAnalyzer
from org.apache.lucene.index import IndexWriter, IndexWriterConfig,IndexOptions
from org.apache.lucene.store import FSDirectory
import org.apache.lucene.document as document
from org.apache.lucene.document import Field, FieldType



lucene.initVM()



#Path that contains all the documents
collection_path=sys.argv[1]
#Path to store the index
index_path=File(str(sys.argv[2])).toPath()
indexDir = FSDirectory.open(index_path)

#Configure the IndexWriter
writerConfig = IndexWriterConfig(StandardAnalyzer())
writer = IndexWriter(indexDir, writerConfig)

#print(collection_path,index_path)

count=0 #Initilize a counter

#Method to add the extracted contents to index file one-by-one
def indexTRECdocs(docno, content):
    doc = document.Document()
    #Set the field type for the CONTENT field in order to store the term frequency vectors
    field_type = FieldType()
    field_type.setStored(True)
    field_type.setTokenized(True)
    field_type.setStoreTermVectors(True)
    field_type.setStoreTermVectorPositions(True)
    field_type.setStoreTermVectorOffsets(True)
    field_type.setIndexOptions(IndexOptions.DOCS_AND_FREQS_AND_POSITIONS_AND_OFFSETS)
    
    doc.add(document.Field("DOCNO", docno, document.TextField.TYPE_STORED))
    doc.add(Field("CONTENT",content, field_type))
    
    writer.addDocument(doc)

#Method to extract the contents out of the documents
def extract_content(collection_path):
      #global contentdf
      global count
      files=[f for f in os.listdir(collection_path)]     #Build a list of all the files under the directory
      #parse the files one by one
      for file in files:
            path=collection_path + "/" +str(file)
            fileptr=open(path,"r",encoding='latin-1')
            data=fileptr.readlines()                    #Read all the lines in the file into a list
            content,docno="",None                       #Variable to store the content under each DOCNO along with the DOCNO
            for line in data:   
            #if reached the end of a document in a file   
               if(line.startswith("</DOC>")):
                    #print(file,docno)
                    count+=1  
                    indexTRECdocs(docno,content)         #Send the docno and content for indexing
                    content,docno="",None                #Reset the variables
               elif(line.startswith("<DOCNO>")):
                    #Extract the DOCNO from <DOC></DOCNO>
                    if(not str(file).startswith("ft")):
                         words=line.split()
                         docno=words[1]
                    else:
                       start=line.find(">")
                       stop=line.find("</")
                       docno=line[start+1:stop]
               else:
                    linecontent,i="",0
                    while(i<len(line)):
                         if(line[i]=="<"):
                              while(line[i]!=">"):
                                   i+=1
                              i+=1
                         else:
                              linecontent+=line[i]
                              i+=1
                    if(len(linecontent)>0 and len(content)>0):
                         content=content+linecontent
                    elif(len(linecontent)>0 and len(content)==0):
                         content=linecontent
            fileptr.close()

#Method used to close the writer            
def closeWriter():
    writer.close()           
            
#Extract all the contents from the docs in the corpus one by one and add to index
extract_content(collection_path)
print("Indexing Completed \n No. Document indexed:",count)
closeWriter() #Close the writer

