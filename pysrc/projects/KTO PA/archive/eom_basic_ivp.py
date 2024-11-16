import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import solve_ivp

# Define constants (rough values from literature for superconducting circuits)
C = 1e-12  # Capacitance, in Farads
L0 = 1e-9  # Base inductance, in Henrys
Lp = 0.2e-9  # Modulated inductance, in Henrys
Z = 50  # Impedance, in Ohms
omega = 2 * np.pi * 5e9  # Signal frequency, 5 GHz
K = 0.1  # Some constant related to the system, arbitrary for now

# Time-dependent inductance
def L(t):
    return L0 + Lp * np.sin(2 * omega * t)

# Input signal (we assume a simple sinusoidal for now)
def phi_in(t):
    return np.sin(omega * t)

# Equation of motion
def dphi_dt(t, y):
    phi, dphi = y  # y contains [phi(t), dphi(t)/dt]
    
    # Define the differential equation based on the equation given
    d2phi = (2/Z * phi_in(t) - dphi/Z - phi/L(t)) / C
    return [dphi, d2phi]

# Initial conditions
phi0 = [0, 0]  # phi(0) = 0, dphi(0)/dt = 0

# Time range for simulation
t_span = [0, 10e-9]  # Simulate for 10 ns
t_eval = np.linspace(t_span[0], t_span[1], 1000)  # Time points for evaluation

# Solve the differential equation
solution = solve_ivp(dphi_dt, t_span, phi0, t_eval=t_eval)

# Extract results
t = solution.t
phi = solution.y[0]  # phi(t)

# Plot the results
plt.figure(figsize=(8, 6))
plt.plot(t * 1e9, phi)
plt.xlabel("Time (ns)")
plt.ylabel(r"$\phi(t)$ (Phase)")
plt.title(r"Phase $\phi(t)$ vs. Time")
plt.grid(True)
plt.show()
