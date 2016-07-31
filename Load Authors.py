#Best idea is to load all JournalNames and the country associated with them and the continent 

import json
from py2neo import Graph, authenticate
from twisted.protocols.telnet import NULL
 
# replace 'foobar' with your password
authenticate("localhost:7474", "neo4j", "lunatic123")
graph = Graph()
 
 
listofFiles = ['A_J_appliedSoftComputing.txt','A_J_Genetic Programming and Evolvable Machines.txt','A_J_Neurocomputing.txt']
path = "/home/gouri/workspace/Prj/dump/JournalsDataAuthors/"

Fn ="InstituteCountryContinent.txt"     
lookupData = json.loads(open(Fn).read())

   
def connectAnJ(json):
    query = """
    WITH {json} AS document
    UNWIND document AS article
    UNWIND document AS journal
    MERGE (a:Article {title: article.A_Title, year: article.A_Year, authors: article.A_Authors, NonLocalcount: article.A_NonLocalCiteCount, totalcites: article.A_TotalCites, selfcites: article.A_SelfCites }) 
    MERGE (j:Journal {name: journal.J_Name})
    MERGE (a)-[:PUBLISHED_IN]->(j)
    """
#     query = """ 
#     WITH {json} AS document
#     UNWIND document AS article
#     UNWIND document AS journal
#     MERGE (c:Journal {name: jounal.name})
#     MERGE (sc:Article {title: article.title})
#     MERGE (sc)-[:PUBLISHED_IN]->(c)
#     """
#     
    
    graph.cypher.execute(query, json = json)

    query = """ 
    CREAT CONSTRAINT on (p:Journal) ASSERT p.name is UNIQUE;
    """
    graph.cypher.execute(query, json = json)

    query = """ 
    CREAT CONSTRAINT on (p:Article) ASSERT p.title is UNIQUE;
    """
    graph.cypher.execute(query, json = json)
 
    return



def readJSONfile(fname):
    data = json.loads(open(fname).read())    
    return data


def searchInrepo(InstiName):
    for i in lookupData:
        if (i.get('Institute')).strip() == InstiName.strip():
            print i
            return i
        #else:
            #print "No Match"
    return


def processAffil(dictAuth):
    affStr = dictAuth['Aff']
    #print affStr, dictAuth['author']
    tempArr = affStr.split(',')
    countryIndex = len(tempArr)
    dict1 = {}
    #if len(tempArr)<=1:
    #    dict1 = ({"country":tempArr[countryIndex-1], "Institute":"NoInfo"})
    #    dictAuth.update(dict1)
    lookupInfo = {}   
    if len(tempArr) > 1:
        for i in tempArr:
            if "University" in i or "Institute" in i:
                print "Name is: " + str(i)
                lookupInfo= searchInrepo(str(i))
                #dict1 = ({"country":(tempArr[countryIndex-1]).encode('utf-8'),"Institute":i.encode('utf-8')})
                if lookupInfo!=None:
                    dictAuth.update(lookupInfo)
                else:
                    dict1 = ({"Country":(tempArr[countryIndex-1]).encode('utf-8'),"Institute":i.encode('utf-8'), "Region": "Unknown"})
    else:
        dict1 = ({"Country":"India","Institute":"Panjab University", "Region":"Southern Asia"})
        dictAuth.update(dict1)          
    #print dictAuth        
    return dictAuth

def AddToGraphDB(json):
    print len(json)
    for i in json:
        print i
        value = i.get('Country') #, "NOData")
        if str(value).strip() == "NOData":
            print value
            json.remove(i)
    print len(json)      
    
    #del json[22]
    #del json[11]
    #del json[14]       
    query = """ 
    WITH {json} AS document
    UNWIND document AS info
    RETURN info.author,info.Aname,info.Institute, info.Country """
    Jname =  graph.cypher.execute(query, json = json)
    print Jname
     
    
    #query = """
    #WITH {json} AS document
    #UNWIND document AS info
    #MERGE (a:Author {name: info.author})
    #MERGE (art:Article {title: info.Aname}) 
    #MERGE (i:Institute {name: info.Institute})
    #MERGE (c:Country {name: info.country})
    #MERGE (a)-[:Authored]->(art)
    #MERGE (a)-[:WORKS_FOR]->(i)
    #MERGE (i)-[:IS_IN]->(c)
    #"""

    #step 1: Add the Author and article first and then comment this code
    #query = """
    #WITH {json} AS document
    #UNWIND document AS info
    #MERGE (a:Author {name: info.author})
    #MERGE (art:Article {title: info.Aname}) 
    #MERGE (a)-[:Authored]->(art)"""
    
  
    #step 2: Now Uncomment this code and execute 
    query = """
    WITH {json} AS document
    UNWIND document AS info
    MERGE (a:Author {name: info.author})
    MERGE (i:Institute {name: info.Institute})
    MERGE (a)-[:WORKS_FOR]->(i)
    """


    graph.cypher.execute(query, json = json)
    return

def loadAuthors(json):
    data = []
    
    for i in json:
        AName = i['A_Title']
        authors = i['A_Authors'].split(',')
        affs = []
        keys = i.keys()
        for j in keys:
            if "Aff" in j:
                affs.append(i[j])
    	#print authors
        #print affs        
        # CREATE AUTHOR AND AFF PAIR
        i = 0
        while  i < len(authors):
        
            dict1 = {'author':authors[i], 'Aff':affs[i], 'Aname':AName}
            #print dict1
            data.append(dict1)
            i = i+1    
    print data    
    
    #process the data to resolve country, Institute
    for d in data:
        ch_d= processAffil(d)
        d.update(ch_d)
    print "--------------------------------------------------------------------------------------------"
    print data    
    
    print "###########################################################################################"
    AddToGraphDB(data)
            
    return


Fname = path+listofFiles[0]
#json = json.loads(open(Fname).read())
json  = readJSONfile(Fname)    
 
#for i in json:
#    chName = i['J_Name'].replace('+', " ")
#    i.update({'J_Name':chName})
    #print i['J_Name']



#connectAnJ(json)
loadAuthors(json)


