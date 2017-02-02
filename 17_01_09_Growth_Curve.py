import openpyxl as xlsx
import numpy as np
import matplotlib.pyplot as plt
import data_muncher as dm
from scipy.optimize import fmin
from pylab import polyfit
from pylab import polyval

#Gompertz Code
#Fit of 17_01_09 Data
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

num = 0;
for value in Blank.mean():
    num += value
    
Blank_val = num/len(Blank.mean())

blankAvg = np.asarray(Blank.mean())
blankStd = np.asarray(Blank.std())

LOQ_values = 3 * blankStd
LOQ = np.mean(LOQ_values)
plt.plot(time_labels, MG_Control.mean())
plt.plot(time_labels, MG_Uninduced.mean())
plt.plot(time_labels, MG_Induced.mean())
plt.plot(time_labels, LOQ_values)
plt.legend(['Control', 'Uninduced', 'Induced', 'LOQ'])
plt.show()

#Subtract the Mean of the blank from the Mean of each Data Series
blankAvg = np.asarray(Blank.mean())
blankAvg = np.mean(blankAvg)
blankStd = np.asarray(Blank.std())
#avg = np.mean()

# LOQ is the standard deviation of the blank multiplied by 3
LOQ_values = (3 * blankStd) + Blank.mean()
LOQ = np.mean(LOQ_values)

#Converting to Arrays
MG_ControlAvg = np.asarray(MG_Control.mean())
MG_UninducedAvg = np.asarray(MG_Uninduced.mean())
MG_InducedAvg = np.asarray(MG_Induced.mean())

#Converting th arbitrary concentration units
'''
ACF = ((Asample - B)/(ALoq - B))
'''

blank = np.mean(blankAvg)

#Generate the masked arrays
mask_Control = (MG_ControlAvg > LOQ)
mask_Uninduced = (MG_UninducedAvg > LOQ)
mask_Induced = (MG_InducedAvg > LOQ)

#Convert to ACF and Generate the standard of the LOQ
Control_ACF = ((MG_ControlAvg - blankAvg)/(LOQ - blank))
Uninduced_ACF = ((MG_UninducedAvg - blankAvg)/(LOQ - blank))
Induced_ACF = ((MG_InducedAvg - blankAvg)/(LOQ - blank))

#Plot the ACF and Generated data for the standard LOQ
plt.plot(time_labels, Control_ACF)
plt.plot(time_labels, Uninduced_ACF)
plt.plot(time_labels, Induced_ACF)
plt.plot(time_labels, LOQ_values)
plt.legend(['Control', 'Uninduced', 'Induced', 'LOQ'])
plt.show()

#Apply the Mask
MG_Control_ACF = Control_ACF[mask_Control]
MG_Uninduced_ACF = Uninduced_ACF[mask_Uninduced]
MG_Induced_ACF = Induced_ACF[mask_Induced]

#Convert to array
MG_Control_ACF = np.asarray(MG_Control_ACF)
MG_Uninduced_ACF = np.asarray(MG_Uninduced_ACF)
MG_Induced_ACF = np.asarray(MG_Induced_ACF)

'''
Do not need to divide by LOQ because already standardized according to the 
code above
'''

# Estimating the initial point of the graph by doing a 1:10^6 dilution for
# Absorbance Measurement 
Control_Initial = 0.795
Uninduced_Initial = 0.740
Induced_Initial = 0.748

#Convert the initial point to ACF unites
Control_Initial_ACF = ((Control_Initial - blankAvg)/(LOQ - blank))
Uninduced_Initial_ACF = ((Uninduced_Initial - blankAvg)/(LOQ-blank))
Induced_Initial_ACF = ((Induced_Initial - blankAvg)/(LOQ - blank))

#Take the initial and then back dilute by 10^-6 
#Must be in ACF before diluting because this is how it is possible 
#to determine get corect dilituion since it is initially in Absorbance units

#Divide by ON by 10^6 to get the initial concentration
Control_Initial_ACF = Control_Initial_ACF/(10E6)
Uninduced_Initial_ACF = Uninduced_Initial_ACF/(10E6)
Induced_Initial_ACF = Induced_Initial_ACF/(10E6)

#Insert the Initial guesses
MG_Control_ACF[0] = Control_Initial_ACF
MG_Uninduced_ACF = np.insert(MG_Uninduced_ACF, 0, Uninduced_Initial_ACF)
MG_Induced_ACF = np.insert(MG_Induced_ACF, 0, Induced_Initial_ACF)

#mask time 
time_control = time_labels[mask_Control]
time_uninduced = time_labels[mask_Uninduced]
time_induced = time_labels[mask_Induced]

