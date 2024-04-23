import random
import sys
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
    k1s=-dt*B*s*i
    k1i=dt*(B*s*i-k*i)

    k2s=-dt*B*(s+k1s/2)*(i+k1i/2)
    k2i=dt*(B*(s+k1s/2)*(i+k1i/2)-k*(i+k1i/2))

    k3s=-dt*B*(s+k2s/2)*(i+k2i/2)
    k3i=dt*(B*(s+k2s/2)*(i+k2i/2)-k*(i+k2i/2))

    k4s=-dt*B*(s+k3s)*(i+k3i)
    k4i=dt*(B*(s+k3s)*(i+k3i)-k*(i+k3i))

    k1r=dt*k*i
    k2r=dt*k*(i+k1i/2)
    k3r=dt*k*(i+k2i/2)
    k4r=dt*k*(i+k3i)


    s1=s+(k1s+2*k2s+2*k3s+k4s)/6
    i1=i+(k1i+2*k2i+2*k3i+k4i)/6
    r1=r+(k1r+2*k2r+2*k3r+k4r)/6
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
np.savetxt('data_rk.txt', data, delimiter='\t', header='Time\tPopulation', fmt='%.4f')

end_time = time.time()
computational_time_euler = end_time - start_time
print(f"Computational Time - Runge-Kutta: {computational_time_euler} seconds")
