import pandas as pd


df1 = pd.read_csv("C:/Users/a.vivek/Desktop/Projects/Calgary/Final Files/Job Specific/Second Run/software developer.csv")
df2 = pd.read_csv("C:/Users/a.vivek/Desktop/Projects/Calgary/Final Files/Job Specific/Second Run/software engineer.csv")

df = pd.concat([df1,df2])
print (df.columns.tolist())
print (len(df1))
print (len(df2))
print (len(df))

#df_uniq = df.drop_duplicates(subset=['Job_Url'],keep="first",inplace=False)
df_uniq = df.drop_duplicates(subset=['Job_Description'])

print (len(df_uniq))


#df = pd.DataFrame({"A":["foo", "foo", "foo", "bar"], "B":[0,1,1,1], "C":["A","A","B","A"]})
#print (df.drop_duplicates(subset=['A', 'C'], keep="first",inplace=False))

job_desc = df["Job_Description"]
df_dups =  (df[job_desc.isin(job_desc.duplicated())])
print (len(df_dups))
df_dups.to_csv("Duplicates.csv", encoding='utf-8')

df_dups1 = pd.concat(g for _, g in df_uniq.groupby("Job_Description") if len(g) > 1)
print (len(df_dups1))
df_dups1.to_csv("Duplicates.csv", encoding='utf-8')