#Convert time to array
time_control = np.asarray(time_control)
time_uninduced = np.asarray(time_uninduced)
time_induced = np.asarray(time_induced)

#insert an additional time point at t= 0 for the initial concentration
time_uninduced = np.insert(time_uninduced, 0, 0)
time_induced = np.insert(time_induced, 0, 0)

plt.plot(time_control,MG_Control_ACF)
plt.plot(time_uninduced, MG_Uninduced_ACF)
plt.plot(time_induced, MG_Induced_ACF)
plt.plot(time_labels, LOQ_values)
plt.legend(['Control', 'Uninduced', 'Induced', 'LOQ'])
plt.show()

#Take the natural log 
MG_Control_ACF_log = np.log(MG_Control_ACF)
MG_Uninduced_ACF_log = np.log(MG_Uninduced_ACF)
MG_Induced_ACF_log = np.log(MG_Induced_ACF)

plt.plot(time_control,MG_Control_ACF_log)
plt.plot(time_uninduced, MG_Uninduced_ACF_log)
plt.plot(time_induced, MG_Induced_ACF_log)
plt.plot(time_labels, LOQ_values)
plt.legend(['Control', 'Uninduced', 'Induced', 'LOQ'])
plt.show()

#determine the linear regression for the plot
(m, b, c, d) = polyfit(time_control[0:4] , MG_Control_ACF_log[0:4], 3)
yp_control = polyval([m, b, c, d], time_labels)

index = 0
for x in yp_control:
    a = 0
    a = x
    if a > MG_Control_ACF_log[0]:
        break
    index += 1
    
time_control_2 = np.insert(time_control, 1, (index * 600)) 
MG_Control_ACF_log_2 = np.insert(MG_Control_ACF_log, 1, yp_control[index])     

#Cannot modify the MG_Uninduced because the linear regression line falls
#above the inital point guess


(m, b) = polyfit(time_uninduced[1:3] , MG_Uninduced_ACF_log[1:3], 1)
yp_uninduced= polyval([m, b], time_labels)

index = 0
for x in yp_uninduced:
    a = 0
    a = x
    if a > MG_Uninduced_ACF_log[0]:
        break
    index += 1
    
time_uninduced = np.insert(time_uninduced, 1, (index * 600)) 
MG_Uninduced_ACF_log = np.insert(MG_Uninduced_ACF_log, 1, yp_uninduced[index])


#(m, b) = polyfit(time_induced[1:5] , MG_Induced_ACF_log[1:5], 1)
#yp_induced= polyval([m, b], time_labels)
(m, b, c, d) = polyfit(time_induced[0:4] , MG_Induced_ACF_log[0:4], 3)
yp_induced= polyval([m, b, c, d], time_labels)

index = 0
for x in yp_induced:
    a = 0
    a = x
    if a > MG_Induced_ACF_log[0]:
        break
    index += 1
    
time_induced_2 = np.insert(time_induced, 1, (index * 600)) 
MG_Induced_ACF_log_2 = np.insert(MG_Induced_ACF_log, 1, yp_induced[index])
#MG_Induced_ACF_log_2 = np.insert(MG_Induced_ACF_log, 1, -8.2368454671488962)

plt.plot(time_control_2, MG_Control_ACF_log_2)
plt.plot(time_uninduced, MG_Uninduced_ACF_log)
plt.plot(time_induced_2, MG_Induced_ACF_log_2)
plt.plot(time_labels, LOQ_values)
plt.legend(['Control', 'Uninduced', 'Induced', 'LOQ'])
plt.show()


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
    return result

'''
Control with Guess
'''
# a = max Value
# u = growth rate
# y = beginning linear range  (lag time)  
#Calling the objective function and Gompertz for 10^-6 dilution
#Culture 1 Fit
a = 2.28821825e+01
u = 6.24008204e-04
y = 5.80621779e+03
guesses = (a, u, y)
initial_guesses = np.asarray(guesses)

MG_Control_ACF_log_2 = 18 + MG_Control_ACF_log_2
estimates1 = fmin(Object, initial_guesses, args = (MG_Control_ACF_log_2,time_control_2))
print estimates1


time =  np.linspace(0, max(time_control_2), 101)
values1 = Gompertz(estimates1, time)
MG_Control_ACF_log_2 = MG_Control_ACF_log_2 - 18
for i in range(len(values1)):
  values1[i] -= 18
