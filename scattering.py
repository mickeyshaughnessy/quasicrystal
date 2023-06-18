import numpy as np
import matplotlib.pyplot as plt
from sympy import primerange
from mpmath import zetazero
import math

# Parameterization
num_primes_1da = 80000
num_primes_1db = 800000
num_zeros = 200
dk_1d = 0.01  # Grid resolution in k-space for 1D plot
wave_number_max = 1000

# 1D Calculation and Plotting
prime_lattice_a = np.log(np.array(list(primerange(1, num_primes_1da + 1))))
prime_lattice_b = np.log(np.array(list(primerange(1, num_primes_1db + 1))))
scattering_amplitude_1d_a = np.zeros(wave_number_max)
scattering_amplitude_1d_b = np.zeros(wave_number_max)
momentum_1d = 2 * np.pi * dk_1d * np.arange(1, wave_number_max+1)

zeta_zeros = [zetazero(n).imag for n in range(1, num_zeros + 1)]

for idx, wave_vector in enumerate(momentum_1d, start=1):
    if idx % 3 == 0:
        print(f"Calculating scattering amplitude (1D): {idx}/{wave_number_max}...")

    phases_a = wave_vector * prime_lattice_a
    phases_b = wave_vector * prime_lattice_b

    scattering_amplitude_1d_a[idx-1] = np.sqrt((np.cos(phases_a).sum()**2 + np.sin(phases_a).sum()**2))
    scattering_amplitude_1d_b[idx-1] = np.sqrt((np.cos(phases_b).sum()**2 + np.sin(phases_b).sum()**2))

# Plotting
plt.figure(figsize=(10, 8))  # Set figure size
plt.scatter(momentum_1d, scattering_amplitude_1d_a, s=10, c='b', label=f'Scattering amplitude $L_{{\chi}}$ = {num_primes_1da}')
plt.scatter(momentum_1d, scattering_amplitude_1d_b, s=10, c='g', label=f'Scattering amplitude $L_{{\chi}}$ = {num_primes_1db}')
plt.scatter(zeta_zeros, [0]*len(zeta_zeros), color='r', marker='x', label='Zeta zeros')
for zero in zeta_zeros:
    plt.axvline(x=zero, color='r', linestyle='--', linewidth=0.5)

plt.xlabel('Momentum (k in units of 2*pi/a)', fontsize=14)  # Larger font size
plt.ylabel('Scattering Amplitude', fontsize=14)  # Larger font size
plt.title('Scattering Amplitude vs Momentum (1D)', fontsize=16)  # Larger font size
plt.grid(False)  # Turned off the grid
plt.xlim(0, max(momentum_1d))
plt.ylim(0, 0.05*max(scattering_amplitude_1d_b))
plt.legend(fontsize=12, loc='upper right')  # Larger font size and custom location
plt.show()

