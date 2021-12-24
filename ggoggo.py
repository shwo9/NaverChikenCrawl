from selenium import webdriver
import time 
import json
import os
import pandas as pd
import requests
from bs4 import BeautifulSoup

Chrome_Driver = "/Users/hwsung/Desktop/crawl/chromedriver" ## 크롬드라이버 경로
now_dirname = os.path.dirname(os.path.abspath(__file__))

## 크롬드라이버 셋팅
options = webdriver.ChromeOptions()
options.add_experimental_option('excludeSwitches', ['enable-logging'])
options.add_argument('window-size=1920x1080')
options.add_argument('headless')
options.add_argument("disable-gpu")
options.add_argument("lang=ko-KR")
options.add_argument("user-agent=Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; rv:11.0) like Gecko")
driver = webdriver.Chrome(Chrome_Driver, options=options)

driver.get("https://map.naver.com/v5/")
time.sleep(0.2)

res = requests.get("https://map.naver.com/v5/api/search?caller=pcweb&query=치킨&type=all&searchCoord=126.8836333;37.4583306&page=1&displayCount=20&isPlaceRecommendationReplace=true&lang=ko").text

res = json.loads(res)

data = res['result']['place']['list']

storeID = []
storeName = []
storePhone = []
storeAddr = []
storeImg = []
storePosX = []
storePosY = []
storeMenu = []

for i in data :
    storeID.append(i['id'])
    storeName.append(i['name'])
    storePhone.append(i['tel'])
    storeAddr.append(i['roadAddress'])
    storeImg.append(i['thumUrl'])
    storePosX.append(i['x'])
    storePosY.append(i['y'])
    storeMenu.append(i['menuInfo'])

list = list(zip(
    storeID,
    storeName,
    storePhone,
    storeAddr,
    storeImg,
    storePosX,
    storePosY,
    storeMenu
    ))
list = pd.DataFrame(list)
list.to_excel('list.xlsx')
print(list)
