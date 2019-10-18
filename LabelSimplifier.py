#varName = [parent, child1,child2,childN...]

# def get_Parent_Title(predicted, generalJobTitlesDF):
#     #removed game designer(111)
#     softwareEngineer = ['Software Engineer',60,21,43,137,29,16,44,61,71,73,131,82,141,106,116,129,80,58,22,36]
#
#     #removed 133 & 136, web admin & web master
#     webDeveloper = ['Web Developer',118,93,117]
#
#     networkEngineer = ['Network Engineer',69,42,46,53,81,101]
#
#     it = ['IT',2,7,13,96,109,125,33,95,4,6,14,20,35,38,56,108,110,47,40,130,48]
#
#     dataEngineer = ['Data Engineer',104,103,92,121,34,114,99,5,122,]
#
#     analyst = ['Analyst', 140, 67, 9, 23, 45, 59, 79, 115, 124]
#
#     ui_ux = ['UI/UX', 24,78,77,84,120,147,97,119,148,52,126,113]
#
#     dataScientist = ['Data Scientist',41,87]
#
#     cyberSecurity = ['Cyber Security',100,94,26,54]
#
#     testEngineer = ['Test Engineer',107,57,25]
#
#     allMyJobLabels = [softwareEngineer,webDeveloper, networkEngineer,it,dataEngineer, ui_ux,dataScientist,analyst,cyberSecurity,testEngineer]
#
#     for currentList in allMyJobLabels:
#         if predicted in currentList[1:]:
#             #print('CNN:',predicted)
#             #print('adjusted:',currentList[0])
#             return currentList[0]
#         else:
#             #print('CNN:',predicted)
#
#             return generalJobTitlesDF['job_title'][predicted]
import pandas as pd
generalJobTitlesDF = pd.read_csv("Job_title.csv")

def get_Parent_Title(predicted,generalJobTitlesDF):
    softwareEngineer = ['Software Engineer',58,19,41,135,27,14,42,59,69,71,129,80,139,104,114,127,78,56,20,34]

    webDeveloper = ['Web Developer',116,91,115]

    networkEngineer = ['Network Engineer',67,40,44,51,79,99]

    it = ['IT',0,5,11,94,107,123,31,93,2,4,12,18,33,36,54,106,108,45,38,128,46]

    dataEngineer = ['Data Engineer',102,101,90,119,32,112,97,3,120]

    analyst = ['Analyst',138,65,7,21,43,57,77,113,122]

    ui_ux = ['UI/UX',22,76,75,82,118,145,95,117,146,50,124,111]

    dataScientist = ['Data Scientist',39,85]

    cyberSecurity = ['Cyber Security',98,92,24,52]

    testEngineer = ['Test Engineer',105,55,23]

    allMyJobLabels = [softwareEngineer,webDeveloper, networkEngineer,it,dataEngineer, ui_ux,dataScientist,analyst,cyberSecurity,testEngineer]

    countLists = len(allMyJobLabels)
    counter = 0

    for currentList in allMyJobLabels:
        counter+=1
        if predicted in currentList[1:]:
            return currentList[0]
        if counter == countLists:
            return generalJobTitlesDF['job_title'][predicted]

a = get_Parent_Title(120,generalJobTitlesDF)
print(a)