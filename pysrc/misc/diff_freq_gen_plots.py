import numpy as np
import matplotlib.pyplot as plt

# catch the two wavelengths (in nm)
# wl1, wl2 = int(input("WL1 (nm):\n")), int(input("WL2 (nm):\n"))
wl1, wl2 = 757,797  # spatial modulation by the SLM

#  convert into frequency (in Hz)
f1, f2 = 3e17*(1/wl1), 3e17*(1/wl2)

print(f"Difference frequency is {abs(f1-f2)*1e-12} GHz")

def E_field(A1,A2,f1,f2,t):
    return A1*np.cos(2*np.pi*f1*t) + A2*np.cos(2*np.pi*f2*t)

plt.figure(1)
t = np.linspace(-500e-15, 500e-15, 10000)
tt = 3000e-15
E_in = E_field(1,1,f1,f2,t)
E_trans = (1/np.sqrt(2))*E_field(1,1,f1,f2,t)
E_refl = (1/np.sqrt(2))*E_field(1,1,f1,f2,(t-tt))
E_opt = E_trans + E_refl
plt.plot(t,E_in,t,E_trans,t,E_refl,t,E_opt)
plt.title(f"Time domain E field")
plt.xlabel("time (fs)")
plt.ylabel("Amplitude")

plt.figure(2)
a = -4.33e-5
b = 0.018
c = 1.10
d = 0.154
w1 = 2*np.pi*f1
w2 = 2*np.pi*f2
tp = 7e-15
wc = 2*np.pi*362e12
dv = a*(np.cos(w1*t) + np.cos(w2*t) + b*(np.cos(2*w1*t) + np.cos(2*w2*t) + 4*(np.cos((w1-w2)*t) + np.cos((w1+w2)*t))) + np.cos(wc*t)*(c*np.exp(-0.5*(t/tp)**2) + 4*d*np.exp(-0.75*(t/tp)**2)) + d*np.exp(-(t/tp)**2)*(2+2*np.cos(2*wc*t)))
plt.plot(t,dv)

plt.show()
