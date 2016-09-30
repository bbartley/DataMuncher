import openpyxl as xlsx
import numpy as np
import matplotlib.pyplot as plt
import data_muncher as dm
from scipy.optimize import fmin

'''
Analysis of the 16_08_30 data
plate layout
10^-6 A : BB52 (1-3)  : SS13 (4-6) : SS17 (7-9)
2^-1 * 10^-6 A : BB52 (1-3)  : SS13 (4-6) : SS17 (7-9)
2^-2 * 10^-6 B : BB52 (1-3)  : SS13 (4-6) : SS17 (7-9)
2^-3 * 10^-6 C : BB52 (1-3)  : SS13 (4-6) : SS17 (7-9)
2^-4 * 10^-6 D : BB52 (1-3)  : SS13 (4-6) : SS17 (7-9)
2^-5 * 10^-6 E : BB52 (1-3)  : SS13 (4-6) : SS17 (7-9)
2^-6 * 10^-6 F : BB52 (1-3)  : SS13 (4-6) : SS17 (7-9)
Blank H : LB Broth


Additionally BB52 was used for preparing the standard curve
'''



#Loading the 16_08_30 plate reader file

f = '16_08_30 Dilution Curve.xlsx'

ex = dm.Experiment(f);
data_series = ex.read('Time [s]')
time_labels = data_series.list_of_series[0]

PlateReadout = dm.Sample();
row_ids = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H']
column_ids = map(str, range(1, 13))
well_ids = [ r + c for r in row_ids for c in column_ids if ex.search(r + c)]
for w in well_ids:
    W = dm.Well();
    W.measurements = ex.read(w)  #Read well data vertically in columns from plate reader spreadsheet
    PlateReadout.addWell(w, W)
data_series = PlateReadout.get_measurements()

#Assigning Samples from plate layout
#BB52 dilution
BB52_10_6 = dm.Sample()
BB52_10_6.addWell('A1', PlateReadout['A1'])
BB52_10_6.addWell('A2', PlateReadout['A2'])
BB52_10_6.addWell('A3', PlateReadout['A3'])

BB52_10_6_2_1 = dm.Sample()
BB52_10_6_2_1.addWell('B1', PlateReadout['B1'])
BB52_10_6_2_1.addWell('B2', PlateReadout['B2'])
BB52_10_6_2_1.addWell('B3', PlateReadout['B3']) 

BB52_10_6_2_2 = dm.Sample()
BB52_10_6_2_2.addWell('C1', PlateReadout['C1'])
BB52_10_6_2_2.addWell('C2', PlateReadout['C2'])
BB52_10_6_2_2.addWell('C3', PlateReadout['C3']) 

BB52_10_6_2_3 = dm.Sample()
BB52_10_6_2_3.addWell('D1', PlateReadout['D1'])
BB52_10_6_2_3.addWell('D2', PlateReadout['D2'])
BB52_10_6_2_3.addWell('D3', PlateReadout['D3']) 

BB52_10_6_2_4 = dm.Sample()
BB52_10_6_2_4.addWell('E1', PlateReadout['E1'])
BB52_10_6_2_4.addWell('E2', PlateReadout['E2'])
BB52_10_6_2_4.addWell('E3', PlateReadout['E3']) 

BB52_10_6_2_5 = dm.Sample()
BB52_10_6_2_5.addWell('F1', PlateReadout['F1'])
BB52_10_6_2_5.addWell('F2', PlateReadout['F2'])
BB52_10_6_2_5.addWell('F3', PlateReadout['F3']) 

BB52_10_6_2_6 = dm.Sample()
BB52_10_6_2_6.addWell('G1', PlateReadout['G1'])
BB52_10_6_2_6.addWell('G2', PlateReadout['G2'])
BB52_10_6_2_6.addWell('G3', PlateReadout['G3']) 

blank = dm.Sample()
blank.addWell('H1', PlateReadout['H1'])
blank.addWell('H2', PlateReadout['H2'])
blank.addWell('H3', PlateReadout['H3'])
blank.addWell('H4', PlateReadout['H4'])
blank.addWell('H5', PlateReadout['H5'])
blank.addWell('H6', PlateReadout['H6'])
blank.addWell('H7', PlateReadout['H7'])
blank.addWell('H8', PlateReadout['H8'])
#blank.addWell('H9', PlateReadout['H9'])
# must determine why the palte reader cannot read the final column that is inputted

#SS13 Dilution
#GFP expression present for only SS13
SS13_10_6 = dm.Sample()
SS13_10_6.addWell('A4', PlateReadout['A4'])
SS13_10_6.addWell('A5', PlateReadout['A5'])
SS13_10_6.addWell('A6', PlateReadout['A6'])

