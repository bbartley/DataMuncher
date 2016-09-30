import openpyxl as xlsx
import numpy as np
import matplotlib.pyplot as plt
import data_muncher as dm
from scipy.optimize import fmin


#Loading the 16_07_09 plate reader file
fnew = '16_07_09 ss13 growth curve data new.xlsx'
ex = dm.Experiment(fnew);
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
#SS07 1/10 dilution
SS07_10 = dm.Sample()
SS07_10.addWell('A10', PlateReadout['A10'])
SS07_10.addWell('A11', PlateReadout['A11'])
SS07_10.addWell('A12', PlateReadout['A12'])

#SS07 1/20 dilution
SS07_20 = dm.Sample()
SS07_20.addWell('B10', PlateReadout['B10'])
SS07_20.addWell('B11', PlateReadout['B11'])
SS07_20.addWell('B12', PlateReadout['B12'])

#SS13 preinduced 1/10 dilution
SS13pre_10 = dm.Sample()
SS13pre_10.addWell('C10', PlateReadout['C10'])
SS13pre_10.addWell('C11', PlateReadout['C11'])
SS13pre_10.addWell('C12', PlateReadout['C12'])

#SS13 preinduced 1/20 dilution
SS13pre_20 = dm.Sample()
SS13pre_20.addWell('D10', PlateReadout['D10'])
SS13pre_20.addWell('D11', PlateReadout['D11'])
SS13pre_20.addWell('D12', PlateReadout['D12'])

#SS13 postinduced 1/10 dilution
SS13post_10 = dm.Sample()
SS13post_10.addWell('E10', PlateReadout['E10'])
SS13post_10.addWell('E11', PlateReadout['E11'])
SS13post_10.addWell('E12', PlateReadout['E12'])

#SS13 postinduced 1/20 dilution
SS13post_20 = dm.Sample()
SS13post_20.addWell('F10', PlateReadout['F10'])
SS13post_20.addWell('F11', PlateReadout['F11'])
SS13post_20.addWell('F12', PlateReadout['F12'])

#SS13 uninduced 1/10 dilution
SS13un_10 = dm.Sample()
SS13un_10.addWell('G10', PlateReadout['G10'])
SS13un_10.addWell('G11', PlateReadout['G11'])
SS13un_10.addWell('G12', PlateReadout['G12'])

#SS13 uninduced 1/20 dilution
SS13un_20 = dm.Sample()
SS13un_20.addWell('H10', PlateReadout['H10'])
SS13un_20.addWell('H11', PlateReadout['H11'])
#SS13un_20.addWell('H12', PlateReadout['H12'])
#It cannot find H12 

# Luria Broth
LB = dm.Sample()
LB.addWell('H9', PlateReadout['H9'])
LB.addWell('H8', PlateReadout['H8'])
LB.addWell('H7', PlateReadout['H7'])

#List all of the wells in the data file
print(PlateReadout)

#Graph the growth curve for 1:10 dilution
plt.plot(time_labels,SS07_10.mean())
plt.plot(time_labels,SS13pre_10.mean())
plt.plot(time_labels,SS13post_10.mean())
plt.plot(time_labels,SS13un_10.mean())
plt.plot(time_labels, LB.mean())
plt.ylabel('optical density (OD)')
plt.xlabel('Time (sec)')
#plt.legend(['SS07', 'SS13++', 'SS13-+', 'SS13--', 'Blank'])
plt.title('Optical Density for 1/10 Diltuion Factor')
plt.show()

#Graph the growth curve for 1:20 dilution
plt.plot(time_labels,SS07_20.mean())
plt.plot(time_labels,SS13pre_20.mean())
plt.plot(time_labels,SS13post_20.mean())
plt.plot(time_labels,SS13un_20.mean())
plt.plot(time_labels, LB.mean())
plt.ylabel('optical density (OD)')
plt.xlabel('Time (sec)')
#plt.legend(['SS07', 'SS13++', 'SS13-+', 'SS13--', 'Blank'])
plt.title('Optical Density for 1/20 Diltuion Factor')
plt.show()


#Subtract the Mean of the Blank from the Mean of each Data Series
LB_a = np.asarray(LB.mean())
LBstd = np.asarray(LB.std());

# LOQ is the standard deviation of the blank multiplied by 3


LOQ = 3 * LBstd

#The 1:10 Dilution Data with the Blank subtracted and 3 times the LOQ masked
SS07_10_a = np.asarray(SS07_10.mean())
SS07_10_a = SS07_10_a - LB_a
mask = (SS07_10_a > LOQ)
SS07_10_a[mask]

SS13pre_10_a = np.asarray(SS13pre_10.mean())
SS13pre_10_a = SS13pre_10_a - LB_a
mask = SS13pre_10_a > LOQ
SS13pre_10_a[mask]

