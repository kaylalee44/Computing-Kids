from bs4 import BeautifulSoup
import pandas as pd
import requests
import urllib3
from urllib.request import urlopen
import matplotlib.pyplot as plt
import re
import time
import sys
import demjson
from datetime import datetime, timedelta
import urllib
from nltk.tokenize import word_tokenize

stateAbbrev_USA = ["AL", "AK", "AZ", "AR", "CA", "CO", "CT", "DE",
                   "FL", "GA", "HI", "ID", "IL", "IN", "IA", "KS",
                   "KY", "LA", "ME", "MD", "MA", "MI", "MN", "MS",
                   "MO", "MT", "NE", "NV", "NH", "NJ", "NM", "NY",
                   "NC", "ND", "OH", "OK", "OR", "PA", "RI", "SC",
                   "SD", "TN", "TX", "UT", "VT", "VA", "WA", "WV",
                   "WI", "WY"]

gen_headers = ['qualifications', 'qualified', 'skills', 'responsibilities', 'duties', 'abilities', 'experience']
required_headers = ['required', "must have", "essential", "needed", "minimum", "require", "basic", "at least"]
good_to_have_headers = ['preferred', "good to have", "nice to have"]
skills_labels = [".Htaccess", ".Net", ".Net-Core", "Abstraction", "Accounting", "Actionscript-3", "Activerecord",
                 "Administration", "Adobe", "Agile", "Ajax", "Algorithm", "Algorithms", "Amazon", "Amazon-Ec2",
                 "Amazon-S3", "Amazon-Web-Services", "Analysis", "Analytics", "Android", "Android-Activity",
                 "Android-Asynctask", "Android-Fragments", "Android-Intent", "Android-Layout", "Android-Listview",
                 "Android-Recyclerview", "Android-Studio", "Angular", "Angularjs", "Angularjs-Directive", "Animation",
                 "Ant", "Apache", "Apache-Flex", "Apache-Kafka", "Apache-Spark", "Api", "Api", "Apl", "App",
                 "Application", "Applications", "Architecture", "Architecture", "Arduino", "Arraylist", "Arrays",
                 "Artificial", "Asp.Net", "Asp.Net-Core", "Asp.Net-Mvc", "Asp.Net-Mvc-3", "Asp.Net-Mvc-4",
                 "Asp.Net-Mvc-5", "Asp.Net-Web-Api", "Assembly", "Assessment", "Asynchronous", "Audio",
                 "Authentication", "Autocomplete", "Automation", "Awk", "Aws", "Azure", "Backbone.Js", "Backend",
                 "Bash", "Basic", "Batch-File", "Beautifulsoup", "Big", "Binding", "Bitmap", "Blender", "Blueprint",
                 "Bluetooth", "Boost", "Bootstrap-4", "Browser", "Build", "Button", "C", "C#", "C#-4.0", "C#/.Net",
                 "C++", "C++11", "Caching", "Caffe", "Cakephp", "Callback", "Caml", "Canvas", "Cassandra", "Casting",
                 "Certifications", "Charts", "Checkbox", "Chemistry", "Clang", "Class", "Clojure", "Cloud",
                 "Cloud/Saas", "Cloudkit", "Cmake", "Cmd", "Cms", "Cocoa", "Cocoa-Touch", "Code", "Codeigniter",
                 "Coding", "Collections", "Colors", "Combobox", "Command-Line", "Communication", "Communications",
                 "Compiler-Errors", "Compiling", "Complex", "Computer", "Computing", "Concurrency", "Configuration",
                 "Constructor", "Control", "Cookies", "Cordova", "Core-Data", "Count", "Creative", "Crm",
                 "Cryptography", "Css", "Css3", "Csv", "Cuda", "Curl", "Customer", "Cyber", "D3.Js", "Dart", "Data",
                 "Data-Binding", "Data-Structures", "Database", "Database-Design", "Dataframe", "Datagrid",
                 "Datagridview", "Datatable", "Datatables", "Date", "Datepicker", "Datetime", "Debugging", "Deep",
                 "Delivery", "Delphi", "Dependency-Injection", "Deployment", "Description", "Design", "Design-Patterns",
                 "Development", "Devise", "Dictionary", "Digital", "Directory", "Django", "Django-Models",
                 "Django-Rest-Framework", "Dll", "Docker", "Doctrine-Orm", "Documentation", "Dom", "Download", "Dplyr",
                 "Drop-Down-Menu", "Drupal", "Dynamic", "Eclipse", "Ecmascript-6", "Elasticsearch", "Electrical",
                 "Elixir", "Eloquent", "Emacs", "Email", "Ember.Js", "Encapsulation", "Encoding", "Encryption",
                 "Engineer", "Engineering", "Engineering", "Enterprise", "Entity-Framework", "Enums", "Enzyme", "Erp",
                 "Error-Handling", "Evaluation", "Events", "Excel", "Excel-Formula", "Excel-Vba", "Exception",
                 "Exception-Handling", "Experience", "Express", "Extjs", "Facebook", "Facebook-Graph-Api", "Ffmpeg",
                 "File", "File-Io", "File-Upload", "Filter", "Firebase", "Firebase-Realtime-Database", "Firefox",
                 "Firewalls", "Flash", "Flask", "Flow", "Flutter", "Fonts", "For-Loop", "Foreach", "Forms", "Fortran",
                 "Framework", "Frameworks", "Frontend", "Full", "Function", "Functional-Programming", "Functionality",
                 "Gcc", "Generics", "Ggplot2", "Git", "Github", "Go", "Golang", "Google-Analytics", "Google-Api",
                 "Google-App-Engine", "Google-Apps-Script", "Google-Chrome", "Google-Chrome-Extension",
                 "Google-Cloud-Platform", "Google-Maps", "Google-Maps-Api-3", "Google-Sheets", "Gradle", "Grails",
                 "Graph", "Graphics", "Gridview", "Groovy", "Group-By", "Gwt", "Hadoop", "Hardware", "Hash", "Haskell",
                 "Hdl", "Heroku", "Hibernate", "Highcharts", "Hive", "Hml", "Host-Based", "Html", "Html5", "Html-Table",
                 "Http", "Https", "Human", "Hyperlink", "Ict", "If-Statement", "Iframe", "Iis", "Image",
                 "Image-Processing", "Immutable.Js", "Implementation", "Import", "Indesign", "Indexing", "Information",
                 "Infrastructure", "Inheritance", "Input", "Installation", "Instructing", "Intelligence", "Intellij",
                 "Intellij-Idea", "Interface", "Internet-Explorer", "Invision", "Io", "Ionic-Framework", "Ios", "Ios7",
                 "Ip", "Ipad", "Iphone", "Jar", "Java", "Java-8", "Java-Ee", "Javafx", "Javascript", "Jdbc", "Jenkins",
                 "Jest", "Join", "Joomla", "Jpa", "Jquery", "Jquery-Mobile", "Jquery-Ui", "Jsf", "Jsf-2", "Json", "Jsp",
                 "Junit", "Jupyter", "Kaggle", "Kali", "Kendo-Ui", "Keras", "Kernal", "Knockout.Js", "Kotlin",
                 "Kubernetes", "Lambda", "Language", "Language", "Laravel", "Laravel-4", "Laravel-5", "Latex", "Layout",
                 "Learning", "Linked-List", "Linq", "Linq-To-Sql", "Linux", "Linux/Unix", "Lisp", "List", "Listview",
                 "Logging", "Login", "Loops", "Lua", "Machine", "Machine-Learning", "Macos", "Magento", "Maintenance",
                 "Makefile", "Management", "Management", "Manufacturing", "Markdown", "Markup", "Math", "Mathematics",
                 "Matlab", "Matplotlib", "Matrix", "Maven", "Mechanical", "Media", "Memory", "Memory-Leaks",
                 "Memory-Management", "Menu", "Merge", "Meteor", "Methods", "Microsoft", "Middleware", "Mining",
                 "Mobile", "Mod-Rewrite", "Model", "Model-View-Controller", "Modeling", "Modems/Routers", "Modification",
                 "Module", "Mongodb", "Mongoose", "Monitoring", "Ms-Access", "Ms-Word", "Multidimensional-Array",
                 "Multithreading", "Mvvm", "Mysql", "Mysqli", "Natural", "Neo4J", "Netbeans", "Network", "Networking",
                 "Neural", "New", "Nginx", "Nhibernate", "Node", "Node.Js", "Nosql", "Notebook", "Npm",
                 "Nullpointerexception", "Numeracy", "Numpy", "Oauth", "Oauth-2.0", "Object", "Object-Oriented",
                 "Objective-C", "Office", "Oop", "Opencv", "Opengl", "Operating", "Operation", "Optimization", "Oracle",
                 "Oracle11G", "Ordering", "Orm", "Outlook", "Pagination", "Pandas", "Parallel-Processing", "Parameters",
                 "Parse-Platform", "Parsing", "Pascal", "Path", "Paypal", "Pdf", "Pdo", "Performance", "Perl",
                 "Persuasion", "Photoshop", "Php", "Phpmyadmin", "Physics", "Pivot", "Planning", "Playframework",
                 "Plot", "Plsql", "Plugins", "Pointers", "Polymorphism", "Post", "Postgresql", "Powershell",
                 "Presentation", "Primefaces", "Printing", "Problem", "Process", "Processing", "Product",
                 "Programming", "Promise", "Properties", "Proxy", "Push-Notification", "Pycharm", "Pyspark", "Python",
                 "Python-2.7", "Python-3.X", "Pytorch", "Qt", "Quantitative", "Query", "R", "Random", "Razor", "React",
                 "React-Native", "Reactjs", "Recursion", "Redirect", "Redis", "Redux", "Reflection", "Regex",
                 "Regression", "Relationship", "Repairing", "Replace", "Reporting-Services", "Reports", "Repository",
                 "Research", "Resource", "Resources", "Responsive-Design", "Rest", "Restful", "Restoration", "Reviews",
                 "Revision", "Risk", "Rpc", "Rspec", "Ruby", "Ruby-On-Rails", "Ruby-On-Rails-3", "Ruby-On-Rails-4",
                 "Saas", "Safari", "Sass", "Scala", "Scikit-Learn", "Scipy", "Scope", "Scraping", "Scratch",
                 "Scripting", "Scroll", "Scrum", "Scss", "Sdk", "Search", "Security", "Sed", "Select", "Selenium",
                 "Selenium-Webdriver", "Serialization", "Server", "Server", "Servers", "Service", "Services",
                 "Services", "Servlets", "Session", "Setup", "Sharepoint", "Shell", "Shiny", "Silverlight", "Soap",
                 "Social", "Socket", "Socket.Io", "Sockets", "Software", "Solr", "Solution", "Solving", "Sonography",
                 "Sorting", "Source", "Split", "Spring", "Spring-Boot", "Spring-Mvc", "Spring-Security", "Sql", "Sql",
                 "Sql-Server", "Sql-Server-2005", "Sql-Server-2008", "Sql-Server-2012", "Sqlite", "Ssh", "Ssis", "Ssl",
                 "Stack", "Statistical", "Statistics", "Storage", "Stored-Procedures", "String", "Struct", "Structural",
                 "Structures", "Study", "Suite", "Support", "Svg", "Svn", "Swift", "Swift3", "Swing", "Symfony",
                 "Syntax", "Systems", "Tables", "Tcl", "Tcp", "Team", "Technical", "Techniques", "Technologies",
                 "Technology", "Telecommunications", "Templates", "Tensor", "Tensorflow", "Terminal", "Test", "Testing",
                 "Text", "Tfs", "Three.Js", "Time", "Timer", "Tkinter", "Tomcat", "Toolkits", "Tools", "Training",
                 "Triggers", "Troubleshooting", "Tsql", "Twitter", "Twitter-Bootstrap", "Twitter-Bootstrap-3", "Types",
                 "Typescript", "Ubuntu", "Ui", "Uikit", "Uitableview", "Uiview", "Uiviewcontroller", "Unicode",
                 "Unit-Testing", "Unity", "Unity3D", "Unix", "Url", "Url-Rewriting", "Usability", "User",
                 "User-Interface", "Utf-8", "Uwp", "Ux", "Validation", "Variables", "Vb.Net", "Vba", "Vbscript",
                 "Vector", "Verification", "Version", "Version-Control", "Video", "View", "Vim", "Virtual", "Vision",
                 "Visual", "Visual-C++", "Visual-Studio", "Visual-Studio-2008", "Visual-Studio-2010",
                 "Visual-Studio-2012", "Visual-Studio-2013", "Visual-Studio-2015", "Visual-Studio-Code", "Vue", "Vue.Js",
                 "Vuejs2", "Wcf", "Web", "Web", "Web-Applications", "Web-Scraping", "Web-Services", "Webforms",
                 "Webpack", "Websocket", "Webview", "While-Loop", "Winapi", "Windows", "Windows-Phone-7",
                 "Windows-Phone-8", "Winforms", "Wireless", "Woocommerce", "Wordpress", "Wpf", "Writing", "Xamarin",
                 "Xamarin.Android", "Xamarin.Forms", "Xaml", "Xcode", "Xml", "Xpath", "Xslt", "Yii", "Zend-Framework",
                 "Zeppelin"]

