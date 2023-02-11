#!/usr/bin/python
import os
import pandas as pd
 
# fileitem = form['upload/input_test']
 
# check if the file has been uploaded
# if fileitem.filename:
    # strip the leading path from the file name
    # fn = os.path.basename(fileitem.filename)

    # df  = pd.read_csv("/upload/" + fn )
df  = pd.read_csv("App/uploads/input_test.csv")

dfd = df.drop(['Name','Assignment','Name reviewer1','Name reviewer2','Name reviewer3'], axis='columns')
# print(dfd)
ambi = []
sus = []
bad = []

    
for i in range(0,len(dfd)):
    # print(dfd)
    # dfS = dfd.sort_values(i,axis=0, ascending=False)    #sort by row)
    dfS = []
    dfS.append(dfd.iloc[i][0])
    dfS.append(dfd.iloc[i][1])
    dfS.append(dfd.iloc[i][2])
    dfS.sort(reverse=True)
    # print(dfS)
    a = dfS[0] - dfS[1]
    b = dfS[1] - dfS[2]

    # print(a)
    # print(b)   

    
    if 1 >= abs(a-b) >= 0:
        if dfS[0] - dfS[1] != 0 and  dfS[1] - dfS[2] != 0:   #find ambigious
            ambi.append(df.iloc[i])
    elif (a+b) >=3:     #still improving
        sus.append(df.iloc[i])      #find sus
        if a>b :
            bad.append(dfS[0])
        elif b>a:
            bad.append(dfS[2])









# print(len(df))
# print(df.iloc[0][4])

print("ambi : " , ambi)
print()
print("sus : " , sus)
print()
print("bad : " , bad)

ambi = pd.DataFrame(ambi)
sus = pd.DataFrame(sus)
#write csv
ambi.to_csv('ambigious.csv', index=False)
sus.to_csv('suspect.csv', index=False)

     
   # open read and write the file into the server
    # open(fn, 'wb').write(fileitem.file.read())