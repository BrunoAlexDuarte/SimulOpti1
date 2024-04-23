import numpy as np
import matplotlib.pyplot as plt

data_euler = np.loadtxt('data_euler.txt')
data_rk = np.loadtxt('data_rk.txt')

time_euler = data_euler[:, 0]
population_euler = data_euler[:, 1]

time_rk = data_rk[:, 0]
population_rk = data_rk[:, 1]

plt.figure(figsize=(12, 6))

plt.subplot(1, 2, 1)
plt.plot(time_euler, population_euler, label='Forward Euler', color='b')
plt.plot(time_rk, population_rk, label='Runge-Kutta', color='r')
plt.title('Population Over Time')
plt.xlabel('Time')
plt.ylabel('Population')
plt.legend()

# Calculate and plot errors
error = np.abs(population_euler - population_rk)

plt.subplot(1, 2, 2)
plt.plot(time_euler, error, label='Error', color='g')
plt.title('Error Between Methods')
plt.xlabel('Time')
plt.ylabel('Absolute Error')
plt.legend()

plt.tight_layout()
plt.show()