base_url = 'https://www.indeed.com/'


def createURL(city=None, state=None, job=None, job_title=None, explvl=None, sort=None):
    """
    Takes in filters (location, search query, job title, experience level) and generates an Indeed URL
    that shows all the job postings with the specified filters
    :param city: city location
    :param state: state location
    :param job: job search query
    :param job_title: position i.e. full time, part time, etc.
    :param explvl: experience level i.e. entry level
    :param sort: jobs sorted by i.e. date
    :return: generated Indeed URL
    """

    final_url = ''
    if job is not None:
        job = job.split()
        job = '+'.join(word for word in job)
        final_url = 'jobs?q=' + job
    else:
        final_url = final_url + 'jobs?q=%22%22'

    if city is not None and state is not None:
        city = city.split()
        city = '+'.join(word for word in city)
        final_url = final_url + '&l=' + city + '%2C+' + state
    elif city is not None and state is None:
        final_url = final_url + '&l=' + city
    elif city is None and state is not None:
        final_url = final_url + '&l=' + state

    if job_title is not None:
        job_title = job_title.split()
        job_title = ''.join(word for word in job_title)
        final_url = final_url + '&jt=' + job_title

    if explvl is not None:
        explvl = explvl.split()
        explvl = '_'.join(word for word in explvl)
        final_url = final_url + '&explvl=' + explvl

    if sort is not None:
        final_url = final_url + '&sort=' + sort

    final_url = final_url + "&start={}"
    final_url = base_url + final_url
    print("Base URL for web scraping: " + final_url)

    return final_url


