import numpy as np
from scipy.integrate import odeint
import matplotlib.pyplot as plt

# Define parameters
C = 1/50      # Example value for capacitance
Z = 50     # Example value for impedance
L_0 = 50   # Base inductance
L_p = 0     # Amplitude of inductance oscillation
omega = 1.0  # Frequency for the sinusoidal functions

# Define L(t) as a function of time
def L(t):
    return L_0 + L_p * np.sin(2 * omega * t)

# Define phi_in_dot(t) as a function of time
def phi_in_dot(t):
    return 1 * np.sin(omega * t)

# Define the system of ODEs
def circuit_equations(y, t):
    phi_net = y[0]
    phi_net_dot = y[1]
    
    # Second-order equation based on the given formula
    phi_net_ddot = - (phi_net_dot / (C * Z)) - (phi_net / (C * L(t))) + (2 * phi_in_dot(t) / (C * Z))
    
    # Return the system of first-order ODEs
    return [phi_net_dot, phi_net_ddot]

# Initial conditions [phi_net(0), phi_net_dot(0)]
y0 = [0.0, 0.0]

# Time points at which to solve the ODE
t = np.linspace(0, 10, 1000)

# Solve the ODE system
solution = odeint(circuit_equations, y0, t)

# Extract the solutions for phi_net(t) and phi_net_dot(t)
phi_net = solution[:, 0]
phi_net_dot = solution[:, 1]

# Plot the results
plt.figure(figsize=(10, 6))
plt.plot(t, phi_net, label="phi_net(t)", color="blue")
plt.plot(t, phi_net_dot, label="phi_net_dot(t)", linestyle="--", color="red")
plt.xlabel('Time [s]')
plt.ylabel('Values')
plt.title('Simulation of Circuit Dynamics with Time-Varying Inductance and Input')
plt.legend()
plt.grid(True)
plt.show()
