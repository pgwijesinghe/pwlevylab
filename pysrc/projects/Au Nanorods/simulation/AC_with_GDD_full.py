import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import LogNorm

# Constants
c = 3e8  # Speed of light (m/s)

# Main pulse parameters
central_wavelength = 800e-9  # meters
pulse_duration = 7e-15  # seconds

# Satellite pulse parameters
satellite_delay = 40e-15
satellite_amplitude = 1
satellite_duration = 8e-15
satellite_phase = np.pi / 2

# GDD and delay scan
gdd_min = -200e-30
gdd_max = 200e-30
num_gdd_points = 100
delay_max = 60e-15
num_delay_points = 200

# Time grid
time_window = 300e-15
num_time_points = 2048
time = np.linspace(-time_window / 2, time_window / 2, num_time_points)
dt = time[1] - time[0]

# Frequency grid
freq = np.fft.fftshift(np.fft.fftfreq(num_time_points, dt))
omega = 2 * np.pi * freq
omega0 = 2 * np.pi * c / central_wavelength

# Delay and GDD arrays
delays = np.linspace(-delay_max, delay_max, num_delay_points)
gdd_values = np.linspace(gdd_min, gdd_max, num_gdd_points)

# Create transform-limited Gaussian pulse
def create_tl_pulse(t, tau):
    tau_std = tau / (2 * np.sqrt(np.log(2)))
    return np.exp(-t**2 / (2 * tau_std**2))

# Main and satellite pulses (envelopes only)
E_main_env = create_tl_pulse(time, pulse_duration)
E_sat_env = satellite_amplitude * create_tl_pulse(time - satellite_delay, satellite_duration) * np.exp(1j * satellite_phase)

# Carrier wave for oscillation
carrier = np.exp(1j * omega0 * time)

# Full field with oscillating carrier
E_combined_t = (E_main_env + E_sat_env) * carrier

# FFT to frequency domain
E_combined_f = np.fft.fftshift(np.fft.fft(E_combined_t))

# Plot: Electric Field (oscillating), Intensity, Spectrum
intensity_time = np.abs(E_combined_t)**2
intensity_freq = np.abs(E_combined_f)**2

# Convert angular frequency to wavelength for plotting
wavelengths = 2 * np.pi * c / omega
wavelengths_nm = wavelengths * 1e9
valid = (wavelengths_nm > 600) & (wavelengths_nm < 1000)

fig, axs = plt.subplots(3, 1, figsize=(10, 10))

# Real part of oscillating E-field
axs[0].plot(time * 1e15, np.real(E_combined_t), color='blue')
axs[0].set_title('Electric Field with Carrier: Real(E(t))')
axs[0].set_xlabel('Time (fs)')
axs[0].set_ylabel('Amplitude')
axs[0].grid(True)

# Temporal Intensity
axs[1].plot(time * 1e15, intensity_time, color='darkgreen')
axs[1].set_title('Temporal Intensity |E(t)|²')
axs[1].set_xlabel('Time (fs)')
axs[1].set_ylabel('Intensity (a.u.)')
axs[1].grid(True)

# Spectrum
axs[2].plot(wavelengths_nm[valid], intensity_freq[valid], color='crimson')
axs[2].set_title('Spectrum |E(ω)|²')
axs[2].set_xlabel('Wavelength (nm)')
axs[2].set_ylabel('Spectral Intensity (a.u.)')
axs[2].invert_xaxis()
axs[2].grid(True)

plt.tight_layout()
plt.show()

# Apply GDD in frequency domain
def apply_gdd(Ef, gdd):
    phase = 0.5 * gdd * (omega - omega0)**2
    return Ef * np.exp(1j * phase)

# Allocate FRAC map
frac_map = np.zeros((num_gdd_points, num_delay_points))

# Loop over GDDs
for i, gdd in enumerate(gdd_values):
    Ef_chirped = apply_gdd(E_combined_f, gdd)
    Et_chirped = np.fft.ifft(np.fft.ifftshift(Ef_chirped))

    for j, delay in enumerate(delays):
        delay_idx = int(round(delay / dt))
        Et_delayed = np.roll(Et_chirped, delay_idx)

        Et_sum = Et_chirped + Et_delayed
        SHG_signal = np.abs(Et_sum)**2
        SHG_output = np.abs(SHG_signal)**2
        frac_map[i, j] = np.sum(SHG_output)

# Normalize each GDD row
frac_map /= np.max(frac_map, axis=1, keepdims=True)

# # Plot FRAC map
# plt.figure(figsize=(12, 8))
# plt.pcolormesh(delays * 1e15, gdd_values * 1e30, frac_map,
#                cmap='inferno', vmin=0, vmax=1)
# plt.colorbar(label='Normalized FRAC (per GDD)')
# plt.xlabel('Delay (fs)')
# plt.ylabel('GDD (fs²)')
# plt.title('FRAC Map (GDD-normalized)')
# plt.grid(True, linestyle='--', alpha=0.6)
# plt.tight_layout()
# plt.show()

# # Plot selected GDD traces
# plt.figure(figsize=(10, 8))
# for gdd in [-200, -100, 0, 100, 200]:
#     idx = np.argmin(np.abs(gdd_values * 1e30 - gdd))
#     plt.plot(delays * 1e15, frac_map[idx], label=f'GDD = {gdd} fs²')

# plt.xlabel('Delay (fs)')
# plt.ylabel('Normalized FRAC')
# plt.title('Selected GDD-normalized FRAC Traces')
# plt.grid(True)
# plt.legend()
# plt.xlim(-60, 60)
# plt.tight_layout()
# plt.show()