def getRoleTitle(job):
    """
    Takes job card and returns the job title
    :param job: job card being looked at
    :return: title for job card
    """

    search = [job.find(name="a", attrs={"data-tn-element": "jobTitle"})]
    # print(search)
    try:
        return search[0]["title"]
    except:
        return "N/A"


def getIndeedJobListingURL(job):
    """
    Takes job card and returns url
    :param job: job being looked at
    :return: url for job card
    """

    search = [job.find("div", {"class": "title"})]
    try:
        return base_url + search[0].a['href']
    except:
        return "N/A"


def getCompany(job):
    """
    Takes job card and returns the company
    :param job: job being looked at
    :return: company of job card
    """

    search = [job.find("span", {"class": "company"})]
    try:
        if search[0].text.strip() is None:
            return search[0].find(name="a", attrs={"data-tn-element": "companyName"}).text.strip()
        else:
            return search[0].text.strip()
    except:
        return "N/A"


def getFullLocation(job):
    """
    Takes in a job card to parse location. This function is sent to getLocationArea() to parse info
    - need to handle edge cases like encountering 'Remote', 'Washington State', 'United States',
    :param job: job being looked at
    :return: full location of job card
    """

    search = [job.find(re.compile(r"(span|div)"), {"class": "location"})]
    try:
        return search[0].text
    except:
        return "N/A"


