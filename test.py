import requests
from urllib.request import urlopen
import re
from bs4 import BeautifulSoup

url = "https://www.indeed.com/jobs?q=data+scientist&l=WA&explvl=entry_level&start={}"
# page_response = requests.get(url, timeout=3)
# soup = BeautifulSoup(page_response.content, 'html.parser')

html = urlopen(url) #connects to url
soup = BeautifulSoup(html.read(), features="lxml") #gets html

num_jobs_area = soup.find(id = 'searchCount').string
job_numbers = re.findall('\d+', num_jobs_area) # Extract the total jobs found from the search result

if len(job_numbers) >= 3: # Have a total number of jobs greater than 1000
    total_num_jobs = (int(job_numbers[1]) * 1000) + int(job_numbers[2])
else:
    total_num_jobs = int(job_numbers[1])

print(total_num_jobs)