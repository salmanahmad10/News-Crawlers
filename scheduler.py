
from apscheduler.schedulers.blocking import BlockingScheduler
import threading
from pymongo import MongoClient
import concurrent.futures
import queue
from multiprocessing import pool
geoUrl="https://www.geo.tv/latest-news"
aryurl="https://arynews.tv/en/latest-news/"
dailyTimesurl="https://dailytimes.com.pk/"
dawnurl="https://www.dawn.com/latest-news"
eturl="https://tribune.com.pk/"
sammaurl="https://www.samaa.tv/latestnews/"
from priorityQueue import PriorityQueue
from controller import newsCrawlersPriority
from concurrent.futures import ThreadPoolExecutor

def connect_db():
    client = MongoClient("localhost", 27017)
    return client
    
client = connect_db()
linksThreadCheck=[None]*6



#=====================================================================
#   assigning pririty
#=====================================================================
# myQueue = PriorityQueue()
# newsCrawlersP=newsCrawlersPriority() 
# myQueue.insert(newsCrawlersP.ary) 
# #myQueue.insert(newsCrawlersP.expressTribune) 
# myQueue.insert(newsCrawlersP.dawn) 
# myQueue.insert(newsCrawlersP.geo) 
# myQueue.insert(newsCrawlersP.dailyNews) 

#return values of link fetching threads
global dawnThreadReturn
dawnThreadReturn=[]

global aryThreadReturn
aryThreadReturn=[]

global geoThreadReturn
geoThreadReturn=[]

global samaaThreadReturn
samaaThreadReturn=[]

global dailyTimesThreadReturn
dailyTimesThreadReturn=[]

global etThreadReturn
etThreadReturn=[]


#====================================================================
#           THREAD 1
#====================================================================

def dawnThread():
    from dawnCrawler import dawnT
    dawnCrawler = dawnT()
    dawnCrawler.crawlLinks()

    db = client['dawnDB']#database creation in mongodb
    unvisitedURLs=db['unvisitedURLs']
    documents = list(unvisitedURLs.find())

    dawnThreadCheck=True
    dawnUrlList=documents

    dawnThreadReturn.insert(0,dawnThreadCheck)
    dawnThreadReturn.insert(1,dawnUrlList)

    

    

   





#====================================================================
#           THREAD 2
#====================================================================

def geoThread():
    from geoCrawler import geoC
    geoCrawler = geoC()
    geoCrawler.linksCrawl()
    db = client['geoDB']#database creation in mongodb
    unvisitedURLs=db['unvisitedURLs']
    documents = list(unvisitedURLs.find())

    geoThreadCheck=True
    geoUrlList=documents

    geoThreadReturn.insert(0,geoThreadCheck)
    geoThreadReturn.insert(1,geoUrlList)



    

#====================================================================
#           THREAD 3
#====================================================================

def aryThread():
    from arycrawler import aryC
    aryCrawler = aryC()
    aryCrawler.linksCrawl()
    db = client['aryDB']#database creation in mongodb
    unvisitedURLs=db['unvisitedURLs']
    documents = list(unvisitedURLs.find())

    aryThreadCheck=True
    aryUrlList=documents

    aryThreadReturn.insert(0,aryThreadCheck)
    aryThreadReturn.insert(1,aryUrlList)

#====================================================================
#           THREAD 4
#====================================================================

def samaaThread():
    try:
        from sammaCrawler import samaaC
        sammaCrawler = samaaC()
        sammaCrawler.crawlLinks()
        db = client['samaaDB']#database creation in mongodb
        unvisitedURLs=db['unvisitedURLs']
        documents = list(unvisitedURLs.find())

        samaaThreadCheck=True
        samaaUrlList=documents

        samaaThreadReturn.insert(0,samaaThreadCheck)
        samaaThreadReturn.insert(1,samaaUrlList)
    except Exception as e:
        samaaThread()
    

#====================================================================
#           THREAD 5
#====================================================================

def dailytimes():
    try:
        from dailyTimesCrawler import dailyTimesT
        dailtTimesCrawler = dailyTimesT().crawlLinks()
        db = client['dailyTimesDB']#database creation in mongodb
        unvisitedURLs=db['unvisitedURLs']
        documents = list(unvisitedURLs.find())
        
        dailyTimesThreadCheck=True
        dailyTimesUrlList=documents

        dailyTimesThreadReturn.insert(0,dailyTimesThreadCheck)
        dailyTimesThreadReturn.insert(1,dailyTimesUrlList)
        
    except Exception as e:
        print(e)

#====================================================================
#           THREAD 6
#====================================================================

def expressT():
    try:
        from etCrawler import expressT
        etCrawler = expressT().crawlLinks()
        
        db = client['expressDB']#database creation in mongodb
        catagoriesT=db['catagoriesT']
        documents = list(catagoriesT.find())
        
        expressTThreadCheck=True
        expressTUrlList=documents

        etThreadReturn.insert(0,expressTThreadCheck)
        etThreadReturn.insert(1,expressTUrlList)
        
    except Exception as e:
        print(e)


