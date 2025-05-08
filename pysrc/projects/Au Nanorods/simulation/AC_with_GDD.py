import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import LogNorm

c = 3e8  # m/s

# Pulse
central_wavelength = 800e-9  # m
pulse_duration = 7e-15  # s

# Satellite pulse
satellite_delay = 40e-15
satellite_amplitude = 0.5
satellite_duration = 8e-15
satellite_phase = np.pi/2

# GDD and Time delay
gdd_min = -200e-30
gdd_max = 200e-30
num_gdd_points = 100
delay_max = 60e-15
num_delay_points = 200

# Time grid
time_window = 300e-15
num_time_points = 2048
time = np.linspace(-time_window/2, time_window/2, num_time_points)
dt = time[1] - time[0]

# Frequency grid
freq = np.fft.fftshift(np.fft.fftfreq(num_time_points, dt))
omega = 2 * np.pi * freq
omega0 = 2 * np.pi * c / central_wavelength

# Delay and GDD arrays
delays = np.linspace(-delay_max, delay_max, num_delay_points)
gdd_values = np.linspace(gdd_min, gdd_max, num_gdd_points)

# Define transform-limited Gaussian pulse
def create_tl_pulse(t, tau):
    tau_std = tau / (2 * np.sqrt(np.log(2)))
    return np.exp(-t**2 / (2 * tau_std**2))

# Main and satellite pulses
E_main_t = create_tl_pulse(time, pulse_duration)
E_satellite_t = satellite_amplitude * create_tl_pulse(time - satellite_delay, satellite_duration) * np.exp(1j * satellite_phase)
E_combined_t = E_main_t + E_satellite_t

# Frequency domain representation
E_combined_f = np.fft.fftshift(np.fft.fft(E_combined_t))

# Apply GDD
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

        # True fringe-resolved autocorrelation: simulate SHG output
        Et_sum = Et_chirped + Et_delayed
        SHG_signal = np.abs(Et_sum)**2
        SHG_output = np.abs(SHG_signal)**2
        frac_map[i, j] = np.sum(SHG_output)

# Normalize each trace to remove global intensity variation (GDD energy loss)
frac_map /= np.max(frac_map, axis=1, keepdims=True)

# Plot FRAC map
plt.figure(figsize=(12, 8))
plt.pcolormesh(delays * 1e15, gdd_values * 1e30, frac_map, 
               cmap='inferno', vmin=0, vmax=1)
plt.colorbar(label='Normalized FRAC (per GDD)')
plt.xlabel('Delay (fs)')
plt.ylabel('GDD (fs²)')
plt.title('FRAC Map (GDD-normalized)')
plt.grid(True, linestyle='--', alpha=0.6)
plt.tight_layout()
plt.show()

# Plot selected traces
plt.figure(figsize=(10, 8))
for gdd in [-200, -100, 0, 100, 200]:
    idx = np.argmin(np.abs(gdd_values * 1e30 - gdd))
    plt.plot(delays * 1e15, frac_map[idx], label=f'GDD = {gdd} fs²')

plt.xlabel('Delay (fs)')
plt.ylabel('Normalized FRAC')
plt.title('Selected GDD-normalized FRAC Traces')
plt.grid(True)
plt.legend()
plt.xlim(-60, 60)
plt.tight_layout()
plt.show()