SS13_10_6_2_1 = dm.Sample()
SS13_10_6_2_1.addWell('B4', PlateReadout['B4'])
SS13_10_6_2_1.addWell('B5', PlateReadout['B5'])
SS13_10_6_2_1.addWell('B6', PlateReadout['B6']) 

SS13_10_6_2_2 = dm.Sample()
SS13_10_6_2_2.addWell('C4', PlateReadout['C4'])
SS13_10_6_2_2.addWell('C5', PlateReadout['C5'])
SS13_10_6_2_2.addWell('C6', PlateReadout['C6']) 

SS13_10_6_2_3 = dm.Sample()
SS13_10_6_2_3.addWell('D4', PlateReadout['D4'])
SS13_10_6_2_3.addWell('D5', PlateReadout['D5'])
SS13_10_6_2_3.addWell('D6', PlateReadout['D6']) 

SS13_10_6_2_4 = dm.Sample()
SS13_10_6_2_4.addWell('E4', PlateReadout['E4'])
SS13_10_6_2_4.addWell('E5', PlateReadout['E5'])
SS13_10_6_2_4.addWell('E6', PlateReadout['E6']) 

SS13_10_6_2_5 = dm.Sample()
SS13_10_6_2_5.addWell('F4', PlateReadout['F4'])
SS13_10_6_2_5.addWell('F5', PlateReadout['F5'])
SS13_10_6_2_5.addWell('F6', PlateReadout['F6'])

SS13_10_6_2_6 = dm.Sample()
SS13_10_6_2_6.addWell('G4', PlateReadout['G4'])
SS13_10_6_2_6.addWell('G5', PlateReadout['G5'])
SS13_10_6_2_6.addWell('G6', PlateReadout['G6']) 

#SS17 Dilution
SS17_10_6 = dm.Sample()
SS17_10_6.addWell('A7', PlateReadout['A7'])
SS17_10_6.addWell('A8', PlateReadout['A8'])
SS17_10_6.addWell('A9', PlateReadout['A9'])

SS17_10_6_2_1 = dm.Sample()
SS17_10_6_2_1.addWell('B7', PlateReadout['B7'])
SS17_10_6_2_1.addWell('B8', PlateReadout['B8'])
SS17_10_6_2_1.addWell('B9', PlateReadout['B9']) 

SS17_10_6_2_2 = dm.Sample()
SS17_10_6_2_2.addWell('C7', PlateReadout['C7'])
SS17_10_6_2_2.addWell('C8', PlateReadout['C8'])
SS17_10_6_2_2.addWell('C9', PlateReadout['C9']) 

SS17_10_6_2_3 = dm.Sample()
SS17_10_6_2_3.addWell('D7', PlateReadout['D7'])
SS17_10_6_2_3.addWell('D8', PlateReadout['D8'])
SS17_10_6_2_3.addWell('D9', PlateReadout['D9']) 

SS17_10_6_2_4 = dm.Sample()
SS17_10_6_2_4.addWell('E7', PlateReadout['E7'])
SS17_10_6_2_4.addWell('E8', PlateReadout['E8'])
SS17_10_6_2_4.addWell('E9', PlateReadout['E9']) 

SS17_10_6_2_5 = dm.Sample()
SS17_10_6_2_5.addWell('F7', PlateReadout['F7'])
SS17_10_6_2_5.addWell('F8', PlateReadout['F8'])
SS17_10_6_2_5.addWell('F9', PlateReadout['F9'])

SS17_10_6_2_6 = dm.Sample()
SS17_10_6_2_6.addWell('G7', PlateReadout['G7'])
SS17_10_6_2_6.addWell('G8', PlateReadout['G8'])
SS17_10_6_2_6.addWell('G9', PlateReadout['G9']) 


# Plot the 10^-6 dilution
plt.plot(time_labels, BB52_10_6.mean())
plt.plot(time_labels, SS13_10_6.mean())
plt.plot(time_labels, SS17_10_6.mean())
plt.plot(time_labels, blank.mean())
plt.ylabel('optical density (OD)')
plt.xlabel('Time (sec)')
plt.legend(['BB52', 'SS13', 'SS17', 'Blank'])
plt.title('Optical Density for 10^-6 Diltuion Factor')
plt.show()

