from selenium import webdriver
from selenium.webdriver.common.by import By
import pickle
import time
from selenium import webdriver 
from selenium.webdriver.chrome.service import Service as ChromeService 
from webdriver_manager.chrome import ChromeDriverManager 
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup 
from selenium.webdriver.chrome.options import Options
from time import sleep
from flask import Flask
import os
import json
import sqlite3



app=Flask(__name__)

def load_cookies_and_access_instagram(chance,cookie_file=r"./instagram_cookies.pkl"):
    basedir = os.path.abspath(os.path.dirname(__file__))

    # Construct the full path to the file
    file_path = os.path.join(basedir, 'backend', 'data.db')
    driver = webdriver.Chrome()

    driver.get("https://www.instagram.com/")
    time.sleep(3)

    # Load cookies from file
    conn = sqlite3.connect(file_path)
    cursor = conn.cursor()
    cursor.execute('SELECT data FROM DataStore WHERE id = ?', (1,))
    data_json = cursor.fetchone()[0]
    conn.close()

    # Convert the JSON string back to Python data structure
    cookies = json.loads(data_json)   
    for cookie in cookies:
        driver.add_cookie(cookie)

    # Refresh the page to apply cookies
    driver.refresh()
    time.sleep(3)

    # Now you are logged in and can navigate to any Instagram page

    # Example: Go to a specific post
    second_url="https://www.instagram.com/reels/C6JqeVyvhu5/"
    driver.get(second_url)
    time.sleep(3)

    # Example: Extract comments
    comment_icon=WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, '.x6s0dn4.x78zum5.xdt5ytf.xl56j7k')))
    driver.execute_script('document.querySelectorAll(".x6s0dn4.x78zum5.xdt5ytf.xl56j7k")[2].click()')
    sleep(3)
    count=0
    def generating_comments():
            nonlocal count
            comments_username_list=[]
            comments_username=driver.execute_script('return document.querySelectorAll("._ap3a._aaco._aacw._aacx._aad7._aade")')
            last_top=None
            while (True):
                scrolable_element=driver.execute_script("return document.querySelector('.x9f619.xjbqb8w.x78zum5.x168nmei.x13lgxp2.x5pf9jr.xo71vjh.xqmdsaz.x1xfsgkm.x1uhb9sk.xw2csxc.x1odjw0f.x1iyjqo2.x2lwn1j.xeuugli.xdt5ytf.xqjyukv.x1qjc9v5.x1oa3qoh.x1nhvcw1').scrollHeight")# get the total height in current batch
                scrolable_element1=driver.execute_script("return document.querySelector('.x9f619.xjbqb8w.x78zum5.x168nmei.x13lgxp2.x5pf9jr.xo71vjh.xqmdsaz.x1xfsgkm.x1uhb9sk.xw2csxc.x1odjw0f.x1iyjqo2.x2lwn1j.xeuugli.xdt5ytf.xqjyukv.x1qjc9v5.x1oa3qoh.x1nhvcw1').scrollTop")#get the position of scroll bar

                scrollHeight=scrolable_element
                scrollTop=scrolable_element1
                print(scrollTop,scrollHeight)
                if scrollTop==last_top: #used to stop scroll
                    count+=1
                    print("out")
                    if count==chance:
                        break
                last_top=scrollTop

                driver.execute_script(f"document.querySelector('.x9f619.xjbqb8w.x78zum5.x168nmei.x13lgxp2.x5pf9jr.xo71vjh.xqmdsaz.x1xfsgkm.x1uhb9sk.xw2csxc.x1odjw0f.x1iyjqo2.x2lwn1j.xeuugli.xdt5ytf.xqjyukv.x1qjc9v5.x1oa3qoh.x1nhvcw1').scroll(0,{scrollHeight})")
                sleep(3)

    generating_comments()
    comments=driver.execute_script("return document.querySelectorAll('.x1lliihq.x1plvlek.xryxfnj.x1n2onr6.x193iq5w.xeuugli.x1fj9vlw.x13faqbe.x1vvkbs.x1s928wv.xhkezso.x1gmr53x.x1cpjm7i.x1fgarty.x1943h6x.x1i0vuye.xvs91rp.xo1l8bm.x5n08af.x10wh9bi.x1wdrske.x8viiok.x18hxmgj')")#will return both username and comment for each user
    for index,i in enumerate(comments):
        if index%2==0:
            print("Username",i.text,end=' ')

        if index%2==1:
            print("Comment:",i.text)

        
    print(len(comments)//2)
    return comments
@app.route("/",methods=['GET'])
def call():
    comments = load_cookies_and_access_instagram(3)
    print(comments)




# Use this function to load cookies and access Instagram

if __name__ == "__main__":
    port = int(os.getenv('PORT', 4000))
    app.run(debug=True,port=port,host='0.0.0.0')
    