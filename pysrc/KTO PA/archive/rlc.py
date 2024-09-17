import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import odeint

# RLC circuit parameters
R = 10       # Resistance in ohms
L = 0.05     # Inductance in henries
C = 0.001    # Capacitance in farads
V0 = 5       # Amplitude of the driving voltage in volts
f = 50       # Frequency of the driving voltage in hertz
omega = 2 * np.pi * f  # Angular frequency of the driving voltage

# Define the differential equations for the driven RLC circuit
def driven_rlc_circuit(X, t, R, L, C, V0, omega):
    Vc, I = X  # Vc is the capacitor voltage, I is the current
    Vin = V0 * np.sin(omega * t)  # Driving voltage (sinusoidal)
    dVc_dt = I / C  # Voltage across capacitor
    dI_dt = (Vin - R * I - Vc) / L  # Current change considering driving voltage
    return [dVc_dt, dI_dt]

# Initial conditions
Vc0 = 0  # Initial voltage across capacitor
I0 = 0   # Initial current in the circuit
X0 = [Vc0, I0]  # Initial state vector

# Time vector (0 to 0.1 second, 1000 points)
t = np.linspace(0, 0.1, 1000)

# Solve the differential equation
solution = odeint(driven_rlc_circuit, X0, t, args=(R, L, C, V0, omega))

# Extract the capacitor voltage and current
Vc = solution[:, 0]
I = solution[:, 1]
Vin = V0 * np.sin(omega * t)  # Driving voltage for comparison

# Plot the results
plt.figure(figsize=(10, 8))

# Plot driving voltage
plt.subplot(3, 1, 1)
plt.plot(t, Vin, 'g', label='Driving Voltage (Vin)')
plt.title('Driven RLC Circuit Simulation')
plt.ylabel('Voltage (V)')
plt.grid(True)
plt.legend()

# Plot voltage across capacitor
plt.subplot(3, 1, 2)
plt.plot(t, Vc, 'b', label='Voltage across Capacitor (Vc)')
plt.ylabel('Voltage (V)')
plt.grid(True)
plt.legend()

# Plot current through the circuit
plt.subplot(3, 1, 3)
plt.plot(t, I, 'r', label='Current (I)')
plt.xlabel('Time (s)')
plt.ylabel('Current (A)')
plt.grid(True)
plt.legend()

plt.tight_layout()
plt.show()