#Plot the 10^-6*2^-1 Optical Density Dilution
plt.plot(time_labels, BB52_10_6_2_1.mean())
plt.plot(time_labels, SS13_10_6_2_1.mean())
plt.plot(time_labels, SS17_10_6_2_1.mean())
plt.plot(time_labels, blank.mean())
plt.ylabel('optical density (OD)')
plt.xlabel('Time (sec)')
plt.legend(['BB52', 'SS13', 'SS17', 'Blank'])
plt.title('Optical Density for 10^-6*2^-1 Diltuion Factor')
plt.show()

#Plot the 10^-6*2^-2 Optical Density Dilution
plt.plot(time_labels, BB52_10_6_2_2.mean())
plt.plot(time_labels, SS13_10_6_2_2.mean())
plt.plot(time_labels, SS17_10_6_2_2.mean())
plt.plot(time_labels, blank.mean())
plt.ylabel('optical density (OD)')
plt.xlabel('Time (sec)')
plt.legend(['BB52', 'SS13', 'SS17', 'Blank'])
plt.title('Optical Density for 10^-6*2^-2 Diltuion Factor')
plt.show()

#Plot the 10^-6*2^-3 Optical Density Dilution
plt.plot(time_labels, BB52_10_6_2_3.mean())
plt.plot(time_labels, SS13_10_6_2_3.mean())
plt.plot(time_labels, SS17_10_6_2_3.mean())
plt.plot(time_labels, blank.mean())
plt.ylabel('optical density (OD)')
plt.xlabel('Time (sec)')
plt.legend(['BB52', 'SS13', 'SS17', 'Blank'])
plt.title('Optical Density for 10^-6*2^-3 Diltuion Factor')
plt.show()

#Plot the 10^-6*2^-4 Optical Density Dilution
plt.plot(time_labels, BB52_10_6_2_4.mean())
plt.plot(time_labels, SS13_10_6_2_4.mean())
plt.plot(time_labels, SS17_10_6_2_4.mean())
plt.plot(time_labels, blank.mean())
plt.ylabel('optical density (OD)')
plt.xlabel('Time (sec)')
plt.legend(['BB52', 'SS13', 'SS17', 'Blank'])
plt.title('Optical Density for 10^-6*2^-4 Diltuion Factor')
plt.show()
#Plot the 10^-6*2^-5 Optical Density Dilution
plt.plot(time_labels, BB52_10_6_2_5.mean())
plt.plot(time_labels, SS13_10_6_2_5.mean())
plt.plot(time_labels, SS17_10_6_2_5.mean())
plt.plot(time_labels, blank.mean())
plt.ylabel('optical density (OD)')
plt.xlabel('Time (sec)')
plt.legend(['BB52', 'SS13', 'SS17', 'Blank'])
plt.title('Optical Density for 10^-6*2^-5 Diltuion Factor')
plt.show()

#Plot the 10^-6*2^-6 Optical Density Dilution
plt.plot(time_labels, BB52_10_6_2_6.mean())
plt.plot(time_labels, SS13_10_6_2_6.mean())
plt.plot(time_labels, SS17_10_6_2_6.mean())
plt.plot(time_labels, blank.mean())
plt.ylabel('optical density (OD)')
plt.xlabel('Time (sec)')
plt.legend(['BB52', 'SS13', 'SS17', 'Blank'])
plt.title('Optical Density for 10^-6*2^-6 Diltuion Factor')
plt.show()


#Subtract the Mean of the blank from the Mean of each Data Series
blankAvg = np.asarray(blank.mean())
blankStd = np.asarray(blank.std());

# LOQ is the standard deviation of the blank multiplied by 3
LOQ = 3 * blankStd
LOQ = np.mean(LOQ)

#The 10^-6 Dilution Data with the Blank subtracted and 3 times the LOQ masked
avgBB52_10_6 = np.asarray(BB52_10_6.mean())
avgBB52_10_6 = avgBB52_10_6 - blankAvg
for value in avgBB52_10_6:
    if value < LOQ:
       avgBB52_10_6 = np.delete(avgBB52_10_6, value)

avgSS13_10_6 = np.asarray(SS13_10_6.mean())
avgSS13_10_6 = avgSS13_10_6 - blankAvg
for value in avgSS13_10_6:
    if value < LOQ:
       avgSS13_10_6 = np.delete(avgSS13_10_6, value)

avgSS17_10_6 = np.asarray(SS17_10_6.mean())
avgSS17_10_6 = avgSS17_10_6 - blankAvg
for value in avgSS17_10_6:
    if value < LOQ:
       avgSS17_10_6 = np.delete(avgSS17_10_6, value)

#The 10^-6* 2^-1 Dilution Data with the Blank subtracted and 3 times the LOQ masked
avgBB52_10_6_2_1 = np.asarray(BB52_10_6_2_1.mean())
avgBB52_10_6_2_1 = avgBB52_10_6_2_1 - blankAvg
for value in avgBB52_10_6_2_1:
    if value < LOQ:
       avgBB52_10_6_2_1 = np.delete(avgBB52_10_6_2_1, value)

