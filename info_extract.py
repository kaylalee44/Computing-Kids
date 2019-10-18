import pandas as pd
from bs4 import BeautifulSoup
from urllib.request import urlopen
import csv


def jobsUpdated(file_name):
    """
    Goes through a data set file and looks through all the job listings for the date it was posted. If the days posted
    was 1, 7, 14, or 21 days ago, then the counter goes up. Prints out the number of jobs that were posted within the
    number range.

    :param file_name: name of data set file passed in
    :return: number of jobs that were updated
    """

    df = pd.read_csv(file_name)
    url_column = df["IndeedJobListingURL"]  # gets url column from .csv file
    urls = url_column.tolist()

    num_last_updated = 0

    base_url = 'https://www.indeed.com/'
    job_num = 1
    for url in urls:
        if (job_num == 1):
            print("Checking first 10 jobs...")
        elif ((job_num % 10) == 0):
            print("Checking next 10 jobs...")

        html = urlopen(base_url + url)  # connects to url
        soup = BeautifulSoup(html.read(), features="lxml")  # gets html

        last_updated_days = soup.find('div', attrs={'class': 'jobsearch-JobMetadataFooter'}).text  # text

        for s in last_updated_days.split():  # extracting number
            if s.isdigit():
                days = int(s)
        # print(days)

        if (days == 1 or days == 7 or days == 14 or days == 21):
            num_last_updated += 1

        job_num += 1

    return (str(num_last_updated) + " jobs were updated 1, 7, 14, or 21 days ago" + "\n")


# test = jobsUpdated("indeedJobs_WA_computerprogrammer_entrylevel.csv")
# print(test)

def companyCount(file_name):
    """
    Goes through the data set passed in and creates a data frame of all the companies and a count of each company.

    :param file_name: name of data set file passed in
    :return: data frame of all the companies and the counts for them
    """

    df = pd.read_csv(file_name)
    company_column = df["Company"]  # gets company column from .csv file
    companies = company_column.tolist()

    count = {}
    for company in companies:
        if company not in count:
            count[company] = 1
        else:
            count[company] = count.get(company, 0) + 1
    df = pd.DataFrame.from_dict(count, orient='index', columns=['Count'])
    df.index.name = 'Company'
    df = df.sort_values(by=['Count'], ascending=False)
    return df


test1 = companyCount("indeedJobs_WA_computerprogrammer_entrylevel.csv")
print(test1)
# test1.to_csv("test.csv")

def locationCount(file_name):
    """
    Goes through the data set passed in and creates a data frame of all the location cities and states and a count for
    each location.

    :param file_name: name of data set file passed in
    :return: data frame of all the locations and the counts for them
    """

    df = pd.read_csv(file_name)
    locationstate_column = df["LocationState"]  # gets location state column from .csv file
    locationstate = locationstate_column.tolist()

    locationcity_column = df["LocationCity"]
    locationcity = locationcity_column.tolist()

    count = {}
    for i in range(0, len(locationcity)):
        location = str(locationcity[i]) + ", " + str(locationstate[i])
        if location not in count:
            count[location] = 1
        else:
            count[location] = count.get(location, 0) + 1
    df = pd.DataFrame.from_dict(count, orient='index', columns=['Count'])
    df.index.name = 'Location'
    df = df.sort_values(by=['Count'], ascending=False)
    return df


test2 = locationCount("indeedJobs_WA_computerprogrammer_entrylevel.csv")
print(test2)
# test2.to_csv("test.csv")

def countJobType(file_name):
    """
    Goes through the data set and creates a data frame of all the job types and a count for each job type.

    :param file_name: name of data set file passed in
    :return: data frame of all the job types and the counts for them
    """
    df = pd.read_csv(file_name)
    jobtype_column = df["JobType"]
    jobtype = jobtype_column.tolist()

    count = {}
    for type in jobtype:
        if type not in count:
            count[type] = 1
        else:
            count[type] = count.get(type, 0) + 1
    df = pd.DataFrame.from_dict(count, orient='index', columns=['Count'])
    df.index.name = 'JobType'
    df = df.sort_values(by=['Count'], ascending=False)
    return df


test2 = countJobType("indeedJobs_WA_software_internship_entrylevel.csv")
print(test2)
# test2.to_csv("test.csv")

def countSalary(file_name):
    """
    Goes through the data set and identifies how many jobs have salaries attached and how many don't. Also, identifies
    all possible options of the salary units and converts all salaries to the same unit (hourly).

    :param file_name: name of data set file passed in
    :return: a string with details on how many jobs have salaries and how many don't.
    """

    df = pd.read_csv(file_name)
    minsalary_column = df["MinimumSalary"]
    min = minsalary_column.tolist()
    min_null = minsalary_column.isnull()

    maxsalary_column = df["MaximumSalary"]
    max = maxsalary_column.tolist()
    max_null = maxsalary_column.isnull()

    salaryunits_column = df["SalaryTimeUnits"]
    salaryunits = salaryunits_column.tolist()

    units = []
    for unit in salaryunits:
        if unit not in units:
            units.append(unit)
    print(units)

    withSalary = 0
    withoutSalary = 0
    print(min)
    for i in range(0, len(min)):
        if min_null[i] and max_null[i]:
            withoutSalary += 1
        else:
            withSalary += 1
    #         if salaryunits[i] != "Hourly":
    #             min[i] = int(min[i]) / 2080
    #             max[i] = int(max[i]) / 2080
    # print(min)

    return "There are " + str(withSalary) + " jobs with salaries attached and " + str(withoutSalary) + \
           " without salaries attached."


test3 = countSalary("indeedJobs_WA_computerprogrammer_entrylevel.csv")
print(test3)
# test3.to_csv("test.csv")


