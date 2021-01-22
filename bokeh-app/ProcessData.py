import os
import numpy as np
import pandas as pd
# run this before sharing the binder bokeh app
# For all rent 
DIRECTORY_PATH = "./raw_data/renta"
DIRECTORY_PATH2 = "./raw_data"
files = [ file_path  for _, _, file_path in os.walk(DIRECTORY_PATH)]


numberList = [item.replace('renta', '') for item in files[0]]
numberList = [item.replace('.txt', '') for item in numberList]
numberList = [int(item) for item in numberList]

numberList = np.array(numberList)
#print("Min date = {:d}".format(numberList.min()))
#print("Max date = {:d}".format(numberList.max()))

print("Min date = {min}, Max date = {max}.".format(min = numberList.min(), max = numberList.max()))

all_df_dict = {}
kk = 0 
for file in files[0]:
    filePath = DIRECTORY_PATH + '/' + file
    df = pd.read_table(filePath, sep = ',')
    all_df_dict.update({str(kk): df})
    kk += 1
    
np.save(DIRECTORY_PATH2 +'/my_file_all.npy', all_df_dict) 
#read_dictionary = np.load(DIRECTORY_PATH2 +'/my_file_all.npy',allow_pickle='TRUE').item()


# By sex 
for ii in range(0,2):
    DIRECTORY_PATH = "./raw_data/renta - sexo/" + str(ii) 
    DIRECTORY_PATH2 = "./raw_data"
    files = [ file_path  for _, _, file_path in os.walk(DIRECTORY_PATH)]

    numberList = [item.replace('renta', '') for item in files[0]]
    numberList = [item.replace('.txt', '') for item in numberList]
    numberList = [int(item) for item in numberList]

    numberList = np.array(numberList)
    print("Min date = {min}, Max date = {max}.".format(min = numberList.min(), max = numberList.max()))

    all_df_dict = {}
    kk = 0 
    for file in files[0]:
        filePath = DIRECTORY_PATH + '/' + file
        df = pd.read_table(filePath, sep = ',')
        df['sex'] = str(ii)
        all_df_dict.update({str(kk): df})
        kk += 1
    
    np.save(DIRECTORY_PATH2 +'/my_file_all'+ str(ii)+'.npy', all_df_dict) 
    #read_dictionary = np.load(DIRECTORY_PATH2 +'/my_file_all'+ str(ii)+'.npy',allow_pickle='TRUE').item()