avgSS13_10_6_2_1 = np.asarray(SS13_10_6_2_1.mean())
avgSS13_10_6_2_1 = avgSS13_10_6_2_1 - blankAvg
for value in avgSS13_10_6_2_1:
    if value < LOQ:
       avgSS13_10_6_2_1 = np.delete(avgSS13_10_6_2_1, value)

avgSS17_10_6_2_1 = np.asarray(SS17_10_6_2_1.mean())
avgSS17_10_6_2_1 = avgSS17_10_6_2_1 - blankAvg
for value in avgSS17_10_6_2_1:
    if value < LOQ:
        avgSS17_10_6_2_1 = np.delete(avgSS17_10_6_2_1, value)

#The 10^-6*2^-2 Dilution DAta with the Blank subtracted and 3 tmes the LOQ masked
avgBB52_10_6_2_2 = np.asarray(BB52_10_6_2_2.mean())
avgBB52_10_6_2_2 = avgBB52_10_6_2_2 - blankAvg
for value in avgBB52_10_6_2_2:
    if value < LOQ:
        avgBB52_10_6_2_2 = np.delete(avgBB52_10_6_2_2, value)

avgSS13_10_6_2_2 = np.asarray(SS13_10_6_2_2.mean())
avgSS13_10_6_2_2 = avgSS13_10_6_2_2 - blankAvg
for value in avgSS13_10_6_2_2:
    if value < LOQ:
        avgSS13_10_6_2_2 = np.delete(avgSS13_10_6_2_2, value)

avgSS17_10_6_2_2 = np.asarray(SS17_10_6_2_2.mean())
avgSS17_10_6_2_2 = avgSS17_10_6_2_2 - blankAvg
for value in avgSS17_10_6_2_2:
    if value < LOQ:
        avgSS17_10_6_2_2 = np.delete(avgSS17_10_6_2_2, value)

#The 10^-6*2^-3 Dilution DAta with the Blank subtracted and 3 tmes the LOQ masked
avgBB52_10_6_2_3 = np.asarray(BB52_10_6_2_3.mean())
avgBB52_10_6_2_3 = avgBB52_10_6_2_3 - blankAvg
for value in avgBB52_10_6_2_3:
    if value < LOQ:
        avgBB52_10_6_2_3 = np.delete(avgBB52_10_6_2_3, value)

avgSS13_10_6_2_3 = np.asarray(SS13_10_6_2_3.mean())
avgSS13_10_6_2_3 = avgSS13_10_6_2_3 - blankAvg
for value in avgSS13_10_6_2_3:
    if value < LOQ:
        avgSS13_10_6_2_3 = np.delete(avgSS13_10_6_2_3, value)

avgSS17_10_6_2_3 = np.asarray(SS17_10_6_2_3.mean())
avgSS17_10_6_2_3 = avgSS17_10_6_2_3 - blankAvg
for value in avgSS17_10_6_2_3:
    if value < LOQ:
        avgSS17_10_6_2_3 = np.delete(avgSS17_10_6_2_3, value)

#The 10^-6*2^-4 Dilution DAta with the Blank subtracted and 3 tmes the LOQ masked
avgBB52_10_6_2_4 = np.asarray(BB52_10_6_2_4.mean())
avgBB52_10_6_2_4 = avgBB52_10_6_2_4 - blankAvg
for value in avgBB52_10_6_2_4:
    if value < LOQ:
        avgBB52_10_6_2_4  = np.delete(avgBB52_10_6_2_4, value)

avgSS13_10_6_2_4 = np.asarray(SS13_10_6_2_4.mean())
avgSS13_10_6_2_4 = avgSS13_10_6_2_4 - blankAvg
for value in avgSS13_10_6_2_4:
    if value < LOQ:
        avgSS13_10_6_2_4  = np.delete(avgSS13_10_6_2_4  , value)

avgSS17_10_6_2_4 = np.asarray(SS17_10_6_2_4.mean())
avgSS17_10_6_2_4 = avgSS17_10_6_2_4 - blankAvg
for value in avgSS17_10_6_2_4:
    if value < LOQ:
        avgSS17_10_6_2_4 = np.delete(avgSS17_10_6_2_4 , value)

