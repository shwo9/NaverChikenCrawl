from selenium import webdriver
import time 
import json
import os
import pandas as pd
import requests
import urllib
from urllib.parse import urlparse
from selenium.webdriver.firefox.options import Options
from fake_useragent import UserAgent


# ## 파이어폭스 셋팅
# options = Options()
# profile = webdriver.FirefoxProfile()
# #profile.set_preference('general.useragent.override', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:65.0) Gecko/20100101 Firefox/65.0')
# profile.set_preference("network.proxy.type", 1)
# profile.set_preference("network.proxy.socks", "127.0.0.1")
# profile.set_preference("network.proxy.socks_port", 9050)
# options.headless = True
# profile.update_preferences()
# FP_path = "/Users/hwsung/Desktop/crawl/ggoggo/geckodriver"
# driver = webdriver.Firefox(profile, options=options, executable_path=FP_path)

## 크롬드라이버 셋팅
Chrome_Driver = "/Users/hwsung/Desktop/crawl/chromedriver" ## 크롬드라이버 경로
now_dirname = os.path.dirname(os.path.abspath(__file__))
options = webdriver.ChromeOptions()
options.add_experimental_option('excludeSwitches', ['enable-logging'])
options.add_argument('window-size=1920x1080')
options.add_argument('headless')
options.add_argument("disable-gpu")
options.add_argument("lang=ko-KR")
#options.add_argument("--proxy-server=socks5://127.0.0.1:9050")
options.add_argument("user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36")
driver = webdriver.Chrome(Chrome_Driver, options=options)

        
## 서울 행정동 불러오기
df = pd.read_excel('서울행정동2.xlsx')
dong_list = df.values.tolist()

storeID = []
storeName = []
storePhone = []
storeAddr = []
storeImg = []
storePosX = []
storePosY = []
storeMenu = []
storeReview = []
cnt = 1

def DelEmoji(inputData):
    return inputData.encode('utf-8', 'ignore').decode('utf-8')

driver.get('https://map.naver.com/v5/')
time.sleep(3)


ua = UserAgent()
for dong in dong_list:
    headers = {
        'Referer': 'https://map.naver.com/',
        'User-Agent': str(ua.random),
        #'User-Agent' : 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36',
        'accept' : "*/*",
        'accept-encoding' : 'gzip, deflate, br',
        'accept-language': 'ko-KR,ko;q=0.8,en-US;q=0.6,en;q=0.4',
        #'cookie' : 'NNB=LLNUYSXZ4PCWC; BMR=s=1640522049791&r=https://news.naver.com/&r2=https://www.naver.com/; page_uid=7a2d34d7-890d-41ee-8e1d-b448d3ae4771',
        }
    #driver.get("https://map.naver.com/v5/search/"+urllib.parse.quote(dong[0]))
    #time.sleep(0.2)
    url = "https://map.naver.com/v5/api/search?caller=pcweb&query=%EC%B9%98%ED%82%A8&type=all&searchCoord=" + str(dong[2]) + ';' + str(dong[1]) + "&page=1&displayCount=20&isPlaceRecommendationReplace=true&lang=ko"
    res = DelEmoji(requests.get(url, headers = headers).text)
    try :
        res = json.loads(res)
        data = res['result']['place']['list']
    except:
        print(requests.get(url, headers = headers))

    if data :
        for i in data :
            storeID.append(i['id'])
            storeName.append(i['name'])
            storePhone.append(i['tel'])
            storeAddr.append(i['roadAddress'])
            storeImg.append(i['thumUrl'])
            storePosX.append(i['x'])
            storePosY.append(i['y'])
            storeMenu.append(i['menuInfo']),
            storeReview.append(i['reviewCount'])
    else : break
    print(urllib.parse.unquote(dong[0]) + ' 수집 완료....', cnt ,'/' , len(dong_list))
    cnt += 1

list = list(zip(
    storeID,
    storeName,
    storePhone,
    storeAddr,
    storeImg,
    storePosX,
    storePosY,
    storeMenu,
    storeReview
    ))
list = pd.DataFrame(list)
list.to_excel('list.xlsx')
print(list)
