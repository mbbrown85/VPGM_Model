#############################################################################
#   This program calculates primary productivity based on the VGPM model    # 
#   from Behrenfeld and Falkowski 1997.  Raw data is taken from hdf files   #
#   from satellite measurements of sea surface temperature, chlorophyll,    #
#   and PAR.  These files can be found on the Ocean Productivity website    #
#   at www.science.oregonstate.edu/ocean.productivity.                      #
#                                                                           #
#   Program requires Python, numpy, pyhdf and the HDF4 libraries.  Pyhdf    #
#   for Windows can be found at the following site:                         # 
#   http://www.lfd.uci.edu/~gohlke/pythonlibs/                              #
#   Take note of which Python version you're running and download the       #
#   appropriate file (the numbers following cp is the version).  Numpy can  #
#   be downloaded individually, or found through distributions like         #
#   Anaconda.  The hdf4 libraries are availble for download via the HDF     # 
#   Group.                                                                  #                                       
#############################################################################

import numpy as np
import re as re
from pyhdf.SD import SD, SDC
    
FILE_NAME_1 = "C:\Anaconda\envs\sat_data\HDF_files\Chl\chl.2015001.hdf"
FILE_NAME_2 = "C:\Anaconda\envs\sat_data\HDF_files\PAR\par.2015001.hdf"
FILE_NAME_3 = "C:\Anaconda\envs\sat_data\HDF_files\SST\sst.2015001.hdf"

chl_hdf = SD(FILE_NAME_1)   #extract data in SD format
par_hdf = SD(FILE_NAME_2)   #extract data in SD format
sst_hdf = SD(FILE_NAME_3)   #extract data in SD format

chl_sds = chl_hdf.select('chl')  #select SD data
par_sds = par_hdf.select('par')  #select SD data 
sst_sds = sst_hdf.select('sst')  #select SD data

chl_data = chl_sds.get()    #convert data to np.array format
par_data = par_sds.get()    #convert data to np.array format
sst_data = sst_sds.get()    #convert data to np.array format

ser = re.search('\d{7}', FILE_NAME_1)
date = str(ser.group())
day = int(date[4:7]) + 2


################################################################ 
#  Calculates optical depth from sst for each pixel using      #
#  Boolean index.  Outputs to optical depth output file.       #
################################################################

sst_data = sst_data.flatten()
pbopt_data = np.copy(sst_data)

sst_nan = sst_data[(sst_data == -9999.0)]
sst_nan = np.nan
pbopt_data[(sst_data == -9999.0)] = sst_nan

temp1 = sst_data[(sst_data < 28.5) & (sst_data > -1.0)]
temp1 = (-3.27*(10**-8))*(temp1**7)+(3.4132*(10**-6))*(temp1**6)-(1.348*10**-4)*(temp1**5)+(2.462*(10**-3))*(temp1**4)-(0.0205*(temp1**3))+(0.0617*(temp1**2))+(0.2749*temp1)+1.2956
pbopt_data[(sst_data < 28.5) & (sst_data > -1.0)] = temp1

temp2 = sst_data[(sst_data <= -10.0)]
temp2 = 0.0
pbopt_data[(sst_data <= -10.0)] = temp2

temp3 = sst_data[(sst_data <= -1.0) & (sst_data > -10.0)]
temp3 = 1.13
pbopt_data[(sst_data <= -1.0) & (sst_data > -10.0)] = temp3

temp4 = sst_data[(sst_data >= 28.5)]
temp4 = 4.0
pbopt_data[(sst_data >= 28.5)] = temp4

pbopt_data = pbopt_data.reshape(1080,2160)
sst_data = sst_data.reshape(1080,2160)
print "pbopt complete"

#################################################################
#  Calculates the total chlorophyll value for each pixel using  #
#  Boolean indexing.  Outputs to chlorophyll output file.       #
#################################################################

chl_data = chl_data.flatten()
tot_chl = np.copy(chl_data)

chl_nan = chl_data[(chl_data == -9999.0)]
chl_nan = np.nan
tot_chl[(chl_data == -9999.0)] = chl_nan
chl_data[(chl_data == -9999.0)] = chl_nan

chl2 = chl_data[(chl_data > 1.0)]
chl2 = 40.2 * (chl2**0.507)
tot_chl[(chl_data > 1.0)] = chl2

chl1 = chl_data[(chl_data < 1.0)]
chl1 = 38.0 * (chl1**0.425)
tot_chl[(chl_data < 1.0)] = chl1

chl_data = chl_data.reshape(1080, 2160)

print "total chl complete"
###################################################################
#   Calculates the euphotic depth for each pixel based on the     #
#   total chlorophyll calculated previously, using Boolean        #
#   indexing.  Outputs to euphotic depth output file.             #        
###################################################################

zeu1_data = np.copy(tot_chl)
zeu2_tile = np.copy(zeu1_data)

