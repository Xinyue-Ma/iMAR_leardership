# -*- coding: utf-8 -*-
"""
Created on Wed Mar 31 02:18:24 2021

@author: Xinyue
"""
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
This is a modification of the code sourced from this article: https://www.linkedin.com/pulse/how-easy-scraping-data-from-linkedin-profiles-david-craven/?trackingId=HUfuRSjER1iAyeWmcgHbyg%3D%3D
It is a web scraper scraping google for linkedin profiles; the use case would be recruiters sourcing target candidates for recruiting purposes. 
Also copied the find_profiles function from here: https://www.pingshiuanchua.com/blog/post/scraping-search-results-from-google-search 

"""


from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
from bs4.element import Tag
from time import sleep
import csv
from parsel import Selector
import numpy

""" parameters """
# search query 
search_query_link = 'site:linkedin.com/in/ AND "python developer" AND "London"'
# file were scraped profile information will be stored  
file_name = 'results_file.csv'
# login credentials
linkedin_username = '1143183660@qq.com'
linkedin_password = '********'


# Function call extracting title and linkedin profile iteratively
def find_profiles():
    for r in result_div:
        # Checks if each element is present, else, raise exception
        try:
            link = r.find('a', href=True)
            title = None
            title = r.find('h3')
            # returns True if a specified object is of a specified type; Tag in this instance 
            if isinstance(title,Tag):
                title = title.get_text()
                title = title + ' -'
    
            description = None
            description = r.find('span', attrs={'class': 'st'})
            if isinstance(description, Tag):
                description = description.get_text()
                
       
    
            # Check to make sure everything is present before appending
            if link != '' and title != '' and description != '':
                links.append(link['href'])
                titles.append(title)
                descriptions.append(description)
            
    
        # Next loop if one element is not present
        except Exception as e:
            print(e)
            continue
        
# This function iteratively clicks on the "Next" button at the bottom right of the search page. 
def profiles_loop():
    
    find_profiles()
    
    next_button = driver.find_element_by_xpath('//*[@id="pnnext"]') 
    next_button.click()
    
    
def repeat_fun(times, f):
    for i in range(times): f()
    
# specifies the path to the chromedriver.exe
driver = webdriver.Chrome()


# driver.get method() will navigate to a page given by the URL address
driver.get('https://www.linkedin.com')

# locate email form by_class_name
username = driver.find_element_by_id('session_key')

# send_keys() to simulate key strokes
username.send_keys(linkedin_username)
sleep(0.5)

# locate password form by_class_name
password = driver.find_element_by_id('session_password')

# send_keys() to simulate key strokes
password.send_keys(linkedin_password)
sleep(0.5)

# locate submit button by_class_name
log_in_button = driver.find_element_by_class_name('sign-in-form__submit-button')

# .click() to mimic button click
log_in_button.click()
sleep(0.5)


# driver.get method() will navigate to a page given by the URL address
driver.get('https://www.google.com')
sleep(1)

# locate search form by_name
search_query = driver.find_element_by_name('q')

# send_keys() to simulate the search text key strokes
search_query.send_keys(search_query_link)

# .send_keys() to simulate the return key 
search_query.send_keys(Keys.RETURN)





    
# initialize empty lists
links = []
titles = []
descriptions = []


# Function call x10 of function profiles_loop; you can change the number to as many pages of search as you like. 
repeat_fun(10, profiles_loop)
soup = BeautifulSoup(driver.page_source,'lxml')
result_div = soup.find_all('div', attrs={'class': 'g'})


print(titles)
print(links)

# Separates out just the First/Last Names for the titles variable
        
        
# titles2 = [i.split("...") for i in titles1]
str = '| LinkedIn'

titles01 = [i.split("-")[0] for i in titles]
titles02 = [i.split("-")[1] for i in titles]
titles03 = [i.split("-")[2].strip(str) for i in titles]
# titles03 = [i.split("-")[2] for i in titles]


# The function below stores scraped data into a .csv file
from itertools import zip_longest
# Load titles and links data into csv
d = [titles01, titles02, titles03, links]
export_data = zip_longest(*d, fillvalue = '')
with open(file_name, 'w', encoding="ISO-8859-1", newline='') as myfile:
      wr = csv.writer(myfile)
      wr.writerow(("Name", "Current_Job", "Current_Company", "Links"))
      wr.writerows(export_data)
myfile.close()


