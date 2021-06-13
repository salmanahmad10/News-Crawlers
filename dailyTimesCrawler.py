# -*- coding: utf-8 -*-
"""
Created on Sat Feb 22 14:38:47 2020

"""
import selenium 
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import os
from os import path
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import StaleElementReferenceException
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.expected_conditions import presence_of_element_located
import time
import pymongo
import requests
from pymongo import MongoClient
from datetime import date
import datetime

chrome_options = Options()
chrome_options.add_argument("--incognito")
chrome_options.add_argument("--window-size=1920x1080")
Path=r"C:\Users\salman\Desktop\chromedriver\chromedriver.exe"
driver = webdriver.Chrome(options=chrome_options, executable_path=Path)
driver.maximize_window()
url="https://dailytimes.com.pk/"
today = date.today()

class dailyTimesT:
    def connect_db():
        client = MongoClient("localhost", 27017)
        return client
    
    client = connect_db()
    global db
    global collection
    db = client['dailyTimesDB']#database creation in mongodb
    collection=db['dailyTimesT'] # document creation
    global catagories
    catagories=["https://dailytimes.com.pk/pakistan/","https://dailytimes.com.pk/world/","https://dailytimes.com.pk/business/",
                "https://dailytimes.com.pk/sports/","https://dailytimes.com.pk/dtculture/"]
   
    global unvisitedURLs
    unvisitedURLs=db['unvisitedURLs']
    global visitedURLs
    visitedURLs=db['visitedURLs']
    global catagoriesURLs 
    catagoriesURLs=db['catagoriesURLs']  
    global catagoriesURLS
    def catagoriesURLS(self):
                
        for x in range(len(catagories)):
            if(db.visitedURLs.find({"urls":catagories[x]}).count()==0 and db.unvisitedURLs.find({"urls":catagories[x]}).count()==0):
                    catagoriesURLs.insert_one({"urls":catagories[x]})
                     
                                        
# =============================================================================
#                ARTICLES LINKS STARTS GETTING CRWALED     
# =============================================================================                      
                                
    def crawlLinks(self):
        catagoriesURLS(self)
        documents = list(catagoriesURLs.find())
        for doc in documents:
                try:
                    mainUrl=doc["urls"]
                    driver.get(mainUrl)
                    unvisitedURLs.delete_many({"urls":mainUrl})
                    visitedURLs.insert_one({"urls":mainUrl})
                    time.sleep(3)
                    global nextPageCheck
                    nextPageCheck=False
                    todaysDate='{dt:%B} {dt.day}, {dt.year}'.format(dt=datetime.datetime.now())
                    
                    todaysDate=todaysDate.upper()
                    
                   
                  
                       
                    postElement=driver.find_elements_by_class_name("post")
                    for posts in postElement:
                        dateElement=posts.find_element_by_class_name("entry-time")
                        postUrlElement=posts.find_element_by_class_name("entry-title-link")
                        postUrl=postUrlElement.get_attribute("href")
                        print (postUrl)
                        print("todaysDate===>",todaysDate)
                        print("article date:---",dateElement.text)
                        if(dateElement.text==todaysDate): 
                            if(db.visitedURLs.find({"urls":postUrl}).count()==0 and db.unvisitedURLs.find({"urls":postUrl}).count()==0 ):
                                data={"urls":postUrl}
                                print(postUrl)
                                unvisitedURLs.insert_one(data)
                            
                            
                        else:
                            print("==============next catagory=================")
                            
                            pass      
                except Exception as e:
                    pass
        
                    
               
                    
# =============================================================================
# ARTICLES LINKS STOPS GETTING CRAWLED
# ============================================================================
   
    def crawl(self,url,urlList):
              
        try:
            documents = urlList
            for k,doc in enumerate( documents,start=0):
                    mainUrl=doc["urls"]
                    driver.get(mainUrl)
                    unvisitedURLs.delete_many({"urls":mainUrl})
                    if(db.visitedURLs.find({"urls":mainUrl}).count()==0):
                        visitedURLs.insert_one({"urls":mainUrl})
                    time.sleep(3)
                    artileElement=driver.find_element_by_class_name("site-container-wrap")
                
                    print("article url: ",mainUrl)
    # =============================================================================
    #                 title
    # =============================================================================
                    titleElement=artileElement.find_element_by_class_name("entry-title")
                    title=titleElement.text
                    print("title===============",title)
    # =============================================================================
    #                 date
    # =============================================================================
                    dateElement=artileElement.find_element_by_class_name("entry-time")
                    date=dateElement.text
                    print("================date",date)
                    
    # =============================================================================
    #                 paragraphs
    # =============================================================================
                    paragraphBody=""
                    paragraphElement=artileElement.find_elements_by_class_name("entry-content")
                    
                    for para in paragraphElement:
                        print(para.text)
                        paragraphBody+=para.text
                        
                        
    # =============================================================================
    #                image
    # =============================================================================
                    try:
                        # imageElement=driver.find_element_by_class_name("lazyloaded")
                        # imageLink=imageElement.get_attribute("src")
                        # print("image link: =-===",imageLink)
                        imageElement=driver.find_element_by_class_name("post")
                        images=imageElement.find_elements_by_tag_name("img")
                        i=0
                        for img in images:
                            imageLink=img.get_attribute("src")
                            response = requests.get(imageLink)
                            currentDirectory = os.getcwd()
                            
                            with open("dailyTimesImage"+str(k)+" "+str(i)+'.jpg', 'wb') as out_file:
                                        
                                    out_file.write(response.content)
                                    i=i+1
                            imageDir=currentDirectory+'/'+"dailyTimesImage"+str(k)+" "+str(i)+'.jpg'
                            
                        collection.insert_one({"story":paragraphBody,"title":title,"url":mainUrl,"date": date,"currentDir":imageDir})
                    except Exception as e:
                        print(e)
                        pass
    
        except Exception as e :
            print(e)
            pass                
        
                
                
                
                
                
                




