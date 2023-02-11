#!/usr/bin/python
import os
import pandas as pd
 
# fileitem = form['upload/input_test']
 
# # check if the file has been uploaded
# if fileitem.filename:
#     # strip the leading path from the file name
#     fn = os.path.basename(fileitem.filename)
#     print(fn)
#     df  = pd.read_csv("/upload/" + fn )

df  = pd.read_csv("uploads/input.csv")
dff  = pd.read_csv("uploads/test2.csv")

dfd = df.drop(['Name','Assignment','Name reviewer1','Name reviewer2','Name reviewer3'], axis='columns')

# l1 = ['Name', 'Assignment', 'Name reviewer1', 'Review score1', 'Name reviewer2', 'Review score2', 'Name reviewer3', 'Review score3']
# l2 = list(dff.columns)
# print (list(df.columns))
# print (list(dff.columns))
# print( l1 == l2)
# print(dfd)
ambi = []
sus = []
bad = []

    
for i in range(0,len(dfd)):
    #sort
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
            ambi.append(df.iloc[i].values)
    elif (a+b) >=3:     #still improving
        sus.append(df.iloc[i])      #find sus
        if a>b :
            bad.append(dfS[0])
        elif b>a:
            bad.append(dfS[2])


print("ambi")
print(ambi[0])

ambi = pd.DataFrame(ambi)
sus = pd.DataFrame(sus)

print("ambi")
print(ambi.to_string(index=False, index_names=False))

#write csv
sus.to_csv('suspect.csv', index=False)
ambi.to_csv('ambigious.csv', index=False)

#read sus.csv
sus  = pd.read_csv("suspect.csv")

#Map bad from sus.csv
name = []
asn = []
bname = []
bscore = []
for i in range(len(sus)):
    name.append(sus.iloc[i]['Name'])
    asn.append(sus.iloc[i]['Assignment'])
    if(sus.iloc[i]['Review score3'] == bad[i] ):
        bname.append(sus.iloc[i]['Name reviewer3'])
        bscore.append(sus.iloc[i]['Review score3'])
    elif(sus.iloc[i]['Review score2'] == bad[i]):
        bname.append(sus.iloc[i]['Name reviewer2'])
        bscore.append(sus.iloc[i]['Review score2'])  
    elif(sus.iloc[i]['Review score1'] == bad[i]):
        bname.append(sus.iloc[i]['Name reviewer1'])
        bscore.append(sus.iloc[i]['Review score1'])


bad_review = {
    'Name' : name,
    'Assignment' : asn,
    'Bad Reviewer' : bname,
    'Score' : bscore
}

bad = pd.DataFrame(bad_review)
print( "bad")
print( bad.to_string(header=None, index=False))
b = bad.to_string(header=None, index=False)
b = b.replace("\n",",")
b = b.replace(" ",",")
print(b)

bad.to_csv('bad_reviewer.csv', index=False)

     
   # open read and write the file into the server
    # open(fn, 'wb').write(fileitem.file.read())