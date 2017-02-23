# -*- coding: utf-8 -*-
"""
Created on Wed Feb 22 17:27:28 2017

@author: bryan
"""
import openpyxl as xlsx
import numpy as np
import matplotlib.pyplot as plt
import data_muncher as dm
from scipy.optimize import fmin
#from pylab import polyfit
#from pylab import polyval
from numpy import polyfit
from numpy import polyval

f = '17_01_09 Growth Curve.xlsx'

ex = dm.Experiment(f);
data_series = ex.read('Time [s]')
time_labels = data_series.list_of_series[0]
time_labels = np.asarray(time_labels)

PlateReadout = dm.Sample();
row_ids = ['A', 'B', 'C']
column_ids = map(str, range(1, 13))
well_ids = [ r + c for r in row_ids for c in column_ids if ex.search(r + c)]
for w in well_ids:
    W = dm.Well();
    W.measurements = ex.read(w)  #Read well data vertically in columns from plate reader spreadsheet
    PlateReadout.addWell(w, W)
data_series = PlateReadout.get_measurements()

#Assigning Samples from plate layout
#All of the dilutions are 10^6
MG_Control = dm.Sample()
MG_Control.addWell('A1', PlateReadout['A1'])
MG_Control.addWell('B1', PlateReadout['B1'])
MG_Control.addWell('C1', PlateReadout['C1'])

MG_Uninduced = dm.Sample()
MG_Uninduced.addWell('A4', PlateReadout['A4'])
MG_Uninduced.addWell('B4', PlateReadout['B4'])
MG_Uninduced.addWell('C4', PlateReadout['C4'])

MG_Induced = dm.Sample()
MG_Induced.addWell('A7', PlateReadout['A7'])
MG_Induced.addWell('B7', PlateReadout['B7'])
MG_Induced.addWell('C7', PlateReadout['C7'])

#only the MG strain was analyzed because it showed the variation in the
#fluorescence measurements

#Blank
Blank = dm.Sample()
Blank.addWell('A10', PlateReadout['A10'])
#Blank.addWell('A11', PlateReadout['A11'])
Blank.addWell('A12', PlateReadout['A12'])
Blank.addWell('B10', PlateReadout['B10'])
Blank.addWell('B11', PlateReadout['B11'])
#Blank.addWell('B12', PlateReadout['B12'])
Blank.addWell('C10', PlateReadout['C10'])
Blank.addWell('C11', PlateReadout['C11'])
Blank.addWell('C12', PlateReadout['C12'])


# Sum the variances over time and over wells
blankAvg = np.asarray(Blank.mean())
blankStd = np.asarray(Blank.std())
TotalStd = np.sqrt(np.sum(np.power(blankStd, 2)))
LOQ = 3 * TotalStd + np.mean(blankAvg)

'''
Control
'''
Control = dm.Sample()
Control.addWell('A1', PlateReadout['A1'])
Control.addWell('B1', PlateReadout['B1'])
Control.addWell('C1', PlateReadout['C1'])
ControlAvg = np.asarray(Control.mean())

Control_Initial = 0.795
### Factor out a separate function for calculating ACF
#Convert the initial point to ACF unites
Control_Initial_ACF = ((Control_Initial - np.mean(blankAvg))/(LOQ - np.mean(blankAvg)))

#Take the initial and then back dilute by 10^-6 
#Must be in ACF before diluting because this is how it is possible 
#to determine get corect dilituion since it is initially in Absorbance units

### Dilution factor should be a constant defined at the beginning of the file, rather than be hard-coded 

#Divide by ON by 10^6 to get the initial concentration
Control_Initial_ACF = Control_Initial_ACF/(10E6)


Control_ACF = ((ControlAvg - blankAvg)/(LOQ - blankAvg))


#Apply the Mask
mask_Control = (ControlAvg > LOQ)
Control_ACF = Control_ACF[mask_Control]

time_control = time_labels[mask_Control]
time_control = np.asarray(time_control)

#Insert the Initial guesses
Control_ACF = np.insert(Control_ACF, 0, Control_Initial_ACF)
time_control = np.insert(time_control, 0, 0)


Control_ACF_log = np.log(Control_ACF)
Control_ACF_log = Control_ACF_log - np.log(Control_Initial_ACF)

def Gompertz(initial_guesses, t):
    results = [] # collects the returned values
    e = np.exp(1)
    for x in t:
        results.append( initial_guesses[0] * np.exp(-np.exp(((initial_guesses[1]*e)/ initial_guesses[0])*((initial_guesses[2] -x) + 1))))
    return results
  
# Solving the Objective function for a given set of gueses for 1/20 dilutution data set
# used for the optimization
def Object(initial_guesses, data, time):
    output = Gompertz(initial_guesses, time)
    output = np.asarray(output)
    result = np.sum(np.power((data - output), 2))
#    result = ((time[2]/600)*np.sum(np.power((data[0]-output[0]),2))) + (np.sum(np.power((data[1:len(data)] - output[1:len(output)]), 2)))
    return result

a = 2.29861400e+01
u =  5.71423395e-04
y = 3.09531489e+03
guesses = (a, u, y)
initial_guesses = np.asarray(guesses)

#Control_ACF_log = 18 + Control_ACF_log
estimates1 = fmin(Object, initial_guesses, args = (Control_ACF_log,time_control))
print estimates1

time =  np.linspace(0, max(time_control), 101)
values1 = Gompertz(estimates1, time)
values1 = values1 + np.log(Control_Initial_ACF)
Control_ACF_log = Control_ACF_log + np.log(Control_Initial_ACF)
#for i in range(len(values1)):
#  values1[i] -= 18
plt.plot(time, values1, 'b')
plt.plot(time_control, Control_ACF_log, 'ko')
#plt.plot(time_labels, LOQ_values, 'k')
plt.legend(['Gompertz', 'Control', 'LOQ'], loc = 'lower right')
plt.ylabel('ACF (Arbitrary Concentration Factor)')
plt.xlabel('Time (sec)')
plt.title('Control')
plt.show()

