import pandas as pd
from bs4 import BeautifulSoup
from urllib.request import urlopen
import urllib
import re

gen_headers = ['qualifications', 'qualified', 'skills', 'responsibilities', 'duties', 'abilities', 'experience']
required_headers = ['required', "must have", "essential", "needed", "minimum", "require"]
good_to_have_headers = ['preferred', "good to have", "at least", "nice to have"]
skills_labels = ["Abstraction", "Accounting Software", "Administration", "Adobe Creative Suite (Photoshop, InDesign, "
                                                                         "etc.)", "Agile Scrum Team", "Algorithms",
                 "Amazon web services", "Analytical Skills", "Analytics", "Android Development", "Angular and Node "
                                                                                                 "Apps", "AngularJS",
                 "Any use of data to explore a problem or make a decision", "Api", "APL", "Application", "Application "
                                                                                                         "Development",
                 "Applications", "Architecture", "Artificial Intelligence", "Authentication Systems", "Aws", "Azure",
                 "Backend", "Bash", "Big Data", "Blender", "Blueprint Design", "C", "C Language", "C#/.Net", "C++",
                 "Caffe", "Calculating", "Caml", "Certification", "Certifications", "Chemistry", "Clang", "Clojure",
                 "Cloud Applications, such as JSON, Rest, and RPC", "Cloud Architecture", "Cloud Computing",
                 "Cloud Middleware Technologies", "Cloud Services", "Cloud Systems Administration",
                 "Cloud/SaaS Services", "Cloudkit", "Cms", "Coding", "Compiler", "Compiling", "Compiling Statistics",
                 "Complex problem solving", "Computer Architecture", "Computing", "Configuration", "Critical thinking",
                 "Cryptography", "CSS", "CSS3", "Cuda", "Customer Relationship Management (CRM)", "Customer Support",
                 "Cyber Security", "Data Analytics", "Data engineering", "Data Mining", "Data presentation",
                 "Data Structures", "Database", "Database architecture", "Database Design", "Database Management",
                 "Database Software", "Debug", "Debugger", "Debugging", "Deductive reasoning", "Deep learning",
                 "Design", "Design reviews", "Development",
                 "Digital Product Design Software, such as InVision and Zeppelin", "Docker", "Documentation",
                 "Electrical", "Elixir", "Encapsulation", "Encryption Algorithms", "Engineer", "Engineering",
                 "Enterprise Resource Planning (ERP) Software", "Enzyme", "Flow", "Fortran", "Frontend", "Full stack",
                 "Functionality", "Go", "Golang", "Hardware", "Hardware Description Language (HDL)",
                 "Hardware Verification Tools and Techniques", "Haskell", "HTML", "HTML5", "Human Resources Software",
                 "ICT (Information and Communications Technology)", "Immutable.js", "Implementation",
                 "Inductive reasoning", "Information Management", "Information ordering", "Information Security",
                 "Information Technology", "Infrastructure", "Inheritance", "Installation", "Instructing", "Intellij",
                 "Inventory Management", "iOS App Development", "IP Setup", "Java", "JavaScript", "Jest", "Junit",
                 "Jupyter notebook", "Kaggle", "Kali", "Keras", "Kernal", "Kotlin", "Kubernetes", "Languages", "Latex",
                 "Linux", "Linux/Unix", "Lisp", "Logical thinking", "Lua", "Machine learning", "Maintenance",
                 "Manufacturing", "Markdown", "Markup", "Mathematical reasoning", "Mathematics", "Mean",
                 "Mechanical Maintenance", "Medical Billing", "Medical Coding", "Microsoft Office Certifications",
                 "Microsoft Office Suite", "Modeling", "Modification", "Mysql", "Natural language processing",
                 "Needs Analysis", "Network", "Network Architecture", "Network Security", "Networking",
                 "Networking Communication", "Neural", "New Technologies", "Node.js", "Nosql", "Numeracy",
                 "Object-oriented programming", "Objective-C", "Oop", "Opencv", "Opengl", "Operating Systems",
                 "Operation monitoring", "Optimization", "Oracle", "Pascal", "Perl", "Persuasion", "PHP", "Phpmyadmin",
                 "Physics", "Pivot tables", "Polymorphism", "Powershell", "Process analysis", "Product enhancement",
                 "Productivity Software", "Programming", "Pycharm", "Python", "Pytorch", "Quantitative Reports",
                 "Quantitative Research", "Query Software", "R", "React", "ReactJS", "Redux", "Regression", "Repairing",
                 "Resource management", "Rest", "Restful", "Restoration", "Risk Assessment", "Ruby", "SaaS", "Sass",
                 "Scala", "Scratch", "scripting", "SCSS", "Sdk", "Security", "Servers", "Shell", "Social media",
                 "Socket", "Software", "Software Revision Control Systems", "Solution Delivery", "Sonography",
                 "Source Code", "SQL", "Sql server", "SSH", "Statistical Analysis", "Storage",
                 "Storage and Data Management", "Strategic planning", "Structural Analysis", "Structures", "Study",
                 "Swift", "Systems Analysis", "Systems evaluation", "Tcl", "Technical", "Technical Support",
                 "Technology", "Telecommunications", "Tensor", "Tensorflow", "Test", "Testing", "Tools", "Training",
                 "Troubleshooting", "Ubuntu", "UI Toolkits and Frameworks", "Uikit", "Unity", "Usability",
                 "User Experience (UX) Design", "User Interface (UI) Design", "UX Design", "Version Repository",
                 "Video Creation", "Virtual and Host-based Firewalls", "Vision", "Visual Basic", "Vue", "Web API",
                 "Web Architecture and Development Framework", "web scraping", "Wireless Modems/Routers", "Writing"]