def getLocationState(job):
    """
    Takes job card and returns location state
    :param job: job being looked at
    :return: location state of job card
    """

    search = [job.find(re.compile(r"(span|div)"), {"class": "location"})]
    # print(search)
    loc = word_tokenize(search[0].text)
    try:
        if len(loc) >= 3:
            return loc[2]
        else:
            return "N/A"
    except:
        return "N/A"


def getLocationCity(job):
    """
    Takes job card and returns the location city
    #need to handle "washington state, remote, etc
    :param job: job being looked at
    :return: location city of job card
    """

    search = [job.find(re.compile(r"(span|div)"), {"class": "location"})]
    loc = word_tokenize(search[0].text)
    try:
        if len(loc) >= 3:
            return loc[0]
        else:
            return "N/A"
    except:
        return "N/A"


def getLocationZipCode(job):
    """
    Takes job card and returns location zip code
    :param job: job being looked at
    :return: location zip code from job card
    """

    search = [job.find(re.compile(r"(span|div)"), {"class": "location"})]
    loc = word_tokenize(search[0].text)
    try:
        if len(loc) == 4:
            return loc[3]
        else:
            return "N/A"
    except:
        return "N/A"


def getLocationArea(l):
    """
    Takes full location string from getFullLocation() and extracts location area
    :param l: full location
    :return: area from job card
    """

    first = l.find('(')
    last = l.find(')')
    if first != -1 and last != -1:
        return l[first:last + 1]
    else:
        return "N/A"


def getSalary(job):
    """
    Takes a job card and parses the salary string
    :param job: job being looked at
    :return: salary from job card
    """

    search = [job.find("span", {"class": "salary no-wrap"})]
    try:
        if not search:
            return "N/A"
        else:
            return search[0].text.strip()
    except:
        return "N/A"


def getMinimumSalary(l):
    """
    Takes full salary to parse minimum salary
    :param l: full salary
    :return: min salary from job card
    """

    pattern = r"(?:[\£\$\€]{1}[,\d]+.?\d*)"
    l = l.replace(".00", "")
    salary = re.findall(pattern, l)
    try:
        return salary[0]
    except:
        return "N/A"


def getMaximumSalary(l):
    """
    Takes full salary to parse maximum salary
    :param l: full salary
    :return: max salary from job card
    """

    pattern = r"(?:[\£\$\€]{1}[,\d]+.?\d*)"
    l = l.replace(".00", "")
    salary = re.findall(pattern, l)
    try:
        return salary[1]
    except:
        return "N/A"


def getSalaryTimeUnits(l):
    """
    Takes full salary and parses for time unit
    :param l: full salary
    :return: time units from job card (for salary)
    """

    if 'hour' in l:
        return 'Hourly'
    elif 'day' in l:
        return 'Daily'
    elif 'week' in l:
        return 'Weekly'
    elif 'year' in l:
        return 'Yearly'
    else:
        return 'N/A'


def getShortDescription(job):
    """
    Takes job card and parses the short description for job postings
    :param job: job being looked at
    :return: short description from job card
    """

    search = [job.find("div", {"class": "summary"})]
    try:
        return search[0].text.strip()
    except:
        return "N/A"


