import pandas as pd

myDF = pd.read_csv("indeedJobs_WA_fulltime_entrylevel combined.csv")
df1 = pd.read_csv("indeedJobs_WA_temporary_entrylevel.csv")
df2 = pd.read_csv("indeedJobs_WA_commission_entrylevel.csv")
df3 = pd.read_csv("indeedJobs_WA_contract_entrylevel.csv")
df4 = pd.read_csv("indeedJobs_WA_internship_entrylevel.csv")
df5 = pd.read_csv("indeedJobs_WA_parttime_entrylevel.csv")
# df5 = pd.read_csv("indeedJobs_WA_developer_entrylevel.csv")
# df6 = pd.read_csv("indeedJobs_WA_informationsecurity_entrylevel.csv")
# df7 = pd.read_csv("indeedJobs_WA_software_entrylevel.csv")
# df8 = pd.read_csv("indeedJobs_WA_softwaredeveloper_entrylevel.csv")
# df9 = pd.read_csv("indeedJobs_WA_softwareengineer_entrylevel.csv")
# df10 = pd.read_csv("indeedJobs_WA_uidesigner_entrylevel.csv")
# df11 = pd.read_csv("indeedJobs_WA_uxdesigner_entrylevel.csv")
# df12 = pd.read_csv("indeedJobs_WA_uxui_entrylevel.csv")
# df13 = pd.read_csv("indeedJobs_WA_webdeveloper_entrylevel.csv")
# df14 = pd.read_csv("indeedJobs_WA_engineer_entrylevel.csv")
# df15 = pd.read_csv("indeedJobs_WA_artificialintelligence_entrylevel.csv")
# df16 = pd.read_csv("indeedJobs_WA_interactiondesigner_entrylevel.csv")
# df17 = pd.read_csv("indeedJobs_WA_applicationarchitect_entrylevel.csv")
# df18 = pd.read_csv("indeedJobs_WA_computerprogrammer_entrylevel.csv")
# df19 = pd.read_csv("indeedJobs_WA_userexperience_entrylevel.csv")
# df20 = pd.read_csv("indeedJobs_WA_cybersecurity_entrylevel.csv")
# df21 = pd.read_csv("indeedJobs_WA_systems_entrylevel.csv")
# df22 = pd.read_csv("indeedJobs_WA_programmer_entrylevel.csv")

myDF = myDF.append(df1)
myDF = myDF.append(df2)
myDF = myDF.append(df3)
myDF = myDF.append(df4)
myDF = myDF.append(df5)
# myDF = myDF.append(df6)
# myDF = myDF.append(df7)
# myDF = myDF.append(df8)
# myDF = myDF.append(df9)
# myDF = myDF.append(df10)
# myDF = myDF.append(df11)
# myDF = myDF.append(df12)
# myDF = myDF.append(df13)
# myDF = myDF.append(df14)
# myDF = myDF.append(df15)
# myDF = myDF.append(df16)
# myDF = myDF.append(df17)
# myDF = myDF.append(df18)
# myDF = myDF.append(df19)
# myDF = myDF.append(df20)
# myDF = myDF.append(df21)
# myDF = myDF.append(df22)

myDF.to_csv('indeedJobs.csv', index=False)
# print(myDF.shape)

# df = pd.read_csv("indeedJobs_WA_commission_entrylevel_date.csv")
# genSkills = df['GenSkills']
# goodSkills = df['GoodToHaveSkills']
# requiredSkills = df['RequiredSkills']
# df2 = pd.DataFrame()
# for list in genSkills:
#     for skill in list:


