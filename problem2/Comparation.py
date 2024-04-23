import numpy as np
import matplotlib.pyplot as plt

data_euler = np.loadtxt('data_euler.txt')
data_rk = np.loadtxt('data_rk.txt')

time_euler = data_euler[:, 0]
s_euler = data_euler[:, 1]
i_euler = data_euler[:, 2]
r_euler = data_euler[:, 3]

time_rk = data_rk[:, 0]
s_rk = data_rk[:, 1]
i_rk = data_rk[:, 2]
r_rk = data_rk[:, 3]
plt.figure(figsize=(12, 6))

plt.subplot(1, 2, 1)
plt.plot(time_euler, s_euler, label='s Forward Euler', color='b')
plt.plot(time_euler, i_euler, label='i Forward Euler', color='r')
plt.plot(time_euler, r_euler, label='r Forward Euler', color='g')

plt.plot(time_rk, s_rk, label='s Runge-Kutta', color='b')
plt.plot(time_rk, i_rk, label='i Runge-Kutta', color='r')
plt.plot(time_rk, r_rk, label='r Runge-Kutta', color='g')
plt.title('Population Over Time')
plt.xlabel('Time')
plt.ylabel('Population')
plt.legend()

# Calculate and plot errors
s_error = np.abs(s_euler - s_rk)
i_error = np.abs(i_euler - i_rk)
r_error = np.abs(r_euler - r_rk)


plt.subplot(1, 2, 2)
plt.plot(time_euler, s_error, label='s Error', color='b')
plt.plot(time_euler, i_error, label='i Error', color='r')
plt.plot(time_euler, r_error, label='r Error', color='g')
plt.title('Error Between Methods')
plt.xlabel('Time')
plt.ylabel('Absolute Error')
plt.legend()

plt.tight_layout()
plt.show()