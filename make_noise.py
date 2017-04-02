#necassary imports
import os, sys
import json
import urllib2
import platform
import time
from random import randint
from selenium import webdriver

#initializing drivers
print("Starting drivers ... ")

# chrome/chromedriver doesn't support RPi
if 'raspberrypi' in platform.uname() or 'armv7l' == platform.machine():
    if not os.getenv('DISPLAY'):
        print("make sure to start a virtual display:")
        print("Xvfb :99 -ac &")
        print("export DISPLAY=:99")
        sys.exit(1)

    from selenium.webdriver.firefox.options import Options
    firefox_options = Options()
    firefox_options.add_argument("--headless")
    firefox_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36")

    p = os.getcwd() + '/geckodriver_arm7'
    driver = webdriver.Firefox(executable_path=p, firefox_options=firefox_options)

else:
    #setting up driver to simulate user and also start chrome in background
    from selenium.webdriver.chrome.options import Options
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36")

    #choosing chrome driver based on OS
    if 'Linux' in (platform.system()):
        driver = webdriver.Chrome(os.getcwd()+'/chromedriver_linux',chrome_options=chrome_options)
    elif 'Windows' in (platform.system()):
        driver = webdriver.Chrome(os.getcwd()+'/chromedriver.exe',chrome_options=chrome_options)
    elif 'Darwin' in (platform.system()):
        driver = webdriver.Chrome(os.getcwd()+'/chromedriver_mac',chrome_options=chrome_options)


#starting pynoise..
print "Generating some random trafific...."

#asking user for input on which sites they browse so pynoise can do a better job contaminating data
print '''Please select which of these sites you visit most often (choose all that is applicable) (input S when you're finished):
1. Reddit
2. Facebook
3. YouTube
4. Tumblr
5. Amazon
6. Ebay'''

#loop to input the data
linklist = []
while(1):
    x = raw_input()
    if (x != "S"):
        linklist.append(x)
    else:
        print "You have succesfully entered " + (str(len(linklist))) + " sites."
        break;

#function to visit random webpages on the internet
def randomsite():
        driver.get("http://www.uroulette.com/visit/oqvsoq")
        time.sleep(randint(0,7))
        print "currently on site: " + driver.current_url

#function to randomly visit a subreddit and then browse through it
def randomreddit():
    driver.get("http://reddit.com/r/random")
    url = driver.current_url+"top/.json?count=10"
    req = urllib2.Request(url, headers={ 'User-Agent': 'Mozilla/5.0' })
    posts = json.loads(urllib2.urlopen(req).read())
    leng = len(posts['data']['children'])
    for i in range(0,leng):
        driver.get("http://reddit.com"+posts['data']['children'][i]['data']['permalink'])
        print "currently on site: " + driver.current_url
        time.sleep(randint(0,5))
    print "currently on site: " + driver.current_url
    time.sleep(randint(0,4))

# loop to start the functions and visits
while(1):
    if '1' in linklist:
        randomreddit()
