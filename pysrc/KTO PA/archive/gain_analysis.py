import numpy as np
import matplotlib.pyplot as plt

# Gain calculation based on the formula
def gain(K, omega, Lp, L):
    numerator = (2 * K / omega + Lp / L)**2
    denominator = (2 * K / omega - Lp / L)**2
    return numerator / denominator

# Define constants (rough values from literature for superconducting circuits)
C = 1e-12  # Capacitance, in Farads
L0 = 1e-9  # Base inductance, in Henrys
Lp = 0.2e-9  # Modulated inductance, in Henrys
Z = 50  # Impedance, in Ohms
omega = 2 * np.pi * 5e9  # Signal frequency, 5 GHz
K = 0.1  # Some constant related to the system, arbitrary for now

# Average inductance (for simplicity, using base inductance L0)
L_avg = L0

# Define a range of values for Lp, omega, and K for analysis
Lp_values = np.linspace(0.1e-9, 1e-9, 100)  # Modulated inductance from 0.1nH to 1nH
omega_values = np.linspace(2 * np.pi * 1e9, 2 * np.pi * 10e9, 100)  # Frequency range from 1GHz to 10GHz
K_values = np.linspace(0.01, 0.5, 100)  # K values from 0.01 to 0.5

# Calculate gain for different Lp, omega, and K, while keeping other parameters fixed
gain_Lp = [gain(K, omega, Lp, L_avg) for Lp in Lp_values]
gain_omega = [gain(K, omega_val, Lp, L_avg) for omega_val in omega_values]
gain_K = [gain(K_val, omega, Lp, L_avg) for K_val in K_values]

# Plotting the results
fig, ax = plt.subplots(3, 1, figsize=(8, 12))

# Plot gain vs Lp
ax[0].plot(Lp_values * 1e9, gain_Lp, label=r'Gain vs $L_p$')
ax[0].set_xlabel(r'$L_p$ (nH)')
ax[0].set_ylabel('Gain')
ax[0].set_title('Gain vs Inductance Modulation $L_p$')
ax[0].grid(True)

# Plot gain vs omega
ax[1].plot(omega_values / (2 * np.pi * 1e9), gain_omega, label=r'Gain vs $\omega$')
ax[1].set_xlabel(r'$\omega$ (GHz)')
ax[1].set_ylabel('Gain')
ax[1].set_title('Gain vs Signal Frequency $\omega$')
ax[1].grid(True)

# Plot gain vs K
ax[2].plot(K_values, gain_K, label=r'Gain vs $K$')
ax[2].set_xlabel(r'$K$')
ax[2].set_ylabel('Gain')
ax[2].set_title('Gain vs Constant $K$')
ax[2].grid(True)

plt.tight_layout()
plt.show()