# def getSkills(file_name):
#     data = pd.read_csv(file_name)
#     url_column = data["IndeedJobListingURL"]  # gets url column from .csv file
#     indeed_urls = url_column.tolist()
#
#     base_url = 'https://www.indeed.com/'
#     urls = []
#     headings = []
#     specific_bullets = []
#     associated_skills = []
#     has_bullets = []
#     descriptions = []
#
#     job_num = 1
#     for url in indeed_urls:
#         if (job_num == 1):
#             print("Working on the first 10 jobs...")
#         elif ((job_num % 10) == 0):
#             print("Working on the next 10 jobs...")
#
#         bullets = []
#         url_heading = []
#         skills = []
#
#         try:
#             urls.append(base_url + url)
#             response = urlopen(base_url + url)  # connects to url
#             soup = BeautifulSoup(response.read(), features="lxml")  # gets html
#             description = soup.find(id='jobDescriptionText')
#             descriptions.append(description)
#             bullet_points = description.select('p + ul')  # gets bullet points right after a <p> tag
#             # section_headers = description.findAll(re.compile(r"^h"), {"class": "jobSectionHeader"})  # header tags
#             # for header in section_headers:
#             #     print(header.next_sibling)
#             # print(sibling)
#             if not bullet_points:
#                 has_bullets.append("False")
#                 clean_description = BeautifulSoup(str(description), features='lxml').get_text().lower()
#                 for skill in skills_labels:
#                     if skill.lower() in clean_description and skill not in skills:
#                         skills.append(skill)
#             else:
#                 has_bullets.append("True")
#                 for bullet in bullet_points:
#                     head = bullet.previous_sibling
#                     clean_head = BeautifulSoup(str(head), features='lxml').get_text()
#                     clean_bullet = BeautifulSoup(str(bullet), features='lxml').get_text().lower()
#                     if any(word in clean_head.lower() for word in key_words):
#                         url_heading.append(clean_head)
#                         bullets.append(bullet)
#                         for skill in skills_labels:
#                             if skill.lower() in clean_bullet and skill not in skills:
#                                 skills.append(skill)
#             if not url_heading:
#                 headings.append("N/A")
#             else:
#                 headings.append(url_heading)
#             if not bullets:
#                 specific_bullets.append("N/A")
#             else:
#                 specific_bullets.append(bullets)
#             if not skills:
#                 associated_skills.append("N/A")
#             else:
#                 associated_skills.append(skills)
#         except urllib.error.URLError as errurl:
#             print("URL Error: ", errurl)
#         except urllib.error.HTTPError as errh:
#             print("HTTP Error: ", errh)
#         except urllib.error.ContentTooShortError as errc:
#             print("Content Error: ", errc)
#         # except:
#         #     specific_bullets.append("N/A")
#         #     headings.append("N/A")
#         #     associated_skills.append("N/A")
#
#         job_num += 1
#
#     df = pd.DataFrame({
#         'URL': urls,
#         'HTMLDescription': descriptions,
#         'HeadingsForBulletPoints': headings,
#         'RelevantHTMLBulletPoints': specific_bullets,
#         'AssociatedSkills': associated_skills,
#         'HasRelevantBulletPoints': has_bullets
#     })
#
#     return df

