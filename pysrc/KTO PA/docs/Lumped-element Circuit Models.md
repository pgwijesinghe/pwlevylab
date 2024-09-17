## Modelling a simple RLC Circuit

Before modeling the Parametric amplifier, I want to do a test simulation on a conventional RLC circuit, to brush up my memory.


## Parametric Amplifier 

In here, I will be solving the circuits classically using equations of motion by modelling the circuit as a lumped-element model. 

This circuit will mainly consist of transmission lines, capacitors and inductors and the idea is to write down the governing equations for the model using Kirchhoff's laws. 

Starting with a transmission line, considering the input-output conditions;
$$
\begin{align}
I_{net} &=& I_{in}-I_{out} \\
V_{net} &=& V_{in} + V_{out} \\
\end{align}
$$
Considering a superconducting circuit, we can write the phase difference across an inductor loop as follows:
$$
\begin{align}
\phi = \frac{2\pi}{\Phi_0} \Phi
\end{align}
$$
where $\Phi$ is the magnetic flux across the inductor and $\Phi_0$ is the flux quantum $\frac{h}{2e}$.

By using Josephson voltage-phase relationship [ref](https://en.wikipedia.org/wiki/Josephson_effect), we have;

$$
\begin{align}
V(t) = \frac{\hbar}{2e} \frac{d\phi}{dt}  \\
\implies \dot{\phi}_{net} = \dot{\phi}_{in} + \dot{\phi}_{out}
\end{align}
$$
This is very similar to Faraday's law of induction. But  this voltage does not come from magnetic energy, since there is no magnetic field in the superconductors; Instead, this voltage comes from the kinetic energy of the carriers (i.e. the Cooper pairs). This phenomenon is also known as kinetic inductance.

Now we'll move on to circuit modeling.
### Base Circuit

![[./assets/Pasted image 20240910152138.png]]


This is the circuit proposed in the DARPA report where parametric amplification is realized by varying the Kinetic inductance.

If we write equations of motion for this circuit,

Considering the node at $\phi(t)$, by applying KCL, we get;
$$
\begin{align}
I_{net} = C\ddot{\phi}_{net}(t) + \frac{\phi_{net}(t)}{L(t)} = \frac{V_{in}}{Z}-\frac{V_{out}}{Z}\\
C\ddot{\phi}_{net}(t) + \frac{\phi_{net}(t)}{L(t)} = \frac{\dot{\phi}_{in}(t)}{Z} - \frac{(\dot{\phi}_{net}(t) - \dot{\phi}_{in}(t))}{Z} \\
C\ddot{\phi}_{net}(t) + \frac{\dot{\phi}_{net}(t)}{Z} + \frac{\phi_{net}(t)}{L(t)} = 2\frac{\dot{\phi}_{in}}{Z} \\
\ddot{\phi}_{net}(t) + \frac{\dot{\phi}_{net}(t)}{CZ} + \frac{\phi_{net}(t)}{CL(t)} = 2\frac{\dot{\phi}_{in}}{CZ}
\end{align}
$$

Here;
- $\phi_{net}(t)$ is the superconducting phase difference across the inductor. 
- $Z$ is the transmission line impedance, 
- $C$ is the capacitance, 
- $L(t) = L_{0} + L_{P}sin(2\omega t)$ is the time dependent inductance,
- $\phi_{in}(t)$ is the incoming signal tone.

Assuming the resonance condition, $\omega = \frac{1}{\sqrt{L_0 C}}$ and let $K=\frac{1}{CZ}$.
Let's also impose the following assumptions on the system;
1. Fluctuations of the kinetic inductance are much smaller than the inherent kinetic inductance $L_{P} << L_{0}$.
2. Rotating Wave Approximation (RWA).

Using assumption 1, upon Taylor expansion, we get;
$$
\frac{1}{L(t)}=\frac{1}{L_0+L_Psin(2\omega t)}=\frac{1}{L_0}(1-\frac{L_p}{L_0}sin(2\omega t))
$$
Now rewriting the equation of motion in terms of $\omega$ and $K$, we get;
$$
\ddot{\phi}_{net}(t) + K\dot{\phi}_{net}(t) + \omega^2[1-\frac{L_P}{L_0}sin(2\omega t)]\phi_{net}(t) = 2K\dot{\phi}_{in}
$$
Let $\phi_{in} = A_{in}sin(\omega t) \implies \dot{\phi}_{in} = A_{in}\omega cos(\omega t)$.
Letting $\phi_{out} = A_{out}sin(\omega t)$, we get;

$$
\begin{align}
\phi_{net} = \phi_{in} + \phi_{out} = (A_{in}+A_{out})sin(\omega t) \\
\implies \dot{\phi}_{net} = (A_{in}+A_{out})\omega cos(\omega t) \\
\implies \ddot{\phi}_{net} = -(A_{in}+A_{out})\omega^2 sin(\omega t)
\end{align}
$$

$$
\begin{align}
-(A_{in}+A_{out})\omega^2 sin(\omega t) + K\omega(A_{in}+A_{out})cos(\omega t) + \omega^2(A_{in}+A_{out})sin(\omega t) \\ 
- \omega^2\frac{L_P}{L_0}(A_{in}+A_{out})sin(2\omega t)sin(\omega t) = 2K\omega A_{in}cos(\omega t) \\
\end{align}
$$
$$
\begin{align}
sin(2\omega t)sin(\omega t) = \frac{1}{2}(cos(\omega t) - cos(3\omega t))
\end{align}
$$
Using assumption 2 (RWA), we can neglect the $3\omega$ oscillating term which upon substituting and simplifying leads to;
$$
\begin{align}
K\omega(A_{in}+A_{out})cos(\omega t) - \omega^2\frac{L_P}{2L_0}(A_{in}+A_{out})cos(\omega t) &= 2K\omega A_{in}cos(\omega t) \\
\implies A_{in}[-\frac{K}{\omega} + \frac{L_P}{2L_0} + \frac{2K}{\omega}] &= A_{out}[\frac{K}{\omega} - \frac{L_P}{2L_0}] \\
\implies G = \frac{A_{out}^2}{A_{in}^2} &\approx\frac{(\frac{2K}{\omega}+\frac{L_P}{L_0})^2}{(\frac{2K}{\omega}-\frac{L_P}{L_0})^2}
\end{align}

$$
## Initial Simulation Results

## FFT


### Intermediate Circuit

![[Pasted image 20240910141102.png]]

Let $L_1 = L_2 = L$

Considering the junction at $\phi_2$, and applying Kirchhoff's current law we get;
$$
\begin{equation}
C_S(\ddot{\phi_2}-\ddot{\phi_1}) + C_D(\ddot{\phi_2}) + \frac{(\phi_2 - \phi_3)}{L}=0
\end{equation}
$$

Considering the junction at $\phi_3$, and applying Kirchhoff's current law we get;
$$
\begin{equation}
C_P(\ddot{\phi_3}-\ddot{\phi_4}) + \frac{\phi_3}{L} + \frac{(\phi_2 - \phi_3)}{L}=0
\end{equation}
$$


