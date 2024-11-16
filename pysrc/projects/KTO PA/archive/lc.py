import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import odeint

# LC circuit parameters
L = 0.05  # Inductance in henries
C = 0.001  # Capacitance in farads
V0 = 5  # Initial voltage across the capacitor in volts

# Define the differential equations for the LC circuit
def lc_circuit(X, t, L, C):
    Vc, I = X  # Vc is the capacitor voltage, I is the current
    dVc_dt = I / C  # Voltage across capacitor
    dI_dt = -Vc / L  # Current change (from inductor)
    return [dVc_dt, dI_dt]

# Initial conditions
Vc0 = V0  # Initial voltage across capacitor
I0 = 0    # Initial current in the circuit
X0 = [Vc0, I0]  # Initial state vector

# Time vector (0 to 0.05 second, 1000 points)
t = np.linspace(0, 0.05, 1000)

# Solve the differential equation
solution = odeint(lc_circuit, X0, t, args=(L, C))

# Extract the capacitor voltage and current
Vc = solution[:, 0]
I = solution[:, 1]

# Plot the results
plt.figure(figsize=(10, 5))

# Plot voltage across capacitor
plt.subplot(2, 1, 1)
plt.plot(t, Vc, 'b', label='Voltage across Capacitor (Vc)')
plt.title('LC Circuit Simulation')
plt.ylabel('Voltage (V)')
plt.grid(True)
plt.legend()

# Plot current through the circuit
plt.subplot(2, 1, 2)
plt.plot(t, I, 'r', label='Current (I)')
plt.xlabel('Time (s)')
plt.ylabel('Current (A)')
plt.grid(True)
plt.legend()

plt.tight_layout()
plt.show()
