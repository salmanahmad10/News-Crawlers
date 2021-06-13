# -*- coding: utf-8 -*-
"""
Created on Wed Feb 12 16:40:22 2020

@author: salman
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
from selenium.webdriver.support import expected_conditions as EC
import requests
import time
import pymongo
import re
from pymongo import MongoClient
from datetime import date


chrome_options = Options()
chrome_options.add_argument("--incognito")
chrome_options.add_argument("--window-size=1920x1080")
Path=r"C:\Users\salman\desktop\chromedriver\chromedriver.exe"
driver = webdriver.Chrome(options=chrome_options, executable_path=Path)
url="https://www.geo.tv/latest-news"
today = date.today()


class geoC:
    def connect_db():
        client = MongoClient("localhost", 27017)
        return client
    client = connect_db()
    global db
    global collection
    db = client['geoDB']#database creation in mongodb
    collection=db['geoT'] # document creation
    
    global download_images
    global save_image_to_file
    global unvisitedURLs
    unvisitedURLs=db['unvisitedURLs']
    global visitedURLs
    visitedURLs=db['visitedURLs']
    
    def linksCrawl(self):
        
        driver.get(url)
        time.sleep(3)
        
    
            

        try:
           elements = driver.find_elements_by_xpath("//a[@href]")#finding all href in page
       
           for x in elements:
               # print(driver.current_url)        
                string=x.get_attribute("href")#all href links
                
                if(string.startswith("https://www.geo.tv/latest/")):
                    if(db.visitedURLs.find({"urls":string}).count()==0 and db.unvisitedURLs.find({"urls":string}).count()==0 ):
                        data={"urls":string}
                        print(string)
                        unvisitedURLs.insert_one(data)
                else:
                    pass
        except Exception as e:
            pass
            
    
    
   
    
    def crawl(self,url,urlList):
          
        try:   
            documents = urlList
            for k,doc in enumerate( documents,start=0):
                
                    mainUrl=doc["urls"]
                    driver.get(mainUrl)
                    unvisitedURLs.delete_many({"urls":mainUrl})
                    visitedURLs.insert_one({"urls":mainUrl})
                    time.sleep(3)
                    
                    
                    #----------------------------getting date----------------------------
                    try:
                        dateElement=driver.find_element_by_xpath("/html/body/div[2]/section/div/div[3]/div[1]/div[2]")
                        dateElementP=dateElement.find_element_by_tag_name("p").get_attribute("textContent")
                        dateElementProcessed = dateElementP.split("\n")[2]
                        dateArray=dateElementProcessed.split(" ")
                        Articledate=dateArray[1]+" "+dateArray[2]+" "+dateArray[3]
                       
                        
                         #-------------------------------article=date------------------------
                        print("article date: ",Articledate)
                       
                        #--------------------------------todays=date--------------------------
                        todaysDate=today.strftime("%b %d, %Y")
                        print("todays date",todaysDate)
                        if(todaysDate==Articledate):#==============comparison=of=dates================
        #                    
                            storyContent=driver.find_element_by_class_name("story-area")
        #                    #===========================paragraphs===========================
                            paragraphs=storyContent.find_elements_by_tag_name("p")
        #                    
                            paragraphBody=""
                            for para in paragraphs:
                                paragraphBody=paragraphBody+para.text
                                print(para.text)
                             #================================story title====================================
                            titleElement=storyContent.find_element_by_tag_name("h1")
                            title=titleElement.text
                            print("title ",title)
                    
                                
                            #==================================IMAGE=========================================
                    
                            i=0        
                            imgTag=storyContent.find_elements_by_tag_name("img")
                            for img in imgTag:
                                imageLink=img.get_attribute("src")
                                print("image link: ",imageLink)
                                
                                dirname=re.sub("[\.]", "",imageLink)
                                response = requests.get(imageLink)
                                currentDirectory = os.getcwd()
                                i=i+1
                            
                                with open('geoImage'+str(k)+" "+str(i)+'.jpg', 'wb') as out_file:
                                   
                                    out_file.write(response.content)
                                imageDir=currentDirectory+'/'+"geoImage"+str(k)+" "+str(i)+'.jpg'
                            collection.insert_one({"story":paragraphBody,"title":title,"url":mainUrl,"date": Articledate,"imageDir":imageDir})
                        
                    except Exception as e:
                       print(e)
                       unvisitedURLs.delete_many({"urls":mainUrl})
                       visitedURLs.insert_one({"urls":mainUrl})
                       
            driver.close()

        except Exception as e:
            pass
                                  
                                          
                    
            
                             

        


