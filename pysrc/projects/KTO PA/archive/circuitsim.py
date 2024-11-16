import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import solve_ivp

# Define constants (rough values for inductors, capacitors, and driving forces)
L1 = 1e-9  # Inductor L1, in Henrys
L2 = 1e-9  # Inductor L2, in Henrys
Cs = 1e-12  # Capacitance Cs, in Farads
Cd = 1e-12  # Capacitance Cd, in Farads
Cp = 1e-12  # Capacitance Cp, in Farads
As = 1e-3  # Amplitude of signal, in Volts
Ap = 1e-3  # Amplitude of pump, in Volts
omega = 2 * np.pi * 5e9  # Signal frequency (5 GHz)

# Define the signal and pump drives
def V_s(t):
    return As * np.sin(omega * t)

def V_p(t)->float:
    return Ap * np.sin(2 * omega * t)

# Define the system of differential equations
def circuit_eqs(t, y):
    I_L1, I_L2, V_Cs, V_Cd = y  # Current through L1, L2 and voltages across Cs, Cd

    dI_L1 = (V_s(t) - V_Cs) / L1  # dI_L1/dt = (V_s - V_Cs) / L1
    dI_L2 = (V_Cd - V_p(t)) / L2  # dI_L2/dt = (V_Cd - V_p) / L2
    dV_Cs = I_L1 / Cs             # dV_Cs/dt = I_L1 / Cs
    dV_Cd = (I_L1 - I_L2) / Cd    # dV_Cd/dt = (I_L1 - I_L2) / Cd
    
    return [dI_L1, dI_L2, dV_Cs, dV_Cd]

# Initial conditions: Zero current and zero voltage
y0 = [0, 0, 0, 0]

# Time range for simulation
t_span = [0, 10e-9]  # Simulate for 10 ns
t_eval = np.linspace(t_span[0], t_span[1], 1000)

# Solve the system of differential equations
solution = solve_ivp(circuit_eqs, t_span, y0, t_eval=t_eval)

# Extract time and solution values
t = solution.t
I_L1, I_L2, V_Cs, V_Cd = solution.y

# Plot the results
plt.figure(figsize=(10, 8))

# Plot current through L1
plt.subplot(2, 2, 1)
plt.plot(t * 1e9, I_L1)
plt.xlabel("Time (ns)")
plt.ylabel("Current through L1 (A)")
plt.title("Current through Inductor L1")
plt.grid(True)

# Plot current through L2
plt.subplot(2, 2, 2)
plt.plot(t * 1e9, I_L2)
plt.xlabel("Time (ns)")
plt.ylabel("Current through L2 (A)")
plt.title("Current through Inductor L2")
plt.grid(True)

# Plot voltage across Cs
plt.subplot(2, 2, 3)
plt.plot(t * 1e9, V_Cs)
plt.xlabel("Time (ns)")
plt.ylabel("Voltage across Cs (V)")
plt.title("Voltage across Capacitor Cs")
plt.grid(True)

# Plot voltage across Cd
plt.subplot(2, 2, 4)
plt.plot(t * 1e9, V_Cd)
plt.xlabel("Time (ns)")
plt.ylabel("Voltage across Cd (V)")
plt.title("Voltage across Capacitor Cd")
plt.grid(True)

plt.tight_layout()
plt.show()
