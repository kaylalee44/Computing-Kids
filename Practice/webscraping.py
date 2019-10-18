# -*- coding: utf-8 -*-
"""
Created on Tue Jul  2 14:02:39 2019

@author: Kayla Lee
"""

from urllib.request import urlopen
from bs4 import BeautifulSoup
#import requests
import pandas as pd
import re
import matplotlib
           
def frequency_titles(city = None, state = None, job = None, job_title = None, explvl = None):
    base_url = 'https://www.indeed.com/'
    if job is not None:
        job = job.split()
        job = '+'.join(word for word in job)
        final_url = 'jobs?q=' + job 
    else:
        final_url = final_url + 'jobs?q=%22%22'
        
    if city is not None and state is not None:
        targetted_city = city.split()
        targetted_city = '+'.join(word for word in targetted_city)
        final_url = final_url + '&l=' + targetted_city + '%2C+' + state  
    elif city is not None and state is None:
        final_url = final_url + '&l=' + targetted_city
    else:
        final_url = final_url + '&l=' + state
    
    if job_title is not None:
        job_title = job_title.split()
        job_title = '+'.join(word for word in job_title)
        final_url = final_url + '&jt=' + job_title
        
    if explvl is not None:
        explvl = explvl.split()
        explvl = '+'.join(word for word in explvl)
        final_url = final_url + '&explvl=' + explvl
        
    final_url = base_url + final_url
    print(final_url)
    
    #alternative to urllib
#    response = requests.get(url)
#    data = response.text
#    soup = BeautifulSoup(data, 'lxml')
    
    html = urlopen(final_url) #connects to url
    soup = BeautifulSoup(html.read(), features="lxml") #gets html
    
    urls = [] #url storage
    titles = [] #titles storage
    
    # Extracting all the <a> tags with the class "jobtitle" into a list.
    tags = soup.findAll('a',attrs={"class":"jobtitle"})
    
    # Extracting URLs and titles from the attribute href and title in the <a> tags.
    for tag in tags:
        url = base_url + tag.get('href') 
        urls.append(url)
        title = tag.get('title')
        titles.append(title) 
    
    num_jobs_area = soup.find(id = 'searchCount').string
    job_numbers = re.findall('\d+', num_jobs_area) # Extract the total jobs found from the search result
    
    if len(job_numbers) >= 3: # Have a total number of jobs greater than 1000
        total_num_jobs = (int(job_numbers[1]) * 1000) + int(job_numbers[2])
    else:
        total_num_jobs = int(job_numbers[1]) 
        
    num_pages = round(total_num_jobs / 10)
    
    for i in range(1, num_pages + 1): # Loop through all of our search result pages
        start_num = str(i*10) # Assign the multiplier of 10 to view the pages we want
        current_page = ''.join([final_url, '&start=', start_num])
        html = urlopen(current_page) #connects to url
        bsObj = BeautifulSoup(html.read(), features="lxml") #gets html
        tags = bsObj.findAll('a',attrs={"class":"jobtitle"})
        for tag in tags:
            url = base_url + tag.get('href') 
            urls.append(url)
            title = tag.get('title')
            titles.append(title) 
             
    d = {'URL':urls, 'Title':titles}
    df = pd.DataFrame(d, columns=['URL', 'Title']) #make a dataframe
    return df

df = frequency_titles(city=None, state='WA', job='developer', 
                      job_title='fulltime', explvl='entry_level') 
df.to_csv('indeed_titles_urls.csv', header=['URL', 'Title'], encoding='utf-8')

#Frequency table (shows frequency of titles)
#df['Counts'] = df.groupby(['Title'])['URL'].transform(len)
#df.to_csv('indeed_webscraping.csv', header=['URL', 'Title', 'Frequency'], encoding='utf-8')

frequency = df.Title.value_counts()
final_plot = frequency.plot(x = 'Job Title', y = 'Frequency', kind = 'bar', 
                            legend = None, title = 'Frequency of Job Titles')
fig = final_plot.get_figure()

frequency.to_csv('indeed_title_freq.csv', header=['Frequency'], 
                 encoding='utf-8')



    





