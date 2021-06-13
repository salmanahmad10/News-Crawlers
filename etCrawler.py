import selenium 
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import os
from os import path
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import StaleElementReferenceException
from selenium.common.exceptions import TimeoutException

import traceback
import logging
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.expected_conditions import presence_of_element_located
import csv
import time
import pymongo
import re
from pymongo import MongoClient
from datetime import date
import enum
from enum import Enum
import requests

chrome_options = Options()
chrome_options.add_argument("--incognito")
chrome_options.add_argument("--window-size=1920x1080")
Path=r"C:\Users\salman\Desktop\chromedriver\chromedriver.exe"
driver = webdriver.Chrome(options=chrome_options, executable_path=Path)
url="https://tribune.com.pk/"
today = date.today()

class expressT:
    global catagories

    catagories=["https://tribune.com.pk/","https://tribune.com.pk/pakistan/","https://tribune.com.pk/business/",
                "https://tribune.com.pk/technology","https://tribune.com.pk/world/","https://tribune.com.pk/sports/"]
    
    def connect_db():
        client = MongoClient("localhost", 27017)
        return client

  

    client = connect_db()
    global db
    global collection
    db = client['expressDB']#database creation in mongodb
    collection=db['expressT'] # document creation
     
    global unvisitedURLs
    unvisitedURLs=db['unvisitedURLs']
    global visitedURLs
    visitedURLs=db['visitedURLs']
    global catagoriesT
    catagoriesT=db['catagoriesT']

    
    global catagoriesURLS
    def catagoriesURLS(self):              
        for x in range(len(catagories)):
            if(db.visitedURLs.find({"urls":catagories[x]}).count()==0 and db.catagoriesT.find({"urls":catagories[x]}).count()==0):
                    catagoriesT.insert_one({"urls":catagories[x]})
    
# =============================================================================
#             article links getting crawled
# =============================================================================
   
    def crawlLinks(self):   
        id_string=""
       
        driver.get(url)
        time.sleep(3)
        urlVisited=False
        catagoriesURLS(self)
     
        documents = list(catagoriesT.find())
        i=0
        for k,doc in enumerate( documents,start=0):
                mainUrl=doc["urls"]
                if(db.visitedURLs.find({"urls":mainUrl}).count()==0):
                    visitedURLs.insert_one({"urls":mainUrl})
                driver.get(mainUrl)
                time.sleep(3)
                try:
                    submenu=driver.find_element_by_id("sub-nav")
                    
                    sub_menu_links=submenu.find_elements_by_tag_name("a")
                    for x in sub_menu_links:
                         string=x.get_attribute("href")
                         print(string)
                         if(db.catagoriesT.find({"urls":string}).count()==0 and db.visitedURLs.find({"urls":string}).count()==0):
                             data={"urls":string}
                             catagoriesT.insert_one(data)
                             if(mainUrl=="https://tribune.com.pk/sports/"):
                                 break
                except Exception as e:
                    pass
                
# =============================================================================
#     #                     links fetched
# =============================================================================
    def crawl(self,url,urlList):
        documents = urlList
        for k,doc in enumerate( documents,start=0):
            mainUrl=doc
            try:    
                elementsI = driver.find_elements_by_xpath("//a[@href]")#for stories
                for x in elementsI:                           
                    string=x.get_attribute("href")#get all links from mainURL
                    if("story" in string):
                        print(string)
                        if(db.visitedURLs.find({"urls":string}).count()==0 and db.catagoriesT.find({"urls":string}).count()==0 and db.unvisitedURLs.find({"urls":string}).count()==0 and string.startswith("https://tribune.com.pk")):#if mainurl page has unique links append the links in urlList 
                            data={"urls":string}
                            unvisitedURLs.insert_one(data)
                        else:
                            pass
            except Exception as e:
                pass
        documents = list(unvisitedURLs.find())
        for k,doc in enumerate( documents,start=0):

            if "story" in mainUrl:#if mainUrl has "story" in it meaning it has news article
                    try:
                        storyurls=mainUrl
                        storyurls=mainUrl.split("/")#split the link to get the news id
                        
                        id=storyurls[4]
                        print("main url: ",mainUrl)
                        
                        if(string=="https://www.cloudflare.com/5xx-error-landing?utm_source=iuam"):
                            time.sleep(8)
                        id_string="id-"+id
                        print("id string--------------------------"+id_string)
                        newsElement=driver.find_element_by_id(id_string)#find news article by news id
                        dateElements=newsElement.find_element_by_class_name("timestamp")#get date from news article
                        
                        todaysDate=today.strftime("%B %d, %Y")#todays date
                        
                        dateArray=dateElements.text.split(" ")
                        
                        
                        
                        articleDate=dateArray[1]+" "+dateArray[2]+" "+dateArray[3]#article date
                        
                        print("todays date: "+todaysDate)
                        print("article date: "+articleDate)
                        
                        articleTitle=newsElement.find_element_by_class_name("title")
                        
                        print(articleTitle.text)
                        
                        if todaysDate==articleDate:
                            paragraphs=newsElement.find_elements_by_tag_name("p")
                            
                            paragraphBody=""
                            for para in paragraphs:
                                paragraphBody=paragraphBody+para.text
                                print(para.text)
                            
                            pictureElement=driver.find_element_by_class_name("story-image")
                            imageElement=pictureElement.find_element_by_tag_name("img")
                            imageLink=imageElement.get_attribute("src")
                            response = requests.get(imageLink)
                            currentDirectory = os.getcwd()
                            
                            with open("etImage"+str(k)+'.jpg', 'wb') as out_file:
                                        
                                    out_file.write(response.content)
                            imageDir=currentDirectory+'/'+"etImage"+str(k)+'.jpg'    
                                
                        
                    
                    
                            data={"title":articleTitle.text,re.sub("[\.]", "",mainUrl):paragraphBody,"date":articleDate,"imageDir":imageDir}
                            collection.insert_one(data)
                            print("now next article")
                        
                    except Exception as e:
                        pass
                   
                

