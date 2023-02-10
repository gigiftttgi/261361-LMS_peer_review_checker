#!/usr/bin/python
import os
import pandas as pd
 
# read file
df  = pd.read_csv("uploads/test2.csv")
ambi = []
sus = []

print(df.iloc[0][3])
print(df.iloc[0][5])
print(df.iloc[0][7])

for i in range(0,len(df)):
    # เป็น ambigious
    if 1 >= abs((abs(df.iloc[i][3] - df.iloc[i][5])) - (abs(df.iloc[i][5] - df.iloc[i][7]))) :
        ambiatt = []
        for j in range(8) : 
            ambiatt.append(df.loc[i][j])
        ambi.append(ambiatt)
        # for j in range(8) : 
        #     ambiatt.append(df.loc[i][j])

print(ambi)
# print("ambi : " + ambi)
# print("sus : " + sus)
    
    #write csv
ambi.to_csv('ambigious.csv', index=False, header=False)
# sus.to_csv('suspect.csv', index=False, header=False)

     
   # open read and write the file into the server
    # open(fn, 'wb').write(fileitem.file.read())