SS13post_10_a = np.asarray(SS13post_10.mean())
SS13post_10_a = SS13post_10_a - LB_a
mask = SS13post_10_a > LOQ
SS13post_10_a[mask]

SS13un_10_a = np.asarray(SS13un_10.mean())
SS13un_10_a = SS13un_10_a - LB_a
mask = SS13un_10_a > LOQ
SS13un_10_a[mask]


#The 1:20 Dilution Data with the Blank subtracted at 3 times the LOQ masked
SS07_20_a = np.asarray(SS07_20.mean())
SS07_20_a = SS07_20_a - LB_a
mask = SS07_20_a > LOQ
SS07_20_a[mask]

SS13pre_20_a = np.asarray(SS13pre_20.mean())
SS13pre_20_a = SS13pre_20_a - LB_a
mask = SS13pre_20_a > LOQ
SS13pre_20_a[mask]

SS13post_20_a = np.asarray(SS13post_20.mean())
SS13post_20_a = SS13post_20_a - LB_a
mask = SS13post_20_a > LOQ
SS13pre_20_a[mask]

SS13un_20_a = np.asarray(SS13un_20.mean())
SS13un_20_a = SS13un_20_a - LB_a
mask = SS13un_20_a > LOQ
SS13un_20_a[mask]



#Translating from ODE to ADF for all of the data
# ADF(Arbitrary Dilution Factor) --> ACF(Arbitrary Cell/Concentration Factor)
# y(ACF) = a(ODE)^2 + b(ODE) + c
a = 0.3433 
b = 1.2228
c = -0.0603

SS07_10_ACF = list()
for value in SS07_10_a[mask]:
    ACF = a * value * value  + b * value  + c
    SS07_10_ACF.append(ACF) 
SS07_10_ACF = np.asarray([ a * value * value  + b * value  + c for value in SS07_10_a[mask] ])
    
SS13pre_10_ACF = list()
for value in SS13pre_10_a[mask]:
    ACF = a * value * value + b * value  + c
    SS13pre_10_ACF.append(ACF) 
    
SS13post_10_ACF = list()
for value in SS13post_10_a[mask]:
    ACF = a * value  * value + b * value   + c
    SS13post_10_ACF.append(ACF) 

SS13un_10_ACF = list()
for value in SS13un_10_a[mask]:
    ACF = a * value *value   + b * value  + c
    SS13un_10_ACF.append(ACF) 
    
  #Translating from ODE to ADF for 1:20 dilution data 
SS07_20_ACF = list()
for value in SS07_20_a[mask]:
    ACF = a * value *value  + b * value   + c
    SS07_20_ACF.append(ACF) 

SS13pre_20_ACF = list()
for value in SS13pre_20_a[mask]:
    ACF = a * value * value + b * value  + c
    SS13pre_20_ACF.append(ACF) 

SS13post_20_ACF = list()
for value in SS13post_20_a[mask]:
    ACF = a * value * value  + b * value + c
    SS13post_20_ACF.append(ACF) 

SS13un_20_ACF = list()
for value in SS13un_20_a[mask]:
    ACF = a * value * value + b * value  + c
    SS13un_20_ACF.append(ACF) 
    
plt.plot(time_labels,SS07_10_ACF)
plt.plot(time_labels,SS13pre_10_ACF)
plt.plot(time_labels,SS13post_10_ACF)
plt.plot(time_labels,SS13un_10_ACF)
plt.plot(time_labels, LB.mean())
plt.ylabel('ACF')
plt.xlabel('Time (sec)')
#plt.legend(['SS07', 'SS13++', 'SS13-+', 'SS13--', 'Blank'])
plt.title('Optical Density for 1/10 Diltuion Factor')
plt.show()

#Graph the growth curve for 1:20 dilution
plt.plot(time_labels,SS07_20_ACF)
plt.plot(time_labels,SS13pre_20_ACF)
plt.plot(time_labels,SS13post_20_ACF)
plt.plot(time_labels,SS13un_20_ACF)
plt.plot(time_labels, LB.mean())
plt.ylabel('optical density (OD)')
plt.xlabel('Time (sec)')
#plt.legend(['SS07', 'SS13++', 'SS13-+', 'SS13--', 'Blank'])
plt.title('Optical Density for 1/20 Diltuion Factor')
plt.show()
   
