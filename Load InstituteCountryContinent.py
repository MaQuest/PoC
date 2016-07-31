#Best idea is to load all JournalNames and the country associated with them and the continent 

import json
from py2neo import Graph, authenticate
from twisted.protocols.telnet import NULL
 
# replace 'foobar' with your password
authenticate("localhost:7474", "neo4j", "lunatic123")
graph = Graph()
 
 
  
Fn ="InstituteCountryContinent.txt"     
lookupData = json.loads(open(Fn).read())
#print lookupData


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

def creteUniqueConstraint():
    query = """ 
    CREATE CONSTRAINT on (p:Country) ASSERT p.name is UNIQUE;
    """r
    graph.cypher.execute(query, json = json)
    
    query = """ 
    CREATE CONSTRAINT on (p:Region) ASSERT p.name is UNIQUE;
    """
    graph.cypher.execute(query, json = json)    
 
    query = """ 
    CREATE CONSTRAINT on (p:Institute) ASSERT p.name is UNIQUE;
    """
    graph.cypher.execute(query, json = json)
    
    #other few that I executed from the UI are:
    #CREATE CONSTRAINT on (p:Article) ASSERT p.title is UNIQUE;
    #CREATE CONSTRAINT on (p:Author) ASSERT p.name is  UNIQUE;
    #CREATE CONSTRAINT on (p:Journal) ASSERT p.name is  UNIQUE; 
    return

def loadCountryContinent(json):
    
    query = """
    WITH {json} AS document
    UNWIND document AS info
    MERGE (c:Country {name: info.Country})
    MERGE (insti:Institute {name: info.Institute}) 
    MERGE (r:Region {name: info.Region})
    MERGE (insti)-[:IS_IN]->(c)
    MERGE (c)-[:BELONGS_TO]->(r)
    """
    #name =  graph.cypher.execute(query, json = json)
    #print name
    
    
    return


#to load country data
loadCountryContinent(lookupData)
#creteUniqueConstraint() #a must for MERGE to work

