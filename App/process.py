#!/usr/bin/python
import os
import pandas as pd
 
# fileitem = form['upload/input_test']
 
# check if the file has been uploaded
# if fileitem.filename:
    # strip the leading path from the file name
    # fn = os.path.basename(fileitem.filename)

    # df  = pd.read_csv("/upload/" + fn )
df  = pd.read_csv("uploads/input_test.csv")
ambi = []
sus = []

    
# for i in range(0,len(df)):
#     dfS = df.sort_values(by=i, axis=1, ascending=False)    #sort by row
#     if 1 <= abs((dfS.iloc[i][0] - dfS.iloc[i][1]) - (dfS.iloc[i][1] - dfS.iloc[i][2])) :    #find ambigious
#         ambi.append(df.iloc[i])
#     elif (dfS.iloc[i][0] - dfS.iloc[i][1]) + (dfS.iloc[i][1] - dfS.iloc[i][2]) >=3:     #still improving
#         sus.append(df.iloc[i])      #find sus


# for i in range(1,len(df)):
#     # dfS = df.sort_values(by=i, axis=1, ascending=False)    #sort by row
#     if 1 <= abs(abs(df.iloc[i][4] - df.iloc[i][6]) - abs(df.iloc[i][6] - df.iloc[i][8])) :    #find ambigious
#         ambi.append(df.iloc[i])
#     elif (df.iloc[i][4] - df.iloc[i][6]) + (df.iloc[i][6] - df.iloc[i][8]) >=3:     #still improving
#         sus.append(df.iloc[i])      #find sus

print(len(df))
print(df.iloc[0][4])

# print("ambi : " + ambi)
# print("sus : " + sus)
    
    #write csv
# ambi.to_csv('ambigious.csv', index=False, header=False)
# sus.to_csv('suspect.csv', index=False, header=False)

     
   # open read and write the file into the server
    # open(fn, 'wb').write(fileitem.file.read())