#The 10^-6*2^-5 Dilution DAta with the Blank subtracted and 3 tmes the LOQ masked
avgBB52_10_6_2_5 = np.asarray(BB52_10_6_2_5.mean())
avgBB52_10_6_2_5 = avgBB52_10_6_2_5 - blankAvg
for value in avgBB52_10_6_2_5:
    if value < LOQ:
        avgBB52_10_6_2_5 = np.delete(avgBB52_10_6_2_5 , value)

avgSS13_10_6_2_5 = np.asarray(SS13_10_6_2_5.mean())
avgSS13_10_6_2_5 = avgSS13_10_6_2_5 - blankAvg
for value in avgSS13_10_6_2_5 :
    if value < LOQ:
        avgSS13_10_6_2_5  = np.delete(avgSS13_10_6_2_5 , value)


avgSS17_10_6_2_5 = np.asarray(SS17_10_6_2_5.mean())
avgSS17_10_6_2_5 = avgSS17_10_6_2_5 - blankAvg
for value in avgSS17_10_6_2_5:
    if value < LOQ:
        avgSS17_10_6_2_5 = np.delete(avgSS17_10_6_2_5, value)

#The 10^-6*2^-6 Dilution DAta with the Blank subtracted and 3 tmes the LOQ masked
avgBB52_10_6_2_6 = np.asarray(BB52_10_6_2_6.mean())
avgBB52_10_6_2_6 = avgBB52_10_6_2_6 - blankAvg
for value in avgBB52_10_6_2_6:
    if value < LOQ:
        avgBB52_10_6_2_6 = np.delete(avgBB52_10_6_2_6, value)

avgSS13_10_6_2_6 = np.asarray(SS13_10_6_2_6.mean())
avgSS13_10_6_2_6 = avgSS13_10_6_2_6 - blankAvg
for value in avgSS13_10_6_2_6:
    if value < LOQ:
        avgSS13_10_6_2_6 = np.delete(avgSS13_10_6_2_6, value)

avgSS17_10_6_2_6 = np.asarray(SS17_10_6_2_6.mean())
avgSS17_10_6_2_6 = avgSS17_10_6_2_6 - blankAvg
mask = (avgSS17_10_6_2_6 > LOQ)
for value in avgSS17_10_6_2_6:
    if value < LOQ:
        avgSS17_10_6_2_6 = np.delete(avgSS17_10_6_2_6, value)

#Translating from ODE to ADF for all of the data
# ADF(Arbitrary Dilution Factor) --> ACF(Arbitrary Cell/Concentration Factor)
# y(ACF) = a(ODE)^2 + b(ODE) + c
a = 0.31 
b = -0.1336
c = 0.2625
  
# 10^-6 dilituion data
BB52_10_6_ACF = list()
for value in avgBB52_10_6 :
    ACF = a * value * value + b * value + c
    BB52_10_6_ACF.append(ACF)
     
SS13_10_6_ACF = list()
for value in avgSS13_10_6 :
     ACF = a * value * value + b * value + c
     SS13_10_6_ACF.append(ACF)
     
SS17_10_6_ACF = list()
for value in avgSS17_10_6:
    ACF = a * value * value + b * value + c
    SS17_10_6_ACF.append(ACF)
    
# 10^-6 * 2^-1 dilution data
BB52_10_6_2_1_ACF = list()
for value in avgBB52_10_6_2_1:
    ACF = a * value * value + b * value + c
    BB52_10_6_2_1_ACF.append(ACF)
  
SS13_10_6_2_1_ACF = list()
for value in avgSS13_10_6_2_1:
    ACF = a * value * value + b * value + c
    SS13_10_6_2_1_ACF.append(ACF)
    
SS17_10_6_2_1_ACF = list()
for value in avgSS17_10_6_2_1:
    ACF = a * value * value + b * value + c
    SS17_10_6_2_1_ACF.append(ACF)

# 10^-6 * 2^-2 dilution data
BB52_10_6_2_2_ACF = list()
for value in avgBB52_10_6_2_2:
    ACF = a * value * value + b * value + c
    BB52_10_6_2_2_ACF.append(ACF)
  
SS13_10_6_2_2_ACF = list()
for value in avgSS13_10_6_2_2:
    ACF = a * value * value + b * value + c
    SS13_10_6_2_2_ACF.append(ACF)
    
SS17_10_6_2_2_ACF = list()
for value in avgSS17_10_6_2_2:
    ACF = a * value * value + b * value + c
    SS17_10_6_2_2_ACF.append(ACF)
    
#10^-6 * 2^-3 diltuion data ACF conversion
BB52_10_6_2_3_ACF = list()
for value in avgBB52_10_6_2_3:
    ACF = a * value * value + b * value + c
    BB52_10_6_2_3_ACF.append(ACF)
  