def getHasExpressApply(job):
    """
    Takes job card and parses express apply option
    :param job: job being looked at
    :return: express apply from job card (if there is express apply, otherwise returns N/A)
    """

    search = [job.find("div", {"class": "iaWrapper"})]
    try:
        if search is None:
            return "N/A"
        else:
            return search[0].div.span.text.strip()
    except:
        return "N/A"


def getIsSponsored(job):
    """
    Takes job card and parses sponsored option
    :param job: job being looked at
    :return: sponsor of job card (if there is one, otherwise returns N/A)
    """

    search = [job.find("span", {"class": "sponsoredGray"})]
    try:
        if not search:
            return "N/A"
        else:
            return search[0].text
    except:
        return "N/A"


def getExperienceLevel(url):
    """
    Takes the url (from creation) and finds experience level
    :param url: url we're looking at
    :return: exp lvl of job
    """

    if 'entry_level' in url:
        return "Entry Level"
    elif 'mid_level' in url:
        return "Mid Level"
    elif 'senior_level' in url:
        return "Senior Level"
    else:
        return "N/A"


def getJobType(url):
    """
    Takes the url (from creation) and finds job type
    :param url: url we're looking at
    :return: job type of job
    """

    if 'fulltime' in url:
        return "Full-time"
    elif 'internship' in url:
        return "Internship"
    elif 'parttime' in url:
        return "Part-time"
    elif 'temporary' in url:
        return "Temporary"
    elif 'contract' in url:
        return "Contract"
    elif 'commission' in url:
        return "Commission"
    else:
        return "N/A"


def getResponsiveEmployer(job):
    """
    Takes job card and parses responsive employer
    :param job: job being looked at it
    :return: responsive employer from job card (if employer is responsive, otherwise returns N/A)
    """

    search = [job.find("div", {"class": "serp-ResponsiveEmployer"})]
    try:
        return search[0].text
    except:
        return "N/A"


# def getCmpID(l, jobMapCount):
#     """
#     Takes jobmap and appends company id
#     :param l: jobmap
#     :param jobCount: iteration number for loop (number of jobs on a page)
#     :return: list of company ids
#     """
#
#     ret = []
#     for items in l:
#         ret.append(items['cmpid'])
#     checkRet(ret, getCmpID.__name__, jobMapCount)
#     return ret
#
#
# def getCmpEsc(l, jobMapCount):
#     """
#     Takes jobmap and appends cmpesc
#     :param l: jobmap
#     :param jobMapCount: iteration number for loop
#     :return: list of cmpesc
#     """
#
#     ret = []
#     for items in l:
#         ret.append(items['cmpesc'])
#     checkRet(ret, getCmpEsc.__name__, jobMapCount)
#     return ret
#
#
# def getSrcName(l, jobMapCount):
#     """
#     Takes jobmap and appends srcname
#     :param l: jobmap
#     :param jobMapCount: iteration number for loop
#     :return: list of srcname
#     """
#
#     ret = []
#     for items in l:
#         ret.append(items['srcname'])
#     checkRet(ret, getSrcName.__name__, jobMapCount)
#     return ret


def getJobID(job):
    """
    Takes job card and parses for each job listing's ID
    :param job: job being looked at
    :return: job ID from job card
    """

    try:
        return job.get('id')
    except:
        return "N/A"


# check if the search 0 (meaning indeed changed their html var names (wont find them)
# if they kept same names & changed data inside -> think about it
# tells us if indeed changed job posting amts too i.e they start displaying n>10 or n<10
# can add like a global error count and if it > 2 = stop program
def checkRet(l, check, jobCount):
    # print("HTML might have changed. Check function:", check, "--- retLen:", len(l))
    if len(l) != jobCount:
        print("HTML might have changed. Check function: ", check, ".")
    pass


