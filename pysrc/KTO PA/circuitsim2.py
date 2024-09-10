import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import odeint

# Define parameters
L1 = 10e-6  # 10 µH
L2 = 10e-6  # 10 µH
Cs = 10e-12  # 10 pF
Cp = 10e-12  # 10 pF
Cd0 = 10e-12  # 10 pF
Cd_amp = 1e-12  # Amplitude of parametric modulation (1 pF variation)
omega = 1e9  # Angular frequency of the signal (1 GHz)
A_s = 1  # Amplitude of input signal
A_p = 1  # Amplitude of pump signal
phi = 0  # Phase of the input signal

# Time array
t = np.linspace(0, 1e-7, 10000)  # Simulating for 100 ns

# Input and pump signals
V_in = A_s * np.sin(omega * t + phi)
V_pump = A_p * np.sin(2 * omega * t)

# Time-varying capacitance (parametric modulation)
def Cd(t):
    return Cd0 + Cd_amp * np.sin(omega * t)

# Define system of differential equations for the currents through L1 and L2
def parametric_amplifier(currents, t, L1, L2, Cs, Cp):
    I1, I2 = currents
    
    # dI1/dt and dI2/dt from the LC circuit equations
    dI1_dt = (V_in[int(t*10000000)] - (1/Cs)*I1) / L1
    dI2_dt = (V_pump[int(t*10000000)] - (1/Cp)*I2) / L2
    return [dI1_dt, dI2_dt]

# Initial conditions for I1, I2
I0 = [0, 0]

# Solve the differential equations
currents = odeint(parametric_amplifier, I0, t, args=(L1, L2, Cs, Cp))

# Extract I1 (signal current) and I2 (pump current)
I1, I2 = currents[:, 0], currents[:, 1]

# Plot the results
plt.figure(figsize=(10, 6))
plt.plot(t, I1, label='Current through L1 (Signal Circuit)')
plt.plot(t, I2, label='Current through L2 (Pump Circuit)', linestyle='dashed')
plt.xlabel('Time (s)')
plt.ylabel('Current (A)')
plt.title('Parametric Amplifier Simulation')
plt.legend()
plt.grid(True)
plt.show()
