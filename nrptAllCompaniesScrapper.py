#-------------------------------------------------------------------------------
# Name:        Email Scraper
# Purpose:      Create a that find email address by the domain name
#
# Author:      Beny-DZIENGUE
#
# Created:     03/01/2019
# Copyright:   (c) Beny-DZIENGUE 2019
# Licence:     <your licence>
#-------------------------------------------------------------------------------

#import needed object
import re
import os
import sys
from concurrent.futures import ThreadPoolExecutor as PoolExecutor
import http.client
import socket
from bs4 import BeautifulSoup

def getPage(page):
    try:
        # always set a timeout when you connect to an external server
        url =  "nrpt.co.uk"
        #coonect to the http server, return the object connection of type http.client.HTTPConnection
        connection = http.client.HTTPSConnection(url, timeout=10)
        #send request to the server, return an object of type NoneTYpe
        connection.request("GET", page)
        #get response from the server, return the object response of type http.client.HTTPResponse
        response = connection.getresponse()
        #read and reurn the response
        return response.read()
    except socket.timeout:
        # in a real world scenario you would probably do stuff if the
        # socket goes into timeout
        pass

def getCompaniesPageLink():
    #initialise the object oage with the link of providers page, return the object page of type str
    page = "/become/providers/index.htm"
    #get the result of the research, return the object result of type bytes
    result = getPage(page)
    #create the object that will contain companies href, return the object companiesHref oof type list
    companiesPageHref = []
    #create a beautifumsoup object, return the object soup of type bs4.BeautifulSoup
    soup = BeautifulSoup(result,features="html.parser")
    #get all container of companies link, return the object companiesLinkContainer
    companiesLinkContainer = soup.find_all('div', class_='cwcf-company')
    #condition to read each element of companiesLinkContainer
    for div in companiesLinkContainer:
        #get href of div, return the object companiesLink of type str
        companiesLink = div.find('a').get('href')
        #add compaaniesLink to companiesHref
        companiesPageHref.append(companiesLink)
    #return companiesHref
    return companiesPageHref

def getCompaniesWebsiteLink(companiesPageHref):
    #excecute 7 instruction in same time
    with PoolExecutor(max_workers=7) as executor:
        #initialise the object that will contain the companie website link,return the object companieWebsiteLink of type str
        companieWebsiteLink = []
        #get the result of the research, return the object sourcePage of type bytes
        for sourcePage in executor.map(getPage, companiesPageHref):
            #create a beautifulsoup object, return the object soup of type bs4.BeautifulSoup
            soup = BeautifulSoup(sourcePage,features="html.parser")
            try:
                #get Companies website link , return the object companieWebsiteLink of type str
                companieWebsiteLink.append(soup.find('a', class_="wtrk-link").get('href'))
            except:
                pass
    return companieWebsiteLink

def writeModel(companieWebsiteLink):
    #create the object that will contain the final output, return the object finalOutput of type list
    finalOutput = []
    for link in companieWebsiteLink:
        #append name in finalOutput
        finalOutput.append(("   link   :"+("{}".center(10," "))+"\n").format(link))
    #return finalOutput
    return finalOutput

def whriteInOuput(finalOutput):
    """
    Whrite the result in a file txt
    """

    os.chdir("D:/IIHT/Python/Project/NRPT all companies scrapper/caches")
     #open text file, return  an object of type io.TextIOWrapper
    with open("Companies Website.txt", "w") as writ:
        #write each line in the object op, return an object of type int
        writ.write('\n'.join(finalOutput) + "\n")


companiesPageHref = getCompaniesPageLink()
companieWebsiteLink = getCompaniesWebsiteLink(companiesPageHref)
finalOutput = writeModel(companieWebsiteLink)
whriteInOuput(finalOutput)