# def scrape(soup):
#     """
#     Takes soup obj -> sends to helper functions to obtain info for our data frame
#     :param soup: soup object
#     :return: roleTitle,company,fullLocation,locationState,
#            locationCity,locationZipCode,locationArea,
#            salary,minSalary,maxSalary,salaryTimeUnits,
#            shortDesc,expressApply,sponsor,indeedURL,
#            expLevel,responsiveEmployer,cmpID,cmpEsc,srcName
#     """
#
#     pattern = re.compile(r"jobmap\[\d+\]= (.*);")
#
#     if soup.find('script', text=lambda text: text and "jobmap = {}" in text) is None:
#         return  # might need to return all the lists
#     else:
#         search = soup.find('script', text=lambda text: text and "jobmap = {}" in text).text
#         data1 = [demjson.decode(item, strict=False) for item in pattern.findall(search)]
#         jobMapCount = 0
#         # the amount of jobs on display pg
#         for i in data1:
#             jobMapCount += 1
#         # print('jobamt=',jobMapAmt)
#
#
#         roleTitle = getRoleTitle(data1, jobMapCount)
#         company = getCompany(data1, jobMapCount)
#         fullLocation = getFullLocation(soup, jobMapCount)  # send to getLocationArea()
#         locationState = getLocationState(data1, jobMapCount)
#         locationCity = getLocationCity(data1, jobMapCount)
#         locationZipCode = getLocationZipCode(data1, jobMapCount)
#         locationArea = getLocationArea(fullLocation, jobMapCount)
#         salary = getSalary(soup, jobMapCount)  # parse this to get min/max salary and salarytimeunits
#         minSalary = getMinimumSalary(salary, jobMapCount)
#         maxSalary = getMaximumSalary(salary, jobMapCount)
#         salaryTimeUnits = getSalaryTimeUnits(salary, jobMapCount)
#         shortDesc = getShortDescription(soup, jobMapCount)
#         expressApply = getHasExpressApply(soup, jobMapCount)
#         sponsor = getIsSponsored(soup, jobMapCount)
#         indeedURL = getIndeedJobListingURL(soup, jobMapCount)
#         expLevel = getExperienceLevel(URL, jobMapCount)  # uses url
#         jobType = getJobType(URL, jobMapCount)  # uses url
#         lastUpdated = getLastUpdated(soup, jobMapCount)
#         responsiveEmployer = getResponsiveEmployer(soup, jobMapCount)
#         cmpID = getCmpID(data1, jobMapCount)
#         cmpEsc = getCmpEsc(data1, jobMapCount)
#         srcName = getSrcName(data1, jobMapCount)
#         jobID = getJobID(soup, jobMapCount)
#
#         return roleTitle, company, fullLocation, locationState, \
#                locationCity, locationZipCode, locationArea, \
#                salary, minSalary, maxSalary, salaryTimeUnits, \
#                shortDesc, expressApply, sponsor, indeedURL, \
#                expLevel, jobType, lastUpdated, responsiveEmployer, cmpID, cmpEsc, srcName, jobID


def scrape(soup):
    """
    Takes soup obj -> sends to helper functions to obtain info for our data frame
    :param soup: soup object
    :return: roleTitle,company,fullLocation,locationState,
           locationCity,locationZipCode,locationArea,
           salary,minSalary,maxSalary,salaryTimeUnits,
           shortDesc, fullDesc, expressApply,sponsor,indeedURL,
           expLevel,responsiveEmployer,jobType, jobID
    """
    search = soup.find_all("div", {"class": "jobsearch-SerpJobCard unifiedRow row result"})
    print("Number of jobs on page: ", len(search))
    roleTitle = []
    company = []
    fullLocation = []
    locationState = []
    locationCity = []
    locationZipCode = []
    locationArea = []
    salary = []
    minSalary = []
    maxSalary = []
    salaryTimeUnits = []
    shortDesc = []
    expressApply = []
    sponsor = []
    indeedURL = []
    expLevel = []
    jobType = []
    responsiveEmployer = []
    jobID = []

    if search is None:
        return  # might need to return all the lists
    else:
        for job in search:
            roleTitle.append(getRoleTitle(job))
            company.append(getCompany(job))
            locationState.append(getLocationState(job))
            locationCity.append(getLocationCity(job))
            locationZipCode.append(getLocationZipCode(job))
            locationArea.append(getLocationArea(getFullLocation(job)))
            minSalary.append(getMinimumSalary(getSalary(job)))
            maxSalary.append(getMaximumSalary(getSalary(job)))
            salaryTimeUnits.append(getSalaryTimeUnits(getSalary(job)))
            shortDesc.append(getShortDescription(job))
            expressApply.append(getHasExpressApply(job))
            sponsor.append(getIsSponsored(job))
            indeedURL.append(getIndeedJobListingURL(job))
            expLevel.append(getExperienceLevel(URL))  # uses url
            jobType.append(getJobType(URL))  # uses url
            responsiveEmployer.append(getResponsiveEmployer(job))
            jobID.append(getJobID(job))

        return roleTitle, company, fullLocation, locationState, \
               locationCity, locationZipCode, locationArea, \
               salary, minSalary, maxSalary, salaryTimeUnits, \
               shortDesc, expressApply, sponsor, indeedURL, \
               expLevel, jobType, responsiveEmployer, jobID