SS13_10_6_2_3_ACF = list()
for value in avgSS13_10_6_2_3:
    ACF = a * value * value + b * value + c
    SS13_10_6_2_3_ACF.append(ACF)
    
SS17_10_6_2_3_ACF = list()
for value in avgSS17_10_6_2_3:
    ACF = a * value * value + b * value + c
    SS17_10_6_2_3_ACF.append(ACF)
    
#10^-6 * 2^-4 diltuion data ACF conversion
BB52_10_6_2_4_ACF = list()
for value in avgBB52_10_6_2_4:
    ACF = a * value * value + b * value + c
    BB52_10_6_2_4_ACF.append(ACF)
  
SS13_10_6_2_4_ACF = list()
for value in avgSS13_10_6_2_4:
    ACF = a * value * value + b * value + c
    SS13_10_6_2_4_ACF.append(ACF)
    
SS17_10_6_2_4_ACF = list()
for value in avgSS17_10_6_2_4:
    ACF = a * value * value + b * value + c
    SS17_10_6_2_4_ACF.append(ACF)
   
#10^-6 * 2^-5 diltuion data ACF conversion
BB52_10_6_2_5_ACF = list()
for value in avgBB52_10_6_2_5:
    ACF = a * value * value + b * value + c
    BB52_10_6_2_5_ACF.append(ACF)
  
SS13_10_6_2_5_ACF = list()
for value in avgSS13_10_6_2_5:
    ACF = a * value * value + b * value + c
    SS13_10_6_2_5_ACF.append(ACF)
    
SS17_10_6_2_5_ACF = list()
for value in avgSS17_10_6_2_5:
    ACF = a * value * value + b * value + c
    SS17_10_6_2_5_ACF.append(ACF)
    
#10^-6 * 2^-6 diltuion data ACF conversion
BB52_10_6_2_6_ACF = list()
for value in avgBB52_10_6_2_6:
    ACF = a * value * value + b * value + c
    BB52_10_6_2_6_ACF.append(ACF)
  
SS13_10_6_2_6_ACF = list()
for value in avgSS13_10_6_2_6:
    ACF = a * value * value + b * value + c
    SS13_10_6_2_6_ACF.append(ACF)
    
SS17_10_6_2_6_ACF = list()
for value in avgSS17_10_6_2_6:
    ACF = a * value * value + b * value + c
    SS17_10_6_2_6_ACF.append(ACF)   
 
#Estimating the initial point of the graph by doing a 1:1000 dilution for
#smallest value that was calculated for the ACF for each data set
#Once the guess is made it is then added the beginning of each array
    
# 10^-6 initial guess data
Initial_BB52_10_6_ACF = BB52_10_6_ACF[0] / 1000
BB52_10_6_ACF = np.asarray(BB52_10_6_ACF)
BB52_10_6_ACF = np.insert(BB52_10_6_ACF, 0, Initial_BB52_10_6_ACF)

Initial_SS13_10_6_ACF = SS13_10_6_ACF[0] / 1000
SS13_10_6_ACF = np.asarray(SS13_10_6_ACF)
SS13_10_6_ACF = np.insert(SS13_10_6_ACF, 0, Initial_SS13_10_6_ACF)

Initial_SS17_10_6_ACF = SS17_10_6_ACF[0] / 1000
SS17_10_6_ACF = np.asarray(SS17_10_6_ACF)
SS17_10_6_ACF = np.insert(SS17_10_6_ACF, 0, Initial_SS17_10_6_ACF)

# 10^-6* 2^-1 Initial guesss data
Initial_BB52_10_6_2_1_ACF = BB52_10_6_2_1_ACF[0] / 1000
BB52_10_6_2_1_ACF = np.asarray(BB52_10_6_2_1_ACF)
BB52_10_6_2_1_ACF = np.insert(BB52_10_6_2_1_ACF, 0, Initial_BB52_10_6_2_1_ACF)

Initial_SS13_10_6_2_1_ACF = SS13_10_6_2_1_ACF[0] / 1000
SS13_10_6_2_1_ACF = np.asarray(SS13_10_6_2_1_ACF)
SS13_10_6_2_1_ACF = np.insert(SS13_10_6_2_1_ACF, 0, Initial_SS13_10_6_2_1_ACF)

Initial_SS17_10_6_2_1_ACF = SS17_10_6_2_1_ACF[0] / 1000
SS17_10_6_2_1_ACF = np.asarray(SS17_10_6_2_1_ACF)
SS17_10_6_2_1_ACF = np.insert(SS17_10_6_2_1_ACF, 0, Initial_SS17_10_6_2_1_ACF)

