# -*- coding: utf-8 -*-
"""
Created on Thu Nov 03 19:13:55 2016

@author: James
"""
import tellurium as te
import roadrunner
import matplotlib.pyplot as plt
import numpy as np

r = te.loada("""
J1: LacI+ P1 -> LacI_P1;  k1 * P1 * LacI;
J2: -> gRNA; k2 * P2;
J3: -> mCherry + dCas9; k3 * (P1 + P3);
J4: dCas9 + gRNA -> dCas9_gRNA; k6 * dCas9 * gRNA ;
J5: dCas9_gRNA + P3 -> dCas9_gRNA_P1; k7 * dCas9_gRNA * P3;
J6: LacI + $IPTG -> LacI_IPTG; k8 * LacI * IPTG;
J7: mCherry -> ; k10




P2 = 1;
P1 = 1;
mCherry_RNA = 0;
dCas9_RNA = 1;
gRNA = 3.5;
aTc_TetR = 0;
$LacI = 1;
IPTG = 0;
at (time > 100): IPTG = IPTG + 1;


k1 = 2.1;
k2 = 3;
k3 = 4;
k4 = 2;
k5 = 1.3;
k6 = 1;
k7 = 0.7;
k8 = 1;
k10 = 1.2;
k11 = 2


""")


result = r.simulate(0, 2, 1000, ['time',  'mCherry', 'IPTG'])
print r.getFullStoichiometryMatrix()
r.plot()

#a = result[:, 0]
#plt.plot(result[:, 0], result[:, 2])
#plt.plot(result[:, 1], result[:, 2])
#plt.xscale('log')
#plt.xlabel('IPTG and aTc (log scale)')
#plt.ylabel('glk')
#plt.xlim(xmin = 6E-2)
#plt.show()



#print r.getFullStoichiometryMatrix()

# Turn of notices so they don't clutter the output
'''
te.noticesOff()
for x in np.arange(0, 6):
    result = r.simulate (0, 4, 500, ['IPTG','glk'])
    r.reset()
    plt.plot(result[:, 0], result[:, 1], linewidth=1.0, linestyle='-', alpha=0.8)
    plt.legend('1' '2' '3''4' '5' '6' )
    plt.xscale('log')
    plt.xlabel('IPTG (log scale)')
    plt.ylabel('glk')
    r.IPTG = r.IPTG + 0.5
# Turn the notices back on
plt.show()
te.noticesOn()
'''



'''
k1 = 0.02;
k2 = 4.1E-3;
k3 = 0.02;
k4 = 4.1E-2;
k5 = 0.02;
k6 = 4.1E-3;
k7 = 4.1E-2;
k8 = 6.3E-5;
'''

'''
IPTG sigmodial values
TetR = 1;
PTet = 1;
P1 = 1;
PTet = 1;
P3 = 1;
TetR_Ptet = 1;
glk = 1;
aTc = 1;
aTc_TetR = 1;
LacI = 1;
LacO = 1;
IPTG = 0.8;

k1 = 0.2;
k2 = 0.001;
k3 = 0.003;
k4 = 0.5;
k5 = 0.1;
k6 = 0.5;
k7 = 65;
k8 = 0.0001;
'''

'''
TetR = 1;
PTet = 1;
P1 = 1;
PTet = 1;
P3 = 1;
TetR_Ptet = 1;
glk = 1;
aTc = 1;
aTc_TetR = 1;
LacI = 1;
IPTG = 0.1;


k1 = 2;
k2 = 0.1;
k3 = 5;
k4 = 4.2;
k5 = 1;
k6 = 0.5;
k7 = 0.33;
k8 = 4.3;
'''