def jobScrape(url_list):
    app_urls = []
    descriptions = []
    last_updated = []
    has_bullets = []
    gen_bullet_points = []
    good_to_have_bullet_points = []
    required_bullet_points = []

    gen_associated_skills = []
    good_to_have_associated_skills = []
    required_associated_skills = []
    for url in url_list:
        required_skills = []
        good_to_have_skills = []
        skills = []

        required_bullets = []
        good_to_have_bullets = []
        bullets = []
        try:
            html = urlopen(url)  # connects to url
            soup = BeautifulSoup(html.read(), features="lxml")  # gets html
            description = soup.find(id='jobDescriptionText')
            descriptions.append(description)

            app_url = soup.find_all('a', string='Apply On Company Site')
            if not app_url:
                app_urls.append("N/A")
            else:
                app_urls.append(app_url[0].get('href'))

            date = soup.find_all("div", {"class": "jobsearch-JobMetadataFooter"})
            updated = date[0].text
            number = re.findall(r'\d+', updated)
            # print(updated)
            if "Just posted" in updated or "Today" in updated:
                last_updated.append(datetime.today())
            elif "day" in updated and number:
                last_updated.append(datetime.today() - timedelta(days=int(number[0])))
            elif number and int(number[0]) == 30:
                last_updated.append(datetime.today() - timedelta(days=30))
            else:
                last_updated.append("N/A")

            tags_content = [str(tag) for tag in description.find_all()]
            ul_tag = ''
            for tag in tags_content:
                if ul_tag != '' and tag != ul_tag:  # after first iteration, skip to found ul tag
                    continue
                b_instances = tag.count("<b>")
                p_instances = tag.count("<p>")
                ul_tag = ''
                if any(word in tag.lower() for word in gen_headers) and (((tag.lower().startswith('<b>')
                                                                           and tag.lower().endswith(
                            '</b>')) and b_instances == 1 and p_instances == 0) or
                                                                         ((tag.lower().startswith(
                                                                             '<p>') and tag.lower().endswith(
                                                                             '</p>'))) and b_instances == 0 and
                                                                         p_instances == 1):
                    start = tags_content.index(tag)
                    while ul_tag is '':
                        if start == len(tags_content) - 1:
                            break
                        start += 1
                        if tags_content[start].startswith("<ul>") and tags_content[start].endswith("</ul>"):
                            ul_tag = tags_content[start]
                    if ul_tag != '':
                        if any(word in tag.lower() for word in required_headers):
                            required_bullets.append(ul_tag)
                        elif any(word in tag.lower() for word in good_to_have_headers):
                            good_to_have_bullets.append(ul_tag)
                        else:
                            bullets.append(ul_tag)

            appendBulletsAndSkills(required_bullets, required_bullet_points, required_skills)
            appendBulletsAndSkills(good_to_have_bullets, good_to_have_bullet_points, good_to_have_skills)
            appendBulletsAndSkills(bullets, gen_bullet_points, skills)
            checkBullets(required_bullets, good_to_have_bullets, bullets, has_bullets, description, skills)

            if not required_skills:
                required_associated_skills.append("N/A")
            else:
                required_associated_skills.append(required_skills)
            if not good_to_have_skills:
                good_to_have_associated_skills.append("N/A")
            else:
                good_to_have_associated_skills.append(good_to_have_skills)
            if not skills:
                gen_associated_skills.append("N/A")
            else:
                gen_associated_skills.append(skills)
        except urllib.error.URLError as errurl:
            print("URL Error: ", errurl)
        except urllib.error.HTTPError as errh:
            print("HTTP Error: ", errh)
        except urllib.error.ContentTooShortError as errc:
            print("Content Error: ", errc)
    return app_urls, descriptions, gen_bullet_points, good_to_have_bullet_points, required_bullet_points, has_bullets, \
           gen_associated_skills, good_to_have_associated_skills, required_associated_skills, last_updated


def appendBulletsAndSkills(small_bullets, big_bullets, skills_list):
    """
    Checks if there are bullet points or not. If there are bullet points, appends the bullet points and then pulls
    the skills from them.
    :param small_bullets: bullet point list to be appended to the the list of all the jobs' bullet points
    :param big_bullets: bullet points to be appended to the data frame
    :param skills_list: skills associated with the jobs' bullet points (if it has any)
    :return: nothing
    """
    if not small_bullets:
        big_bullets.append("N/A")
    else:
        big_bullets.append(small_bullets)
        for bullet in small_bullets:
            clean_bullet = BeautifulSoup(str(bullet), features='lxml').get_text().lower()
            for skill in skills_labels:
                if skill == 'C++' or skill == 'C#':
                    skill_pattern = re.compile(re.escape(skill), re.IGNORECASE)
                else:
                    skill_pattern = re.compile(r"\b" + re.escape(skill) + r"\b", re.IGNORECASE)
                if skill_pattern.findall(clean_bullet) and skill not in skills_list:
                    skills_list.append(skill)


def checkBullets(required_bullets, good_to_have_bullets, bullets, has_bullets, description, skills):
    """
    Checks if there are any bullet points. If not, pulls the skills from the entire description and appends "False" to
    the has bullet points list. If there are bullet points, appends "True" to the has bullet points list.
    :param required_bullets: bullet points that has a heading indicating that they are required
    :param good_to_have_bullets: bullet points that has a heading indicating that they are good to have
    :param bullets: bullet points that has a heading indicating neither good to have or required.
    :param has_bullets: list that indicates if a job description has bullet points or not.
    :param description: entire HTML description of the job listing
    :param skills: list of skills pulled from the entire description
    :return: nothing
    """
    if not required_bullets and not good_to_have_bullets and not bullets:
        has_bullets.append("False")
        clean_description = BeautifulSoup(str(description), features='lxml').get_text().lower()
        for skill in skills_labels:
            if skill == 'C++' or skill == 'C#':
                skill_pattern = re.compile(re.escape(skill), re.IGNORECASE)
            else:
                skill_pattern = re.compile(r"\b" + re.escape(skill) + r"\b", re.IGNORECASE)
            if skill_pattern.findall(clean_description) and skill not in skills:
                skills.append(skill)
    else:
        has_bullets.append("True")


