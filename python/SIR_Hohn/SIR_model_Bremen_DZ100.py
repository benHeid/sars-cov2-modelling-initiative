#SIR_model.py for Germany

import numpy as np
import scipy.optimize as opt

import matplotlib.pyplot as plt
from pylab import *
import matplotlib.colors as mcolors
from scipy.optimize import curve_fit
import math
from scipy.stats import norm
import matplotlib.mlab as mlab
import scipy.special as sp

# data:
data_file="./Corona_infections_Bremen.txt"
Binf = np.genfromtxt(data_file,skip_header=0,filling_values=-999.,delimiter="\t")

data_file="./Corona_deaths_Bremen.txt"
Bdead = np.genfromtxt(data_file,skip_header=0,filling_values=-999.,delimiter="\t")

data_file="./Corona_recovered_Bremen.txt"
Brec = np.genfromtxt(data_file,skip_header=0,filling_values=-999.,delimiter="\t")



P=820000.0 # average population size between 1990 and 2018
P1=81800000.0
# parameters: constrained
b= 0.009019 * 1.0/360.0 # birth rate (per year) 
#theta= 0.003024 * 1.0/360.0 # immigration rate of susceptible (people per day)
theta=0.0 # due to closed borders
d= 0.010615 * 1.0/360.0 # death rate of healthy individuals (per year)



# parameters: unconstrained
# infection dynamics:
a= 0.03 # probability that the disease is transmitted upon contact
c= 4.70/P # contact rate per susceptible individual

# recovery and mortality
#delta= 0.033 # death rate of infected individuals # based on Chinese data
delta= 0.000021 # death rate of infected individuals # based on GERMAN data


rho= 0.03 # recovery rate for infected individuals

# immunity or not?
sigma= 0.0 # rate of recovered individuals that become susceptible for reinfection

# initialization
tmax=365
dt=1.0

S=np.zeros(tmax)
I=np.zeros(tmax)
R=np.zeros(tmax)
D=np.zeros(tmax)
time=np.arange(0,tmax,1)
DDt=np.zeros(tmax-1)


S[0]=P
I[0]=42.0*100.0
R[0]=0.0

for i in range(tmax-1):
    if i>15:
        c=2.0/P
        if i>20:
            rho=0.06
    
    # susceptible fraction of population
    dSdt=theta*S[i]+b*S[i]-d*S[i] - a*c*S[i]*I[i] + sigma*R[i]
    # infected fraction of population
    dIdt=a*c*S[i]*I[i] - delta*I[i] - rho*I[i]
    # recovered fraction of population
    dRdt=rho*I[i] - sigma*R[i] - d*R[i]
    
    S[i+1]=S[i]+dSdt*dt
    I[i+1]=I[i]+dIdt*dt
    R[i+1]=R[i]+dRdt*dt
    D[i+1]=D[i]+delta*I[i]*dt
    
    DDt[i]=np.log(2.0)/np.log(1.0+a*c*S[i])
    

print 'total fatalities=', D[tmax-1]


plt.figure(1)
#plt.plot(time,S,'b',label='susceptible')
#plt.plot(time,0.01*(I+R),'r',label='infected cumulative')
plt.plot(time,(I+R),'r',label='true infected cumulative')
plt.plot(time,I,'m',label='true infected active')
plt.plot(time,R,'g',label='true recovered')
plt.plot(time,D,'c',label='dead')
#plt.plot(time,S+I+R,'k',label='total population')
#plt.plot(Binf,'ro',label='infections')
#plt.plot(Bdead,'bo',label='deaths')
#plt.plot(Brec,'go',label='recovered')
plt.xlabel('days after 11th of March')
plt.ylabel('number of people')
plt.title('Covid Model for Bremen plus surrounding (assuming 99\% unreported cases)')
plt.legend(loc=5)


#plt.figure(2)
##plt.plot(time,I,'g',label='active Infections') # 2% der Infizierten entwickeln eine Pneumonie, Quelle RKI
#plt.plot(time,I*0.13,'b',label='Hospitalized') # 2% der Infizierten entwickeln eine Pneumonie, Quelle RKI
#plt.plot(time,I*0.02,'r',label='Pneumonia') # 2% der Infizierten entwickeln eine Pneumonie, Quelle RKI
#plt.xlabel('days after 11th of March')
#plt.ylabel('number of people')
#plt.title('Hospitalized cases')
#plt.legend(loc=1)



#plt.figure(3)
#plt.plot(DDt,'b',label='doubling time')
#plt.xlabel('days after 11th of March')
#plt.ylabel('days')
#plt.legend(loc=1)


print 'Verdoppelungszeit=',DDt[7]
print 'Verdoppelungszeit=',DDt[tmax-2]


#lenBinf=len(Binf)
#doubletime=np.zeros(lenBinf-1)
#for j in range(lenBinf-1):
#    doubletime[j]=np.log(2.0)/np.log(1.0+(Binf[j+1]-Binf[j])/Binf[j])


#plt.figure(4)
#plt.plot(doubletime,'bo',label='Verdoppelungszeit Daten')
#plt.legend(loc=1)

print np.max(I)*0.13
print np.max(I)*0.02

plt.show()

