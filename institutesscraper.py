from BeautifulSoup import BeautifulSoup
from time import sleep
from random import choice
from csv import DictWriter
import urllib2
import sys
import json
import datetime
import codecs
import xlrd

out_file = file("InstituteCountryContinent.txt",'a')
# lookup country from the file
def readCountinents():
    # Open the workbook
    xl_workbook = xlrd.open_workbook("new.xls")

    # List sheet names, and pull a sheet by name
    #
    sheet_names = xl_workbook.sheet_names()
    print('Sheet Names', sheet_names)
 
    #xl_sheet = xl_workbook.sheet_by_name(sheet_names[0])
     
    xl_sheet = xl_workbook.sheet_by_index(0)
    print ('Sheet name: %s' % xl_sheet.name)
    num_cols = xl_sheet.ncols
    print num_cols
    listRegions =  xl_sheet.row(0) #returns all the CELLS of row 0,
    #print listRegions    
    data = [] #make a data store
    for i in xrange(xl_sheet.ncols):
        data.append(xl_sheet.col_values(i)) #drop all the values in the rows into data
    #print data
    listmy = []
    for i in data:
        count = 1
        while count < len(i) and i[count]!='':
            dict1 = {"region": i[0], "country":i[count]}
            listmy.append(dict1)
            count = count+1
    #print len(listmy)
    #print listmy
    
    return listmy

def printToFile(somestr):
    global out_file
    json.dump(somestr, out_file)

#write to a file
def writeToSpreadsheet(dictItem):
    with open('InstituteCountryContinent.csv','a') as outfile:
        writer = DictWriter(outfile, ['Institute', 'Country', 'Region'])
        writer.writerow(dictItem)



def getContinent(lookupList, country):
    for i in lookupList:
        if country == i['country']:
            #print country, i['region']
            return i['region']
        elif country in i['country']:
            #print country, i['region']
            return i['region']

country_contList = readCountinents()

html_page = open("w.html")
if html_page!= False:
    soup = BeautifulSoup(html_page)
    rows = soup.findAll("tr")
    
    for i in rows[1:len(rows)]:
        j = i.findAll("td")
        #print j[1].text, j[2].text
        region = getContinent(country_contList, j[2].text)
        dict1 = {"Institute":(j[1].text).encode('utf-8'), "Country":(j[2].text).encode('utf-8'), "Region":region}
        #writeToSpreadsheet(dict1)
        printToFile(dict1)
        
        