def get_max_results(url):
    """
    Gets the total number of jobs and pages found from a search on Indeed.
    :param url: indeed URL search
    :return: total number of jobs found
    """

    # page_response = requests.get(url, timeout=3)
    # soup = BeautifulSoup(page_response.content, 'html.parser')

    html = urlopen(url)  # connects to url
    soup = BeautifulSoup(html.read(), features="lxml")  # gets html

    num_jobs_area = soup.find(id='searchCountPages').text.strip()
    # print(num_jobs_area)
    job_numbers = re.findall(r'\d+', num_jobs_area)  # Extract the total jobs found from the search result

    if len(job_numbers) >= 3:  # Have a total number of jobs greater than 1000
        total_num_jobs = (int(job_numbers[1]) * 1000) + int(job_numbers[2])
    else:
        total_num_jobs = int(job_numbers[1])

    print("Number of jobs found: " + str(total_num_jobs) + " jobs" + "\n")
    numPages = round(total_num_jobs / 10) - 1
    return numPages


# -----------------------------------------------------------------------------------------------------------------------
df = pd.DataFrame()
jobDescription_df = pd.DataFrame()
URL = createURL(city=None, state="WA", job="ux ui", job_title=None, explvl="entry level", sort="date")
maxResults = get_max_results(URL)
http = urllib3.PoolManager()

t0 = time.time()
for pages in range(maxResults):
    t1 = time.time()
    nextPage = URL.format(pages * 10)
    print("Working on page: ", pages + 1)
    print("URL being scraped: ", nextPage)
    try:
        html = urlopen(nextPage)  # connects to url
        soup = BeautifulSoup(html.read(), features="lxml")  # gets html

        roleTitle, company, fullLocation, locationState, \
        locationCity, locationZipCode, locationArea, \
        salary, minSalary, maxSalary, salaryTimeUnits, \
        shortDesc, expressApply, sponsor, indeedURL, \
        expLevel, jobType, responsiveEmployer, jobID = scrape(soup)

        applicationURL, jobDescription, genBullets, goodToHaveBullets, requiredBullets, hasBulletPoints, \
        genSkills, goodToHaveSkills, requiredSkills, lastUpdated = jobScrape(indeedURL)

        newData = pd.DataFrame({
            'RoleTitle': roleTitle,
            'Company': company,
            'LocationState': locationState,
            'LocationCity': locationCity,
            'LocationZipCode': locationZipCode,
            'LocationArea': locationArea,
            'MinimumSalary': minSalary,
            'MaximumSalary': maxSalary,
            'SalaryTimeUnits': salaryTimeUnits,
            'ShortDescription': shortDesc,
            'FullDescription': jobDescription,
            'GenBulletPoints': genBullets,
            'GoodToHaveBulletPoints': goodToHaveBullets,
            'RequiredBulletPoints': requiredBullets,
            'HasBulletPoints': hasBulletPoints,
            'GenAssociatedSkills': genSkills,
            'GoodToHaveAssociatedSkills': goodToHaveSkills,
            'RequiredAssociatedSkills': requiredSkills,
            'HasExpressApply': expressApply,
            'IsSponsored': sponsor,
            'IndeedJobListingURL': indeedURL,
            'ApplicationURL': applicationURL,
            'ExperienceLevel': expLevel,
            'JobType': jobType,
            'LastUpdated': lastUpdated,
            'ResponsiveEmployer': responsiveEmployer,
            'JobID': jobID
        })

        df = df.append(newData)

        print("Processing iteration: {} || Completion: {}% ||".format(pages, 100 * pages // maxResults), end="")
        t2 = time.time()
        print(" Iteration time: {}s || Total time: {}s".format(round(t2 - t1, 3), round(t2 - t0, 3)) + "\n")


    except requests.exceptions.HTTPError as errh:
        print("Http error:", errh)
    except requests.exceptions.ConnectionError as errc:
        print("Error connecting:", errc)
    except requests.exceptions.Timeout as errt:
        print("Timeout error:", errt)
    except requests.exceptions.RequestException as err:
        print("Error (unid):", err)
    # except:
    #     df.to_csv("indeedJobs.csv", index=False)

df = df.drop_duplicates(subset="HTMLDescription", keep=False) # remove duplicates
df.to_csv("indeedJobs.csv", index=False) # export dataframe to csv