'''
#Estimating the initial point of the graph by doing a 1:1000 dilution for
#smallest value that was calculated for the ACF for each data set
#Once the guess is made it is then added the beginning of each array
Initial_SS07_10_ACF = SS07_10_ACF[0] / 1000
SS07_10_ACF = np.asarray(SS07_10_ACF)
SS07_10_ACF = np.insert(SS07_10_ACF, 0, Initial_SS07_10_ACF)

Initial_SS13pre_10_ACF = SS13pre_10_ACF[0] / 1000
SS13pre_10_ACF = np.asarray(SS13pre_10_ACF)
SS13pre_10_ACF = np.insert(SS13pre_10_ACF, 0, Initial_SS13pre_10_ACF)

Initial_SS13post_10_ACF = SS13post_10_ACF[0] / 1000
SS13post_10_ACF = np.asarray(SS13post_10_ACF)
SS13post_10_ACF = np.insert(SS13post_10_ACF, 0, Initial_SS13post_10_ACF)

Initial_SS13un_10_ACF = SS13un_10_ACF[0] / 1000
SS13un_10_ACF = np.asarray(SS13un_10_ACF)
SS13un_10_ACF = np.insert(SS13un_10_ACF, 0, Initial_SS13un_10_ACF)

#ACF addition for 1:20 Dilution
Initial_SS07_20_ACF = SS07_20_ACF[0] / 1000
SS07_20_ACF = np.asarray(SS07_20_ACF)
SS07_20_ACF = np.insert(SS07_20_ACF, 0, Initial_SS07_20_ACF)

Initial_SS13pre_20_ACF = SS13pre_20_ACF[0] / 1000
SS13pre_20_ACF = np.asarray(SS13pre_20_ACF)
SS13pre_20_ACF = np.insert(SS13pre_20_ACF, 0, Initial_SS13pre_20_ACF)

Initial_SS13post_20_ACF = SS13post_20_ACF[0] / 1000
SS13post_20_ACF = np.asarray(SS13post_20_ACF)
SS13post_20_ACF = np.insert(SS13post_20_ACF, 0, Initial_SS13post_20_ACF)

Initial_SS13un_20_ACF = SS13un_20_ACF[0] / 1000
SS13un_20_ACF = np.asarray(SS13un_20_ACF)
SS13un_20_ACF = np.insert(SS13un_20_ACF, 0, Initial_SS13un_20_ACF)
'''

# The 1:10 dilution normalization
maxVal = SS07_10_ACF[0]
for value in SS07_10_ACF:
    if value > maxVal:
        maxVal = value
SS07_10_ACF = SS07_10_ACF/maxVal

maxVal = SS13pre_10_ACF[0]
for value in SS13pre_10_ACF:
    if value > maxVal:
        maxVal = value
SS13pre_10_ACF = SS13pre_10_ACF/maxVal

maxVal = SS13post_10_ACF[0]
for value in SS13post_10_ACF:
    if value > maxVal:
        maxVal = value
SS13post_10_ACF = SS13post_10_ACF/maxVal

maxVal = SS13un_10_ACF[0]
for value in SS13un_10_ACF:
    if value > maxVal:
        maxVal = value
SS13un_10_ACF = SS13un_10_ACF/maxVal

# The 1:20 dilution normalization where the max value divides all of the 
# rest of the data values for each data series
'''
maxVal = SS07_20_ACF[0]
for value in SS07_20_ACF:
    if value > maxVal:
        maxVal = value
SS07_20_ACF = SS07_20_ACF/maxVal

maxVal = SS13pre_20_ACF[0]
for value in SS13pre_20_ACF:
    if value > maxVal:
        maxVal = value
SS13pre_20_ACF = SS13pre_20_ACF/maxVal

maxVal = SS13post_20_ACF[0]
for value in SS13post_20_ACF:
    if value > maxVal:
        maxVal = value
SS13post_20_ACF = SS13post_20_ACF/maxVal

maxVal = SS13un_20_ACF[0]
for value in SS13un_20_ACF:
    if value > maxVal:
        maxVal = value
SS13un_20_ACF = SS13un_20_ACF/maxVal

'''
# Normalize with LOQ

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
def Object_20(initial_guesses, data):
    t = time_labels
    output = Gompertz(initial_guesses, t)
    output = np.asarray(output)
    result = np.sum(np.power((data - output), 2))
    return result
    

    
#Calling the objective function and Gompertz for 1/20 dilution
a =1
u = np.log(2)/20./60
y =2500
guesses = (u, y)
initial_guesses = np.asarray(guesses)
estimates = fmin(Object_20, initial_guesses, args = (SS07_20_ACF,))
print estimates

values = Gompertz(estimates, time_labels)
    
plt.plot(time_labels, values)
plt.plot(time_labels, SS07_20_ACF)
plt.show()

   
'''
plt.plot(time_labels,SS07_10_ACF)
plt.plot(time_labels,SS13pre_10_ACF)
plt.plot(time_labels,SS13post_10_ACF)
plt.plot(time_labels,SS13un_10_ACF)
plt.plot(time_labels, LB.mean())
plt.ylabel('ACF')
plt.xlabel('Time (sec)')
plt.legend(['SS07', 'SS13++', 'SS13-+', 'SS13--', 'Blank'])
plt.title('Optical Density for 1/10 Diltuion Factor')
plt.show()
'''
