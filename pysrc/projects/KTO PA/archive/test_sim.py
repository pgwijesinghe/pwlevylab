import numpy as np
from qutip import *
from qutip import QobjEvo

# Define parameters for the LC circuit
C = 1e-12  # Capacitance in Farads
L0 = 1e-9  # Base inductance in Henries
Lp = 1e-10  # Modulation amplitude for inductance
omega = 2 * np.pi * 1e9  # Driving frequency in rad/s (1 GHz)
hbar = 1.0545718e-34  # Reduced Planck constant

# Define the number of energy levels to consider
N = 10  # Number of basis states (truncation)

# Time-dependent inductance
def L_t(t):
    return L0 + Lp * np.sin(2 * omega * t)

# Hamiltonian components
a = destroy(N)  # Annihilation operator
phi_operator = a + a.dag()  # Flux operator (position-like)
q_operator = 1j * (a - a.dag())  # Charge operator (momentum-like)

# Define the time-dependent Hamiltonian
def H_t(t, args):
    L_t_val = L_t(t)
    return (q_operator**2) / (2 * C) + (phi_operator**2) / (2 * L_t_val)

# Convert the time-dependent Hamiltonian to a QobjEvo (time-evolution operator)
H = QobjEvo(H_t, tlist=np.linspace(0, 10e-9, 1000))  # Time array

# Initial state (ground state)
psi0 = basis(N, 0)  # Ground state

# Time array for evolution
tlist = np.linspace(0, 10e-9, 1000)  # Evolve for 10 ns

# Run the simulation
result = mesolve(H, psi0, tlist, [], [a.dag() * a])

# Plot the expectation value of the number operator (photon number)
import matplotlib.pyplot as plt

plt.figure()
plt.plot(tlist, result.expect[0])
plt.xlabel('Time (s)')
plt.ylabel('Photon number')
plt.title('Time evolution in a parametrically driven quantum LC circuit')
plt.show()
