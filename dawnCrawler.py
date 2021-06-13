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
Path=r"C:\Users\salman\desktop\chromedriver\chromedriver.exe"
driver = webdriver.Chrome(options=chrome_options, executable_path=Path)
url = "https://www.dawn.com/latest-news"
today = date.today()



class dawnT:
    def connect_db():
        client = MongoClient("localhost", 27017)
        return client
    
    client = connect_db()
    global db
    global collection
    db = client['dawnDB']#database creation in mongodb
    collection=db['dawnT'] # document creation
    global unvisitedURLs
    unvisitedURLs=db['unvisitedURLs']
    global visitedURLs
    visitedURLs=db['visitedURLs']
    
            
# =============================================================================
#             articles links getting crawled
# =============================================================================
    def crawlLinks(self):
        driver.get(url)
        time.sleep(3)
        
        
        
        try:
            boxElements=driver.find_elements_by_class_name("box")
            for x in boxElements:
                hrefElement = x.find_element_by_class_name("story__link")#finding all href in page
                dateElement=  x.find_element_by_class_name("timestamp--time")
             
                string=hrefElement.get_attribute("href")#all href links
                date=dateElement.get_attribute("title")
                print("string: ", string)
               
                dateArray=date.split(" ")
                finalDate=dateArray[0]+" "+dateArray[1]+" "+dateArray[2]
                print("date", finalDate)
            
                todaysDate=today.strftime("%b %d, %Y")
                print("todays date",todaysDate)
            

                if(string.startswith("https://www.dawn.com/news/") and todaysDate==finalDate):
                    if(db.visitedURLs.find({"urls":string}).count()==0 and db.unvisitedURLs.find({"urls":string}).count()==0 ):
                        data={"urls":string,"date":finalDate}
                        unvisitedURLs.insert_one(data)
        except Exception as e:
            pass
# =============================================================================
#     article links stops getting crawled
# =============================================================================
    def crawl(self,url,urlList):
        
        try:
            documents = urlList
            for k,doc in enumerate( documents,start=0):
                 mainUrl=doc["urls"]
                 if mainUrl.startswith("https://www.dawn.com/news/"):#if main url starts wuth this then fetch all links from it
                            driver.get(mainUrl)
                            unvisitedURLs.delete_many({"urls":mainUrl})
                            visitedURLs.insert_one({"urls":mainUrl})
                            time.sleep(3)
                            newsElement=driver.find_element_by_class_name("story__content")
                            paragraphs=newsElement.find_elements_by_tag_name("p")
                            paragraphBody=""
                            print("-------------------------story content------------------------")
                                
                            #-----------------------story title------------------------
                            titleElement=driver.find_element_by_class_name("story__link")
                            title=titleElement.text
                            print("title: ",title)
                            
                            #------------------------url--------------------------------
                            print("url: ",mainUrl)
                            
                            #-----------------------date--------------------------------
                            date=doc["date"]
                            print("date: ",date)
                            
                            #-------------------------paragraph creation-------------------
                            for para in paragraphs:
                                paragraphBody=paragraphBody+para.text
                                print(para.text)
                                
                            # =============================================================================
                            #                image
                            # =============================================================================
                            pictureElement=driver.find_element_by_class_name("media__item          ")
                            imageElement=pictureElement.find_element_by_tag_name("img")
                            imageLink=imageElement.get_attribute("src")
                            response = requests.get(imageLink)
                            currentDirectory = os.getcwd()
                            
                            with open("dawnImage"+str(k)+'.jpg', 'wb') as out_file:
                                        
                                    out_file.write(response.content)
                            imageDir=currentDirectory+'/'+"dawnImage"+str(k)+'.jpg'    
                                    
                                
                            
                            print("-------------------------story ends------------------------")
                            
                            collection.insert_one({"story":paragraphBody,"title":title,"url":mainUrl,"date": date,"imageDir":imageDir})

            driver.close()                    
        except Exception as e:
            pass
        