# 10^-6* 2^-2 Initial guesss data
Initial_BB52_10_6_2_2_ACF = BB52_10_6_2_2_ACF[0] / 1000
BB52_10_6_2_2_ACF = np.asarray(BB52_10_6_2_2_ACF)
BB52_10_6_2_2_ACF = np.insert(BB52_10_6_2_2_ACF, 0, Initial_BB52_10_6_2_2_ACF)

Initial_SS13_10_6_2_2_ACF = SS13_10_6_2_2_ACF[0] / 1000
SS13_10_6_2_2_ACF = np.asarray(SS13_10_6_2_2_ACF)
SS13_10_6_2_2_ACF = np.insert(SS13_10_6_2_2_ACF, 0, Initial_SS13_10_6_2_2_ACF)

Initial_SS17_10_6_2_2_ACF = SS17_10_6_2_2_ACF[0] / 1000
SS17_10_6_2_2_ACF = np.asarray(SS17_10_6_2_2_ACF)
SS17_10_6_2_2_ACF = np.insert(SS17_10_6_2_2_ACF, 0, Initial_SS17_10_6_2_2_ACF)

# 10^-6* 2^-3 Initial guesss data
Initial_BB52_10_6_2_3_ACF = BB52_10_6_2_3_ACF[0] / 1000
BB52_10_6_2_3_ACF = np.asarray(BB52_10_6_2_3_ACF)
BB52_10_6_2_3_ACF = np.insert(BB52_10_6_2_3_ACF, 0, Initial_BB52_10_6_2_3_ACF)

Initial_SS13_10_6_2_3_ACF = SS13_10_6_2_3_ACF[0] / 1000
SS13_10_6_2_3_ACF = np.asarray(SS13_10_6_2_3_ACF)
SS13_10_6_2_3_ACF = np.insert(SS13_10_6_2_3_ACF, 0, Initial_SS13_10_6_2_3_ACF)

Initial_SS17_10_6_2_3_ACF = SS17_10_6_2_3_ACF[0] / 1000
SS17_10_6_2_3_ACF = np.asarray(SS17_10_6_2_3_ACF)
SS17_10_6_2_3_ACF = np.insert(SS17_10_6_2_3_ACF, 0, Initial_SS17_10_6_2_3_ACF)

# 10^-6* 2^-4 Initial guesss data
Initial_BB52_10_6_2_4_ACF = BB52_10_6_2_4_ACF[0] / 1000
BB52_10_6_2_4_ACF = np.asarray(BB52_10_6_2_4_ACF)
BB52_10_6_2_4_ACF = np.insert(BB52_10_6_2_4_ACF, 0, Initial_BB52_10_6_2_4_ACF)

Initial_SS13_10_6_2_4_ACF = SS13_10_6_2_4_ACF[0] / 1000
SS13_10_6_2_4_ACF = np.asarray(SS13_10_6_2_4_ACF)
SS13_10_6_2_4_ACF = np.insert(SS13_10_6_2_4_ACF, 0, Initial_SS13_10_6_2_4_ACF)

Initial_SS17_10_6_2_4_ACF = SS17_10_6_2_4_ACF[0] / 1000
SS17_10_6_2_4_ACF = np.asarray(SS17_10_6_2_4_ACF)
SS17_10_6_2_4_ACF = np.insert(SS17_10_6_2_4_ACF, 0, Initial_SS17_10_6_2_4_ACF)

# 10^-6* 2^-5 Initial guesss data
Initial_BB52_10_6_2_5_ACF = BB52_10_6_2_5_ACF[0] / 1000
BB52_10_6_2_5_ACF = np.asarray(BB52_10_6_2_5_ACF)
BB52_10_6_2_5_ACF = np.insert(BB52_10_6_2_5_ACF, 0, Initial_BB52_10_6_2_5_ACF)

Initial_SS13_10_6_2_5_ACF = SS13_10_6_2_5_ACF[0] / 1000
SS13_10_6_2_5_ACF = np.asarray(SS13_10_6_2_5_ACF)
SS13_10_6_2_5_ACF = np.insert(SS13_10_6_2_5_ACF, 0, Initial_SS13_10_6_2_5_ACF)

Initial_SS17_10_6_2_5_ACF = SS17_10_6_2_5_ACF[0] / 1000
SS17_10_6_2_5_ACF = np.asarray(SS17_10_6_2_5_ACF)
SS17_10_6_2_5_ACF = np.insert(SS17_10_6_2_5_ACF, 0, Initial_SS17_10_6_2_5_ACF)

