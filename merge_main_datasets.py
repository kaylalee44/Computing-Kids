import pandas as pd

# DF1 = pd.read_csv("indeedJobsHalfUnknownsRemoved.csv")
# DF2 = pd.read_csv("indeedJobs2.csv")
# DF2.append(DF1)
#
# DF2.to_csv('indeedJobsHello.csv',index=False)

DF1 = pd.read_csv("data_commission.csv")
DF2 = pd.read_csv("data_contract.csv")
DF3 = pd.read_csv("data_internship.csv")
DF4 = pd.read_csv("data_parttime.csv")
DF5 = pd.read_csv("data_temporary.csv")
DF6 = pd.read_csv("data_fulltime_part1.csv")

DF1 = DF1.append(DF2)
DF1 = DF1.append(DF3)
DF1 = DF1.append(DF4)
DF1 = DF1.append(DF5)
DF1 = DF1.append(DF6)

DF1.to_csv('indeedJobs_WA_alljobtypes_entrylevel_date.csv',index=False)
