import random
import sys
import numpy as np
from matplotlib.pyplot import show
from pylab import *
import time

start_time = time.time()

def initialization():
    global s, r, i, t, sr, ir, rr, tr
    s=float(sys.argv[1])
    i=float(sys.argv[2])
    r=float(sys.argv[3])
    t=0
    sr=[s]
    ir=[i]
    rr=[r]
    tr=[t]

def observe():
    global s, r, i, t, sr, ir, rr, tr
    sr.append(s)
    ir.append(i)
    rr.append(r)
    tr.append(t)

def update():
    global s, r, i, t

    s1=s-B*s*i*dt
    i1=i+(B*s*i-k*i)*dt
    r1=r+k*i*dt
    t= t + dt
    s, i, r = s1, i1, r1

B=float(sys.argv[4])
k=float(sys.argv[5])
dt=float(sys.argv[6])
tf=int(sys.argv[7])

initialization()
for t in range(tf):
    update()
    observe()

plt.plot(tr,sr,label='Susceptible population')
plt.plot(tr,ir,label='Infected population')
plt.plot(tr,rr,label='Recovered population')
plt.title('Evolution of an infectious disease in a population')
plt.xlabel('Time')
plt.ylabel('Population')
plt.legend(loc='center right')
plt.show()

data = np.column_stack((tr, sr, ir, rr))
np.savetxt('data_euler.txt', data, delimiter='\t', header='Time\tPopulation', fmt='%.4f')

end_time = time.time()
computational_time_euler = end_time - start_time
print(f"Computational Time - Forward Euler: {computational_time_euler} seconds")