plt.plot(time, values1, 'b')
plt.plot(time_control_2, MG_Control_ACF_log_2, 'go')
plt.plot(time_labels, LOQ_values, 'k')
plt.legend(['Gompertz', 'Control w/ Guess', 'LOQ'], loc = 'lower right')
plt.ylabel('ACF (Arbitrary Concentration Factor)')
plt.xlabel('Time (sec)')
plt.show()

'''
Control
'''
a = 2.29861400e+01
u =  5.78233857e-04
y = 3.39201411e+03
guesses = (a, u, y)
initial_guesses = np.asarray(guesses)

MG_Control_ACF_log = 18 + MG_Control_ACF_log
estimates1 = fmin(Object, initial_guesses, args = (MG_Control_ACF_log,time_control))
print estimates1

time =  np.linspace(0, max(time_control), 101)
values1 = Gompertz(estimates1, time)
MG_Control_ACF_log = MG_Control_ACF_log - 18
for i in range(len(values1)):
  values1[i] -= 18
plt.plot(time, values1, 'b')
plt.plot(time_control, MG_Control_ACF_log, 'ko')
plt.plot(time_labels, LOQ_values, 'k')
plt.legend(['Gompertz', 'Control', 'LOQ'], loc = 'lower right')
plt.ylabel('ACF (Arbitrary Concentration Factor)')
plt.xlabel('Time (sec)')
plt.show()

'''
Uninduced
'''
a = 2.28056854e+01
u =  5.51946980e-04 
y = 3.95755497e+03
guesses = (a, u, y)
initial_guesses = np.asarray(guesses)

MG_Uninduced_ACF_log = 18 + MG_Uninduced_ACF_log
estimates1 = fmin(Object, initial_guesses, args = (MG_Uninduced_ACF_log,time_uninduced))
print estimates1

time =  np.linspace(0, max(time_uninduced), 101)
values1 = Gompertz(estimates1, time)
MG_Uninduced_ACF_log = MG_Uninduced_ACF_log - 18
for i in range(len(values1)):
  values1[i] -= 18
plt.plot(time, values1, 'b')
plt.plot(time_uninduced, MG_Uninduced_ACF_log, 'ko')
plt.plot(time_labels, LOQ_values, 'k')
plt.legend(['Gompertz', 'Uninduced', 'LOQ'], loc = 'lower right')
plt.ylabel('ACF (Arbitrary Concentration Factor)')
plt.xlabel('Time (sec)')
plt.show()

'''
Induced with Guess
'''
# a = max Value
# u = growth rate
# y = beginning linear range  (lag time)  
#Calling the objective function and Gompertz for 10^-6 dilution
#Culture 1 Fit
a = 2.28647142e+01
u = 5.34367027e-04
y = 3.63885263e+03
guesses = (a, u, y)
initial_guesses = np.asarray(guesses)

MG_Induced_ACF_log_2 = 18 + MG_Induced_ACF_log_2
estimates1 = fmin(Object, initial_guesses, args = (MG_Induced_ACF_log_2,time_induced_2))
print estimates1


time =  np.linspace(0, max(time_induced_2), 101)
values1 = Gompertz(estimates1, time)
MG_Induced_ACF_log_2 = MG_Induced_ACF_log_2 - 18
for i in range(len(values1)):
  values1[i] -= 18
plt.plot(time, values1, 'b')
plt.plot(time_induced_2, MG_Induced_ACF_log_2, 'go')
plt.plot(time_labels, LOQ_values, 'k')
plt.legend(['Gompertz', 'Induced w/ Guess', 'LOQ'], loc = 'lower right')
plt.ylabel('ACF (Arbitrary Concentration Factor)')
plt.xlabel('Time (sec)')
plt.show()

'''
Induced
'''
a = 2.28512755e+01
u =  5.40429197e-04 
y = 12000
guesses = (a, u, y)
initial_guesses = np.asarray(guesses)

MG_Induced_ACF_log = 18 + MG_Induced_ACF_log
estimates1 = fmin(Object, initial_guesses, args = (MG_Induced_ACF_log,time_induced))
print estimates1

time =  np.linspace(0, max(time_induced), 101)
values1 = Gompertz(estimates1, time)
MG_Induced_ACF_log = MG_Induced_ACF_log - 18
for i in range(len(values1)):
  values1[i] -= 18
plt.plot(time, values1, 'b')
plt.plot(time_induced, MG_Induced_ACF_log, 'ko')
plt.plot(time_labels, LOQ_values, 'k')
plt.legend(['Gompertz', 'Induced', 'LOQ'], loc = 'lower right')
plt.ylabel('ACF (Arbitrary Concentration Factor)')
plt.xlabel('Time (sec)')
plt.show()

