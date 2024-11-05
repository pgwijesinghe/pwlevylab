import numpy as np
from scipy.integrate import odeint
import matplotlib.pyplot as plt

# Define parameters
C = 1/50    # Capacitance
Z = 500   # Impedance
L_0 = 50    # Base inductance
L_p = 1   # Amplitude of inductance oscillation
omega = 1.0 # Frequency for the sinusoidal functions

# Define phi_in(t) as the integral of phi_in_dot(t)
def phi_in(t):
    return -1 / omega * np.cos(omega * t + np.pi/2)

# Define phi_in_dot(t) as a function of time
def phi_in_dot(t):
    return 1 * np.sin(omega * t + np.pi/2)

# Define L(t) as a function of time
def L(t):
    return L_0 + L_p * np.sin(2 * omega * t)

# Define the system of ODEs
def circuit_equations(y, t):
    phi_net, phi_net_dot = y
    phi_net_ddot = - (phi_net_dot / (C * Z)) - (phi_net / (C * L(t))) + (2 * phi_in_dot(t) / (C * Z))
    
    return [phi_net_dot, phi_net_ddot]

def calc_thoretical_gain(C=C, Z=Z, L_0=L_0, L_p=L_p, omega=omega):
    K = 1/(C*Z)
    gain = (((2*K/omega) + L_p/L_0)/((2*K/omega) - L_p/L_0))**2
    return gain

print(calc_thoretical_gain())

# Initial conditions for [phi_net(0), phi_net_dot(0)]
y0 = [0.0, 0.0]

# Time Array
t = np.linspace(0, 400, 10000)

# Solve the ODE system
solution = odeint(circuit_equations, y0, t)

# Extract the solutions for phi_net(t) and phi_net_dot(t)
phi_net = solution[:, 0]
phi_net_dot = solution[:, 1]

# Calculate phi_in(t)
phi_in_vals = phi_in(t)

# Calculate phi_out(t) as phi_out = phi_in - phi_net
phi_out_vals = phi_in_vals - phi_net

t_points = 1000
idx = []
phi_new = []
phi_in_new = []
for i in range(t_points):
    per = 4*np.pi
    step = per/t_points
    inc = 350 + i*step
    idx.append(int((np.abs(t - inc)).argmin()))
    phi_new.append(phi_out_vals[idx[i]])
    phi_in_new.append(phi_in_vals[idx[i]])

print(idx)
plt.figure()
plt.plot(phi_new)
plt.plot(phi_in_new)
plt.show()
# Plot the results for phi_out
plt.figure(figsize=(10, 6))
plt.plot(phi_new, label="phi_out(t)", color="green")
plt.xlabel('Time [s]')
plt.ylabel('Values')
plt.title('phi_out(t) vs Time')
plt.legend()
plt.grid(True)
plt.show()

# Fourier Transform of phi_out
phi_out_fft = np.fft.fft(phi_new)
phi_in_fft = np.fft.fft(phi_in_new)

# Frequencies corresponding to the FFT components (in Hz)
frequencies = np.fft.fftfreq(t_points, 4*np.pi/t_points)

# Convert frequencies from cycles per second (Hz) to angular frequencies (rad/s)
frequencies_hz = frequencies * 2 * np.pi

# Power spectrum (magnitude of the Fourier transform)
power_spectrum = np.abs(phi_out_fft)**2

# Plot the power spectrum (only positive frequencies)
plt.figure(figsize=(10, 6))
plt.plot(frequencies_hz[:len(frequencies)//2], power_spectrum[:len(frequencies)//2], color='purple')
plt.plot(frequencies_hz[:len(frequencies)//2], np.abs(phi_in_fft[:len(frequencies)//2])**2, color='orange')
plt.xlabel('Frequency [Hz]')
plt.ylabel('Power (log scale)')
plt.title('Power Spectrum of phi_out(t)')
plt.grid(True)
plt.show()