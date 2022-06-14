import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import requests , json ,firebase_admin ,zlib,datetime
from firebase_admin import credentials ,firestore

options = webdriver.ChromeOptions()
# options.add_argument("--start-maximized")
options.add_argument("--headless")#incognito headless
options.add_argument("--disable-popup-blocking ")
options.add_argument('--window-size=1920,1080')
options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.5005.115 Safari/537.36")

today = datetime.datetime.now(tz=datetime.timezone(datetime.timedelta(hours=8)))
cred = credentials.Certificate('testkey.json')
firebase_admin.initialize_app(cred)
db = firestore.client()
collection_ref = db.collection("test")

driver = webdriver.Chrome(options = options)
nd = webdriver.Chrome(options = options) 
url = "https://www.accuweather.com/zh/tw/taiwan-weather"
driver.get(url)
time.sleep(5)
doc_ref = db.collection("test").document("whe")
msg = ""
for i in driver.find_elements_by_xpath("/html/body/div/div[4]/div[1]/div/div[2]/div/a"):
    if i.find_element_by_class_name("text.title.no-wrap").text[2:] in ["市","縣"]:
        area = i.find_element_by_class_name("text.title.no-wrap").text
        whurl = i.get_attribute("href")
        nd.get(whurl)
        nurl = nd.find_element_by_xpath("/html/body/div/div[3]/div/div[3]/a[2]").get_attribute("href")
        nd.get(nurl)
        time.sleep(2)
        msg += area + "\n"
        for k in nd.find_elements_by_xpath("/html/body/div/div[5]/div[1]/div[1]"):
            elnnum = len(nd.find_elements_by_class_name("accordion-item.hourly-card-nfl.hour.non-ad"))
            for s in range(1,elnnum):
                k.find_element_by_id("hourlyCard" + str(s)).click()
                time.sleep(0.2)
            for a in k.find_elements_by_xpath("//*/div[1]/div/div[1]/h2/span"):
                print(a.text) 
            for b in k.find_elements_by_class_name("phrase"):
                print(b.text) 
            for c in k.find_elements_by_class_name("temp.metric"):
                print(c.text) 
code = zlib.compress(str(msg).encode("utf-8"))
doc_ref.update({str(today.date()) : code})
quit()