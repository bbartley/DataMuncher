import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import fmin
import data_muncher as dm


f = '17_01_09 Growth Curve.xlsx'

ex = dm.Experiment(f)
def time_labels(ex):
    data_series = ex.read('Time [s]')
    time_labels = data_series.list_of_series[0]
    time_labels = np.asarray(time_labels)
    return time_labels  

def read_plate(ex, row_ids=[], nums=[], *args):
    PlateReadout = dm.Sample();
    column_ids = map(str, range(nums[0], nums[1]))
    well_ids = [ r + c for r in row_ids for c in column_ids if ex.search(r + c)]
    for w in well_ids:
        W = dm.Well();
        W.measurements = ex.read(w)  #Read well data vertically in columns from plate reader spreadsheet
        PlateReadout.addWell(w, W) 
    return PlateReadout
        
def read_sample(PlateReadout, sample_ids=[], *args):
    Sample = dm.Sample()
    for ids in sample_ids:
        Sample.addWell(ids, PlateReadout[ids])
    return Sample
   
def LOQ_calc(Blank):
    blankAvg = np.asarray(Blank.mean())
    blankStd = np.asarray(Blank.std())
    TotalStd = np.sqrt(np.sum(np.power(blankStd, 2)))
    LOQ = 3 * TotalStd + np.mean(blankAvg)
    return LOQ
    
def initial_pt(val, blankAvg , LOQ):
    Initial_ACF = ((val - np.mean(blankAvg))/(LOQ - np.mean(blankAvg)))
    return Initial_ACF
    
def mask(sample, LOQ):
    mask = (sample > LOQ)
    return mask
    
def mask_apply(sample, LOQ, blankAvg):
    sample_mask = mask(sample, LOQ)
    time = time_labels(ex)
    sample_ACF = ((InducedAvg - blankAvg)/(LOQ - blankAvg))
    sample_ACF = sample_ACF[sample_mask ]
    sample_time = time[sample_mask]
    sample_time = np.asarray(sample_time)
    return (sample_ACF, sample_time)

def insert_initial(val, blankAvg, InducedAvg, LOQ):
    Initial = initial_pt(val, blankAvg, LOQ)
    masked_vals = mask_apply(InducedAvg, LOQ, blankAvg)
    Initial_ACF = Initial/(10E6)
    sample_ACF = np.insert(masked_vals[0], 0, Initial_ACF)
    sample_time = np.insert(masked_vals[1], 0, 0)
    return (sample_ACF, sample_time)
    
def log(val, blankAvg, InducedAvg, LOQ):
    ACF_log = insert_initial(val, blankAvg, InducedAvg, LOQ)
    ACF_log = np.log(ACF_log[0])
    ACF_log = ACF_log - (ACF_log[0])
    return ACF_log
    
def Gompertz(initial_guesses, t):
    results = []
    e = np.exp(1)
    for x in t:
        results.append( initial_guesses[0] * np.exp(-np.exp(((initial_guesses[1]*e)/ initial_guesses[0])*((initial_guesses[2] -x) + 1))))
    return results
    
def Object(initial_guesses, data, time):
    output = Gompertz(initial_guesses, time)
    output = np.asarray(output)
    result = np.sum(np.power((data - output), 2))
    return result
    
a = 1.56567557e+01
u =  7.18991900e-04
y = 2.07319236e+04
guesses = (a, u, y)
initial_guesses = np.asarray(guesses)

def graph_fit(initial_guesses, val, blankAvg, InducedAvg, LOQ):
    sample_data = insert_initial(val, blankAvg, InducedAvg, LOQ)
    sample_time = sample_data[1]
    sample_log = log(val, blankAvg, InducedAvg, LOQ)
    estimates = fmin(Object, initial_guesses, args = (sample_log, sample_time))
    graph_time =  np.linspace(0, max(sample_time), 101)
    values = Gompertz(estimates, graph_time) 
    plt.plot(graph_time, values)
    plt.plot(sample_time, sample_log, 'ko')
    plt.legend(['Gompertz', 'Sample'], loc = 'lower right')
    plt.ylabel('ACF (Arbitrary Concentration Factor)')
    plt.xlabel('Time (sec)')
    plt.title('Induced')
    return (graph_time, values)
    

    
    
'''

#values1 = values1 + np.log(Induced_Initial_ACF)
#Induced_ACF_log = Induced_ACF_log + np.log(Induced_Initial_ACF)

#plt.plot(time, values1, 'b')
#plt.plot(time_induced, Induced_ACF_log, 'ko')
plt.legend(['Gompertz', 'Induced', 'LOQ'], loc = 'lower right')
plt.ylabel('ACF (Arbitrary Concentration Factor)')
plt.xlabel('Time (sec)')
plt.title('Induced')
plt.show()

      '''  
ids = ['A10', 'A12', 'B10', 'B11', 'C10', 'C11', 'C12']
plate = read_plate(ex, ['A', 'B', 'C'] , [1, 13])
Blank = read_sample(plate, ids)
LOQ = LOQ_calc(Blank)

induced_ids = ['A7', 'B7', 'C7']
Induced = read_sample(plate, induced_ids)
InducedAvg = np.asarray(Induced.mean())

blankAvg = np.asarray(Blank.mean())

initial = initial_pt(0.748, blankAvg, LOQ)

initial_mask = mask(InducedAvg, LOQ)

apply_mask = mask_apply(InducedAvg, LOQ, blankAvg)

insert = insert_initial(0.748, blankAvg, InducedAvg, LOQ)

val = 0.748

#estimates = minimize(initial_guesses, 0.740, blankAvg, InducedAvg, LOQ)
value = log(val, blankAvg, InducedAvg, LOQ)
print value

graph = graph_fit(initial_guesses, val, blankAvg, InducedAvg, LOQ)
    
    
    
#induced.read_plate(['A','B', 'C'], [1, 13])