zeu1 = tot_chl[(tot_chl != chl_nan)]                                        #Calculates euphotic depth based on the first algorithm
zeu1 = 200.0*(zeu1**-0.293)
zeu1_data[(tot_chl != chl_nan)] = zeu1 

zeu2_pixel = zeu1_data[(zeu1_data <= 102.0) & (zeu1_data != chl_nan)]       #Sets any euphotic depth less than 102.0 to 1.0 in a new array (zeu2) 
zeu2_pixel = 1.0
zeu2_tile[(zeu1_data <= 102.0) & (zeu1_data != chl_nan)] = zeu2_pixel

zeu2_blank = zeu1_data[(zeu1_data > 102.0)]                                 #Sets any euphotic depth greater than 102.0 in zeu2 to 0.0 
zeu2_blank = 0.0
zeu2_tile[(zeu1_data > 102.0)] = zeu2_blank

zeu2_data = zeu2_tile * tot_chl                                             #Replaces pixels in zeu2 equal to 1.0 with the original total chlorophyll values

zeu2 = zeu2_data[(zeu2_data != 0.0) & (zeu2_data != chl_nan)]                                    #Calculates euphotic depth for depths less than 102.0 with the second algorithm
zeu2 = 568.2*(zeu2**-0.746)                                     
zeu2_data[(zeu2_data != 0.0) & (zeu2_data != chl_nan)] = zeu2    

zeu_blank = zeu1_data[(zeu1_data <= 102.0) & (zeu1_data != chl_nan)]        #Sets any depths less than 102.0 in zeu1 to 0.0 
zeu_blank = 0.0
zeu1_data[(zeu1_data <= 102.0) & (zeu1_data != chl_nan)] = zeu_blank

zeu_data = zeu1_data + zeu2_data                                            #Combines zeu1 and zeu2 into a single array

zeu_data = zeu_data.reshape(1080,2160)
tot_chl = tot_chl.reshape(1080,2160)

print "optical depth complete"
###################################################################
#  Calculates the irradiance value for each pixel using Boolean   #
#  indexing.  Outputs to PAR output file.                         #
###################################################################

par_data = par_data.flatten()

par_nan = par_data[(par_data == -9999.0)]
par_nan = np.nan
par_data[(par_data == -9999.0)] = par_nan

par = par_data[(par_data != -9999.0)]
par = 0.66125 * par/(par + 4.1)
par_data[(par_data != -9999.0)] = par

par_data = par_data.reshape(1080,2160)

print "par complete"
###################################################################
#   Generates a day length map based on latitude and the inputed  #
#   day of the year.                                              #
###################################################################

lat_array = np.arange(90,-90,(-1.0/6))
lat_array = np.split(lat_array, 1080)

lat_data = np.tile(lat_array, 2160).reshape(1080,2160)
lat_data = lat_data*(np.pi/180)

psi = float(day)/365.0 * 2.0 * np.pi

sol_decl = np.ones(1080)
sol_decl = np.tile(sol_decl,2160)
sol_decl = sol_decl * np.tan((0.39637 - (22.9133 * np.cos(psi)) + (4.02543 * np.sin(psi)) - (0.38720 * np.cos(2*psi)) + (0.05200 * np.sin(2*psi))) * np.pi/180.0)

rad_sol = lat_data
rad_sol = rad_sol.flatten()
rad_sol = -1*np.tan(rad_sol)

rad_sol = np.multiply(rad_sol, sol_decl)

dl_data = np.zeros_like(rad_sol)

day1 = rad_sol[(rad_sol <= -1)]
day1 = 24.0
dl_data[(rad_sol <= -1)] = day1

day2 = rad_sol[(rad_sol < 1) & (rad_sol > -1)] 
day2 = 24.0 * np.arccos(day2)/np.pi
dl_data[(rad_sol < 1) & (rad_sol > -1)] = day2

day3 = rad_sol[(rad_sol >= 1)]
day3 = 0.0
dl_data[(rad_sol >= 1)] = day3

dl_data = dl_data.reshape(1080,2160)
print "day length complete"

####################################################################
#   Calculates NPP for each pixel by multiplying values for that   #
#   pixel from pbopt, zeu, tot_chl, par and dl together.           #
#   Produces output hdf file containing NPP data.                  #
####################################################################  

NPP_data = np.zeros_like(dl_data)

NPP_data = pbopt_data * zeu_data * chl_data * par_data * dl_data 

OUTPUT1 = "C:\Anaconda\envs\sat_data\NPP_3.hdf"
NPP = SD(OUTPUT1, SDC.WRITE | SDC.CREATE)
sds = NPP.create("sds1", SDC.FLOAT64,(1080,2160))
sds.setfillvalue(0)
sds[:] = NPP_data
sds.endaccess()
NPP.end()