dailyTimesThreadFree='dailyTimesThread'
dawnThreadFree='dawnThread'
aryThreadFree='aryThread'
geoThreadFree='geoThread'
samaaThreadFree='samaaThread'
expressTThreadFree='expressT'                   
freeThreads=[dailyTimesThreadFree,dawnThreadFree,geoThreadFree,samaaThreadFree,aryThreadFree,expressTThreadFree]

def ThreadController():
    if(len(freeThreads)>0):
        print(freeThreads)     



def dawnNewsCrawl(dawnList):
    print("==============dawnNewsCrawl crawl===================")
    freeThreads.remove(dawnThreadFree)
    from dawnCrawler import dawnT
    dawnCrawler = dawnT()
    dawnCrawler.crawl(dawnurl,dawnList)#passingnews link and dawn urlList to crawl
    freeThreads.append(dawnThreadFree)
    print ('dawn thread free')
    ThreadController()
    return True


def aryNewsCrawl(aryList):
    print("==============aryNewsCrawl crawl===================")
    freeThreads.remove(aryThreadFree)
    from arycrawler import aryC
    arycrawler = aryC()
    arycrawler.crawl(aryurl,aryList)#passingnews link and dawn urlList to crawl
    freeThreads.append(aryThreadFree)
    print('ary thread free')
    ThreadController()
    return True




def geoNewsCrawl(geoList):
    print("==============geoNewsCrawl crawl===================")
    freeThreads.remove(geoThreadFree)
    from geoCrawler import geoC
    geoCrawler = geoC()
    geoCrawler.crawl(geoUrl,geoList)#passingnews link and dawn urlList to crawl
    freeThreads.append(geoThreadFree)
    print("geo thread free")
    ThreadController()
    return True

def samaaNewsCrawl(samaaList):
    print("==============samaaNewsCrawl crawl===================")
    freeThreads.remove(samaaThreadFree)
    from sammaCrawler import samaaC
    samaaCrawler = samaaC()
    samaaCrawler.crawl(sammaurl,samaaList)#passingnews link and dawn urlList to crawl
    freeThreads.append(samaaThreadFree)
    print("samaa thread free")
    ThreadController()
    return True

def dailyTimesNewsCrawl(dailyTimesList):
    print("==============dailyTimesNewsCrawl crawl===================")
    freeThreads.remove(dailyTimesThreadFree)
    from dailyTimesCrawler import dailyTimesT
    dailyTimesCrawler=dailyTimesT()
    dailyTimesCrawler.crawl(dailyTimesurl,dailyTimesList)
    freeThreads.append(dailyTimesThreadFree)
    print("daily times thread free")
    ThreadController()
    #passingnews link and dawn urlList to crawl
    return True


def expressTNewsCrawl(expressTList):
    print("==============expressTNewsCrawl crawl===================")
    freeThreads.remove(expressTThreadFree)
    from etCrawler import expressT
    etCrawler = expressT()
    etCrawler.crawl(eturl,expressTList)
    freeThreads.append(expressTThreadFree)
    print("et times thread free")
    ThreadController()
    #passingnews link and dawn urlList to crawl
    return True




#links crawl
t1 = threading.Thread(target=dawnThread)
t2 = threading.Thread(target=geoThread)
t3 = threading.Thread(target=aryThread)
t4 = threading.Thread(target=samaaThread)
t5 = threading.Thread(target=dailytimes)
t6 = threading.Thread(target=expressT)


#contentCrawl

t1.start()
t2.start()
t3.start()
t4.start()
t5.start()
#t6.start()


t1.join()
t2.join()
t3.join()
t4.join()
t5.join()
#t6.join()



 

if(dawnThreadReturn[0]==True and geoThreadReturn[0]==True and aryThreadReturn[0]==True and samaaThreadReturn[0]==True and dailyTimesThreadReturn[0]==True):
#if(etThreadReturn[0]==True):
    print("crawling starts")
    t6 = threading.Thread(target=dawnNewsCrawl,args=(dawnThreadReturn[1],))
    t7 = threading.Thread(target=geoNewsCrawl,args=(geoThreadReturn[1],))
    t8 = threading.Thread(target=aryNewsCrawl,args=(aryThreadReturn[1],))
    t9 = threading.Thread(target=samaaNewsCrawl,args=(samaaThreadReturn[1],))
    t10 = threading.Thread(target=dailyTimesNewsCrawl,args=(dailyTimesThreadReturn[1],))
    #t11 = threading.Thread(target=expressTNewsCrawl,args=(etThreadReturn[1],))
    t12 = threading.Thread(target=ThreadController)


            
    t12.start()
    t6.start()
    t7.start()
    if(t6.is_alive() and  t7.is_alive()):
        t6.join()
        t7.join()
    t8.start()
    t9.start()
    if(t8.is_alive() and  t9.is_alive()):
        t8.join()
        t9.join()
    t10.start()
    if(t10.is_alive()):
        t10.join()
        
    t12.join()

    # t11.start()
    # t11.join()
        



             

 
