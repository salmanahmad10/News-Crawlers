# -*- coding: utf-8 -*-
"""
Created on Fri Feb 14 13:06:56 2020

@author: salman
"""
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
import datetime
from selenium.webdriver.common.keys import Keys


chrome_options = Options()
chrome_options.add_argument("--incognito")
chrome_options.add_argument("--window-size=1920x1080")
Path=r"C:\Users\salman\Desktop\chromedriver\chromedriver.exe"
driver = webdriver.Chrome(options=chrome_options, executable_path=Path)
driver.maximize_window()
url="https://arynews.tv/en/latest-news/"
today = date.today()


class aryC:
    try:    
            def connect_db():
                client = MongoClient("localhost", 27017)
                return client
            client = connect_db()
            global db
            global collection
            db = client['aryDB']#database creation in mongodb
            collection=db['aryT'] # document creation
            global unvisitedURLs
            unvisitedURLs=db['unvisitedURLs']
            global visitedURLs
            visitedURLs=db['visitedURLs']
          
            
            
            
            
            global __scroll_down_page
            def scroll_down_page(self,driver):
               speed=18
               current_scroll_position, new_height= 0, 1
               while current_scroll_position <= new_height:
                    current_scroll_position += speed
                    driver.execute_script("window.scrollTo(0, {});".format(current_scroll_position))
                    new_height = driver.execute_script("return document.body.scrollHeight")
              # =============================================================================
              #        LINKS STARTS CRAWLING
              # =============================================================================      
                
            def linksCrawl(self):
               
                try:
        
                    driver.get(url)
                    driver.refresh()
                except requests.exceptions.ConnectionError:
                    pass
                
                time.sleep(3)
                    # =============================================================================
                    # scrolling latest page to load all articles
                    # =============================================================================
        
                while(1):
                    try:
                        time.sleep(3)
                        self.scroll_down_page(driver)
                        driver.find_element_by_class_name("btn-bs-pagination").click()
                    except NoSuchElementException:
                        break
                    
                try:
                   elements = driver.find_elements_by_xpath("//a[@href]")#finding all href in page
                  
                   for x in elements:
                       # print(driver.current_url)        
                        string=x.get_attribute("href")#all href links
                        
                        if(string.startswith("https://arynews.tv/en")):
                            if(db.visitedURLs.find({"urls":string}).count()==0 and db.unvisitedURLs.find({"urls":string}).count()==0 ):
                                data={"urls":string}
                                print(string)
                                unvisitedURLs.insert_one(data)
                        else:
                            pass
                except Exception as e:
                    pass
             
                
                        
        # =============================================================================
        #     LINKS FINISH CRAWLING
        # =============================================================================
                
            
            def crawl(self,url,urlList):
        
        
                
                documents = urlList
                for k,doc in enumerate( documents,start=0):
                        mainUrl=doc["urls"]
                        try:
                                driver.get(mainUrl)
                        except requests.exceptions.ConnectionError:
                                pass
                        
                        unvisitedURLs.delete_many({"urls":mainUrl})
                        visitedURLs.insert_one({"urls":mainUrl})
                        time.sleep(3)
                        
                        
        # =============================================================================
        #                 #----------------------------getting date--------------------
        # =============================================================================
                        try:
                            dateElement=driver.find_element_by_class_name("post-published")
                            dateElementP=dateElement.find_element_by_tag_name("b").get_attribute("textContent")
                            dateArray=dateElementP.split(" ")
                            Articledate=dateArray[0]+" "+dateArray[1]+" "+dateArray[2]
                           
                            
                            # =============================================================================
                            #                      #-------------------------------article=date------------------------
                            # =============================================================================
                            print("article date: ",Articledate)
                           
                            # =============================================================================
                            #                     #--------------------------------todays=date--------------------------
                            # =============================================================================
                            todaysDate='{dt:%b} {dt.day}, {dt.year}'.format(dt=datetime.datetime.now())
                            print("todays date",todaysDate)
                            if(todaysDate==Articledate):#==============comparison=of=dates================
                            
                                storyContent=driver.find_element_by_class_name("single-container")
                          #===========================paragraphs===========================
                                paragraphs=storyContent.find_elements_by_tag_name("p")
                            
                                paragraphBody=""
                                for para in paragraphs:
                                    paragraphBody=paragraphBody+para.text
                                    print(para.text)
        #                         #================================story title====================================
                                titleElement=driver.find_element_by_class_name("post-title")
                                title=titleElement.text
                                print("title ",title)
        #                
                                # =============================================================================
                                #==================================IMAGE=======================================
                                # =============================================================================
                                i=0
                                image=storyContent.find_elements_by_tag_name("img")
                                for img in image:
                                    imageLink=img.get_attribute("src")
                                    print("image link: ",imageLink)
                                    
                                    
                                    response = requests.get(imageLink)
                                    currentDirectory = os.getcwd()
                                    i=i+1
                                    with open("aryImage"+str(k)+" "+str(i)+'.jpg', 'wb') as out_file:
                                       
                                        out_file.write(response.content)
                                    imageDir=currentDirectory+'/'+"aryImage"+str(k)+" "+str(i)+'.jpg'
                                collection.insert_one({"story":paragraphBody,"title":title,"url":mainUrl,"date": Articledate,"currentDir":imageDir})
           
                        
                        except Exception as e:
                           print("not available")
                           pass
                   
                driver.close()        
                                  
    except Exception as e:
            pass
                             


