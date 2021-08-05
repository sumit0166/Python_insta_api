from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup as b
import time

from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException
import random
import csv
import datetime
import calendar
import matplotlib.pyplot as plt
import numpy as np
#import pandas as pd
#import seaborn as sb
from getpass import getpass
from pandas import DataFrame
import seaborn as sb




# path = r"E:\Projects\Intern_project\driver\driver\MicrosoftWebDriver.exe"
path = r"E:\Projects\Intern_project\driver\chromedriver.exe"   # To use chrome

print("Enter Instagram Account Details For login ")
username = input("Enter Username\email : ")
password = getpass("Enter Password : ")

# driver = webdriver.Edge(path)
driver = webdriver.Chrome(path)

driver.get('https://www.instagram.com')
uid = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="loginForm"]/div/div[1]/div/label/input')))
uid.click()
uid.send_keys(username)
pswd = driver.find_element_by_xpath('//*[@id="loginForm"]/div/div[2]/div/label/input')
pswd.click()
pswd.send_keys(password)
btn = driver.find_element_by_xpath('//*[@id="loginForm"]/div[1]/div[3]/button')
btn.click()

not_now = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR,'#react-root > section > main > div > div > div > div > button')))
not_now.click()
try :
    no = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR,'body > div.RnEpo.Yx5HN > div > div > div > div.mt3GC > button.aOOlW.HoLwm')))
    no.click()
except :
    pass

usr = input("Enter Username To visualize : ")
WebDriverWait(driver, 30)

driver.get('https://www.instagram.com/'+usr)
find = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, '#react-root > section > main')))
html_parse = b(find.get_attribute('innerHTML'), 'html.parser')
followers = html_parse.findAll('span', {'class':'g47SY'})


post = followers[0].getText().replace(',', '')
follow = followers[1].getText().replace(',', '')
following = followers[2].getText().replace(',', '')

print("User : "+usr)
print("post : "+post)
print("Followers : "+follow)
print("Following : "+following)


pic_hrefs = []
for i in range(1, (int(int(post) / 10) + (int(post) % 10 > 0))):
    try:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2)
        # get tags
        hrefs_in_view = driver.find_elements_by_tag_name('a')
        # finding relevant hrefs
        hrefs_in_view = [elem.get_attribute('href') for elem in hrefs_in_view
                            if '.com/p/' in elem.get_attribute('href')]
        # building list of unique photos
        [pic_hrefs.append(href) for href in hrefs_in_view if href not in pic_hrefs]
        # print("Check: pic href length " + str(len(pic_hrefs)))
    except Exception:
        continue

unique_photos = len(pic_hrefs)
time_stamps = []
for pic_href in pic_hrefs:
    driver.get(pic_href)

    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    try:
        time.sleep(random.randint(2, 4))
        #get timestamp
        # element = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//time')))
        element = driver.find_elements_by_xpath("//time")
        time_stamps.append(element[0].get_attribute('datetime'))
        print(element[0].get_attribute('datetime'))
        # for second in reversed(range(0, random.randint(18, 28))):
        #     print('unique photos left: ' + str(unique_photos)
        #                     + " | Sleeping " + str(second))

    except Exception as e:
        print(e)

    unique_photos -= 1
    
print(time_stamps)

count_weekday = []
month_list = []
just_time_list = []
for t in time_stamps:
    datetime_conversion = datetime.datetime.strptime(t, '%Y-%m-%dT%H:%M:%S.%fZ')
    day = datetime_conversion.weekday()
    week_day = (calendar.day_name[day])
    month = datetime_conversion.strftime("%B")
    just_time = datetime_conversion.strftime("%I %p")
    print(datetime_conversion)
    print(week_day)
    print(month)
    count_weekday.append(week_day)
    month_list.append(month)
    just_time_list.append(just_time)
    print(count_weekday)

correct_weekday_order = ['Sunday','Monday','Tuesday','Wednesday','Thursday','Friday','Saturday']
sorted_weekdays = sorted(count_weekday, key=correct_weekday_order.index)


freq = {}
for item in sorted_weekdays:
    freq[item] = freq.get(item, 0)+1
print(freq)

keys = freq.keys()
values = freq.values()

plt.bar(keys, values)
plt.xlabel('Days of the week')
plt.ylabel('No. of posts')
plt.savefig('Graph_1.png', dpi=300, bbox_inches='tight')
plt.show()


correct_month_order = ['January','February','March','April','May','June','July','August','September','October','November','December']
sorted_months = sorted(month_list, key=correct_month_order.index)

freq_two = {}


try:
    for months in sorted_months:
        freq_two[months] = freq_two.get(months, 0)+1
    print(freq_two)
except ValueError:
    pass


index_keys = freq_two.keys()
Cols = ['Number of Posts']

#pd.Series(list(freq_two.values()), index=pd.Series(list(freq_two.keys())))

#df = ser.unstack().fillna(0)
#df.shape
#plt.imshow(ser, cmap='hot', interpolation='nearest')
#plt.show()


df = DataFrame(list(freq_two.values()), index = index_keys, columns = Cols)
cmap = sb.cm.rocket_r

sb.heatmap(df, annot = True, cmap = cmap)
plt.savefig('Garph_2.png', dpi=300, bbox_inches='tight')
plt.show()


print(just_time_list)

correct_time_order = ['12 AM','01 AM','02 AM','03 AM','04 AM','05 AM','06 AM', '07 AM', '08 AM','09 AM','10 AM','11 AM','12 PM','01 PM','02 PM','03 PM','04 PM','05 PM','06 PM','07 PM','08 PM','09 PM','10 PM','11 PM']
sorted_time = sorted(just_time_list, key=correct_time_order.index)

freq_three = {}

try:
    for hours in sorted_time:
        freq_three[hours] = freq_three.get(hours, 0)+1
    print(freq_three)
except ValueError:
    pass

tuples = sorted(freq_three.items())

x, y = zip(*tuples)

plt.plot(x, y)
plt.savefig('graph_3.png', dpi=300, bbox_inches='tight')
plt.show()