# 10^-6* 2^-6 Initial guesss data
Initial_BB52_10_6_2_6_ACF = BB52_10_6_2_6_ACF[0] / 1000
BB52_10_6_2_6_ACF = np.asarray(BB52_10_6_2_6_ACF)
BB52_10_6_2_6_ACF = np.insert(BB52_10_6_2_6_ACF, 0, Initial_BB52_10_6_2_6_ACF)

'''
Initial_SS13_10_6_2_6_ACF = SS13_10_6_2_6_ACF[0] / 1000
SS13_10_6_2_6_ACF = np.asarray(SS13_10_6_2_6_ACF)
SS13_10_6_2_6_ACF = np.insert(SS13_10_6_2_6_ACF, 0, Initial_SS13_10_6_2_6_ACF)
''' 

Initial_SS17_10_6_2_6_ACF = SS17_10_6_2_6_ACF[0] / 1000
SS17_10_6_2_6_ACF = np.asarray(SS17_10_6_2_6_ACF)
SS17_10_6_2_6_ACF = np.insert(SS17_10_6_2_6_ACF, 0, Initial_SS17_10_6_2_6_ACF)

# Normalizaing with respect to the LOQ

#Normalizing the 10^-6 ACF Data
BB52_10_6_ACF = BB52_10_6_ACF/ LOQ
SS13_10_6_ACF = SS13_10_6_ACF / LOQ
SS17_10_6_ACF = SS17_10_6_ACF / LOQ

# Normalizing the 10^-6 * 2^-1 ACF Data
BB52_10_6_2_1_ACF = BB52_10_6_2_1_ACF/ LOQ
SS13_10_6_2_1_ACF = SS13_10_6_2_1_ACF / LOQ
SS17_10_6_2_1_ACF = SS17_10_6_2_1_ACF / LOQ

# Normalizing the 10^-6 * 2^-2 ACF Data
BB52_10_6_2_2_ACF = BB52_10_6_2_2_ACF/ LOQ
SS13_10_6_2_2_ACF = SS13_10_6_2_2_ACF / LOQ
SS17_10_6_2_2_ACF = SS17_10_6_2_2_ACF / LOQ

# Normalizing the 10^-6 * 2^-3 ACF Data
BB52_10_6_2_3_ACF = BB52_10_6_2_3_ACF/ LOQ
SS13_10_6_2_3_ACF = SS13_10_6_2_3_ACF / LOQ
SS17_10_6_2_3_ACF = SS17_10_6_2_3_ACF / LOQ

# Normalizing the 10^-6 * 2^-4 ACF Data
BB52_10_6_2_4_ACF = BB52_10_6_2_4_ACF/ LOQ
SS13_10_6_2_4_ACF = SS13_10_6_2_4_ACF / LOQ
SS17_10_6_2_4_ACF = SS17_10_6_2_4_ACF / LOQ

# Normalizing the 10^-6 * 2^-5 ACF Data
BB52_10_6_2_5_ACF = BB52_10_6_2_5_ACF/ LOQ
SS13_10_6_2_5_ACF = SS13_10_6_2_5_ACF / LOQ
SS17_10_6_2_5_ACF = SS17_10_6_2_5_ACF / LOQ

# Normalizing the 10^-6 * 2^-6 ACF Data
BB52_10_6_2_6_ACF = BB52_10_6_2_6_ACF/ LOQ
SS13_10_6_2_6_ACF = SS13_10_6_2_6_ACF / LOQ
SS17_10_6_2_6_ACF = SS17_10_6_2_6_ACF / LOQ


# a = max Value
# u = growth rate
# y = beginning linear range
def Gompertz(initial_guesses, t):
    results = [] # collects the returned values
    e = np.exp(1)
    for x in t:
        results.append( a * np.exp(-np.exp((initial_guesses[0]*e)/a*(initial_guesses[1] -x) + 1)))
    return results
  
     
# Solving the Objective function for a given set of gueses for 1/20 dilutution data set
# used for the optimization
def Object(initial_guesses, data):
    t = np.linspace(0, 57600, len(data))
    output = Gompertz(initial_guesses, t)
    output = np.asarray(output)
    result = np.sum(np.power((data - output), 2))
    return result
    
    
#Calling the objective function and Gompertz for 10^-6 dilution
a =1
u = np.log(2)/20./60
y =2500
guesses = (u, y)
initial_guesses = np.asarray(guesses)

estimates = fmin(Object, initial_guesses, args = (BB52_10_6_ACF,))
print estimates

time =  np.linspace(0, 57600, len(BB52_10_6_ACF))
values = Gompertz(estimates, time)

plt.plot(time, values)
plt.plot(time, BB52_10_6_ACF)
plt.show()









