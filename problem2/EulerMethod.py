import random
import sys
from matplotlib.pyplot import show
from pylab import *

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

plot(tr,sr)
plot(tr,ir)
plot(tr,rr)
show()

