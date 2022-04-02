import re
import pandas as pd
import numpy as np

filename1 = f'/XMI_1.xmi'
filename2 = f'/XMI_2.xmi'

file = [filename1,filename2]

typedf = []
iddf = []
namedf = []
for i in file:
    with open(i) as file:
        for line in file:
            try:
                type = re.findall(r"xmi:type = \"(.*?)\"", line)[0]

                name = re.findall(r"name = \"(.*?)\"", line)[0]
            except:
                type = ""
                name = ""

            typedf.append(type)

            namedf.append(name)
print(typedf)
print(namedf)
            #print(type,id,name)

df = pd.DataFrame(data={'Type': typedf, 'Name':namedf})
df['Type'].replace('', np.nan, inplace=True)
df['Name'].replace('', np.nan, inplace=True)
df = df.dropna()

df = df.drop_duplicates(keep=False)

print(df)