def getSkills(file_name):
    """
    Pulls the skills from either the bullet points or entire description depending on if the job listing has
    bullet points or not. Also, differentiates between bullets as "good to have" and "required," which then
    differentiates skills between "good to have" and "required", as well.
    :param file_name: data set
    :return: data frame of Indeed URLs, general bullet points, good to have bullet points, required bullet points,
    general skills, good to have skills, required skills, if the description has bullet points, and the entire job
    listing's description.
    """
    data = pd.read_csv(file_name)
    url_column = data["IndeedJobListingURL"]  # gets url column from .csv file
    indeed_urls = url_column.tolist()
    urls = []

    gen_bullet_points = []
    good_to_have_bullet_points = []
    required_bullet_points = []

    gen_associated_skills = []
    good_to_have_associated_skills = []
    required_associated_skills = []

    has_bullets = []
    descriptions = []

    job_num = 1
    for url in indeed_urls:
        if (job_num == 1):
            print("Working on the first 10 jobs...")
        elif ((job_num % 10) == 0):
            print("Working on the next 10 jobs...")
        required_skills = []
        good_to_have_skills = []
        skills = []

        required_bullets = []
        good_to_have_bullets = []
        bullets = []
        try:
            urls.append(url)
            response = urlopen(url)  # connects to url
            soup = BeautifulSoup(response.read(), features="lxml")  # gets html
            description = soup.find(id='jobDescriptionText')
            descriptions.append(description)
            tags_content = [str(tag) for tag in description.find_all()]
            ul_tag = ''
            for tag in tags_content:
                if ul_tag != '' and tag != ul_tag:  # after first iteration, skip to found ul tag
                    continue
                b_instances = tag.count("<b>")
                p_instances = tag.count("<p>")
                ul_tag = ''
                if any(word in tag.lower() for word in gen_headers) and (((tag.lower().startswith('<b>')
                    and tag.lower().endswith('</b>')) and b_instances == 1 and p_instances == 0) or
                    ((tag.lower().startswith('<p>') and tag.lower().endswith('</p>'))) and b_instances == 0 and
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

        job_num += 1

    df = pd.DataFrame({
        'URL': urls,
        'HTMLDescription': descriptions,
        'GenBulletPoints': gen_bullet_points,
        'RequiredBulletPoints': required_bullet_points,
        'GoodToHaveBulletPoints': good_to_have_bullet_points,
        'GenAssociatedSkills': gen_associated_skills,
        'RequiredAssociatedSkills': required_associated_skills,
        'GoodToHaveAssociatedSkills': good_to_have_associated_skills,
        'HasBulletPoints': has_bullets
    })

    return df


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


test = getSkills("indeedJobs_WA_uxui_entrylevel.csv")
# print(test)
test.to_csv("test.csv", index=None)
