import glob
path = 'C:/Users/a.vivek/Desktop/Projects/Calgary/Final Files/Job Specific/Second Run/*'
files = glob.glob(path)
for file in files:
    print (file)