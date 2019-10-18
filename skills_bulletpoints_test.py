import pandas as pd
from bs4 import BeautifulSoup
from urllib.request import urlopen
from owlready2 import *
import nltk

key_words = ['qualifications', 'qualified', 'skills', 'required', 'qualifications:', 'skills:', 'responsibilities:',
             'responsibilities', 'duties', 'duties:', 'preferred', 'abilities', 'abilities:', 'require:', 'experience',
             'experience:']

def getSkills(file_name):
    data = pd.read_csv(file_name)
    url_column = data["IndeedJobListingURL"]  # gets url column from .csv file
    indeed_urls = url_column.tolist()

    base_url = 'https://www.indeed.com/'
    skills = []
    urls = []
    headings = []

    job_num = 1
    for url in indeed_urls:
        if (job_num == 1):
            print("Working on the first 10 jobs...")
        elif ((job_num % 10) == 0):
            print("Working on the next 10 jobs...")

        bullets = []
        url_heading = []

        try:
            urls.append(base_url + url)
            response = urlopen(base_url + url)  # connects to url
            soup = BeautifulSoup(response.read(), features="lxml")  # gets html

            description = soup.find(id='jobDescriptionText')

            bullet_points = description.select('p + ul')
            # for bullet in bullet_points:
            #     print(bullet.previous_sibling)

            for bullet in bullet_points:
                head = bullet.previous_sibling
                clean_head = BeautifulSoup(str(head), features='lxml').get_text().lower()

                tokens = nltk.word_tokenize(bullet)
                print(tokens)
                if any(word in clean_head for word in key_words):
                    url_heading.append(clean_head)
                    bullets.append(bullet)
            headings.append(url_heading)
            skills.append(bullets)
        except:
            skills.append("N/A")
            headings.append("N/A")

        job_num += 1

    df = pd.DataFrame({
        'URL': urls,
        'Headings': headings,
        'Bulletpoints': skills
    })

    return df


test = getSkills("indeedJobs_WA_computerprogrammer_entrylevel.csv")
# print(test)
test.to_csv("test.csv", index=None)
