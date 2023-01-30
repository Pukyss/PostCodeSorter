
#python script
import pandas as pd
import re
import os

wrongPostCode =  bool(0)

def ValidateWrongPostCode(input):
    #Code translation:
    #[0-9] 0 to 9
    #[A-Z] any letter from a to z
    #{1-2} followed by a one or two-digit number
    #[0-9R] 0 to 9 or escape
    #[0-9A-Z]? match 0 to 9 or A to Z
    #[ABD-HJLNP-UW-Z]{2}$  must be two letters at the end of the string.
    return bool (re.match(r"^[A-Z]{1,2}[0-9R][0-9A-Z]? [0-9][ABD-HJLNP-UW-Z]{2}$",input))

#Philes location
dataPath = str('C:\code\PostCodeSorter\csv')
a = str('')

#File path check
if not os.path.exists(dataPath + r'\solution'):
    os.makedirs(dataPath + r'\solution')

#adds samples from CSV to data frame.
df = pd.read_csv(dataPath + '\InputFile.csv',encoding='cp1252', header=None, names=['PC'])
dfLondonPostCodes = pd.read_csv(dataPath + '\LondonPostcodes.csv',encoding='cp1252', header=None, names=['PC'])

#creates data frames for solution
dfBadPC = pd.DataFrame(columns=['PC'])

i = int(len(df)) -1
while  i > -1:
    wrongPostCode = ValidateWrongPostCode(df.iloc[i, 0])
    if wrongPostCode == 0:
        dfBadPC.loc[len(dfBadPC.index)] = [df.iloc[i, 0]]
        df.drop([i], axis = 0,inplace=True)
    i -= 1

dfBadPC.to_csv(dataPath + r'\solution\IncorrectPostCodes.csv', index=False, encoding='cp1252', header=None)

#inner join to find all London post codes
dfLondPC = pd.merge(dfLondonPostCodes,df,on='PC',how="inner")

#Join data frames and resets indexes
dfOtherPC = pd.concat([dfLondPC, df], ignore_index=True)
#removes all dublicates in data frame
dfOtherPC.drop_duplicates(subset="PC", keep=False, inplace=True)

dfLondPC.to_csv(dataPath + r'\solution\LondonPostCodes.csv', index=False, encoding='cp1252', header=None)
dfOtherPC.to_csv(dataPath + r'\solution\OtherPostCodes.csv', index=False, encoding='cp1252', header=None)