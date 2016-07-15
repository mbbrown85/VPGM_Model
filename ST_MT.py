#####################################################################
#       Caluculates the Fm for the single turnover and multiple     #
#       turnover for data from a Fast Repetition Rate Fluorometer.  #
#                                                                   #
#                                                                   #
#####################################################################

import math as math
import re as re
import numpy as np
import matplotlib.pyplot as plt

FILE_NAME_1 = "4_20_16_Stat2_STMT"
#FILE_NAME_2 = "5_25_16_CTD38_Station12_MixLayer.dat"

data_1 = open(FILE_NAME_1)
#data_2 = open(FILE_NAME_2)

st_raw_1 = list()
mt_raw_1 = list()
st_data_1 = list()
mt_data_1 = list()
stmt_range_1 = list()

#st_raw_2 = list()
#mt_raw_2 = list()
#st_data_2 = list()
#mt_data_2 = list()
#stmt_range_2 = list()

Irr_1 = np.array([0,20,40,60,80,100,123,150,177,205,250,300,348,399,448,500])
#Irr_2 = np.array([0,1,2,3,4,5,10,15,20,30,40,50,60,70,80,90,100,125,150,175,200,225,250])

def average(list_name):
    temp_list = list()
    for val in list_name:
        val = float(val)
        temp_list.append(val) 
    num = sum(temp_list)
    den = len(list_name)
    aver = num/den
#    print "Average is" , aver                          #Debugging, to see if the function is correctly outputting a value
    return aver

datapoint = 0
  
for line in data_1:
    begin = re.search('====', line)  
    if begin:
        datapoint = -1
#        print line                                      #Debugging, makes sure the program is selecting the right line
    datapoint = datapoint+1
    if 79 < datapoint < 100:
        st_raw_1.append(line[27:35])
        #for val in st_raw_1:
        #    print val
        #    print type(val)
    elif datapoint == 101:
        aver = average(st_raw_1)
#        print aver                                     #Debugging, makes sure that the return value is getting saved
        st_data_1.append(aver)
    elif datapoint == 102:
        st_raw = list()
#        print st_raw                                   #Debugging, making sure the list is empty before the next set of data
    if 1760 < datapoint < 1780:
        mt_raw_1.append(line[27:35])
    elif datapoint == 1781:
        aver = average(mt_raw_1)
#        print aver                                     #Debugging, makes sure that the return value is getting saved
        mt_data_1.append(aver)         
    elif datapoint == 1782:
        mt_raw_1 = list()
#        print mt_raw                                    #Debugging, makes sure the program is selecting the right line

#for line in data_2:
#    begin = re.search('====', line)  
#    if begin:
#        datapoint = -1
#        print line                                      #Debugging, makes sure the program is selecting the right line
#    datapoint = datapoint+1
#    if 79 < datapoint < 101:
#        st_raw_2.append(line[28:35])
#    elif datapoint == 101:
#        aver = average(st_raw_2)
#        print aver                                     #Debugging, makes sure that the return value is getting saved
#        st_data_2.append(aver)
#    elif datapoint == 102:
#        st_raw_2 = list()
#        print st_raw                                   #Debugging, making sure the list is empty before the next set of data
#    if 1560 < datapoint < 1580:
#        mt_raw_2.append(line[28:35])
#    elif datapoint == 1581:
#        aver = average(mt_raw_2)
#        print aver                                     #Debugging, makes sure that the return value is getting saved
#        mt_data_2.append(aver)         
#    elif datapoint == 1582:
#        mt_raw_2 = list()
#        print mt_raw                                    #Debugging, makes sure the program is selecting the right line


st_array_1 = np.asarray(st_data_1)
mt_array_1 = np.asarray(mt_data_1)
#st_array_2 = np.asarray(st_data_2)
#mt_array_2 = np.asarray(mt_data_2)

stmt_range_1 = np.divide(st_array_1, mt_array_1)
#stmt_range_2 = np.divide(st_array_2, mt_array_2)
print st_array_1
print mt_array_1
print stmt_range_1
#print stmt_range_2

print len(Irr_1)
print len(stmt_range_1)
plt.plot(Irr_1, stmt_range_1, 'g^')
plt.xlabel("Irradiance")
plt.ylabel("ST/MT")
plt.show()


