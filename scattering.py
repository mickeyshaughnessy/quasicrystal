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
prime_numbers_a = np.array(list(primerange(1, num_primes_1da + 1)))
prime_numbers_b = np.array(list(primerange(1, num_primes_1db + 1)))
prime_lattice_a = np.array([math.log(x) for x in prime_numbers_a])
prime_lattice_b = np.array([math.log(x) for x in prime_numbers_b])

scattering_amplitude_1d_a = []
scattering_amplitude_1d_b = []
momentum_1d = [] 

zeta_zeros = []
for n in range(1, num_zeros + 1):
    zeta_zeros.append(zetazero(n).imag)
    if n % 15 == 0:
        print(f"Calculating Riemann Zeta Function zeros: {n}/{num_zeros}...")

for wave_number in range(1, wave_number_max+1):
    wave_vector = 2 * np.pi * wave_number * dk_1d
    sum_cosine_a, sum_sine_a, sum_magnitude_a = 0, 0, 0
    sum_cosine_b, sum_sine_b, sum_magnitude_b = 0, 0, 0

    if wave_number % 3 == 0:
        print(f"Calculating scattering amplitude (1D): {wave_number}/{wave_number_max}...")

    momentum_1d.append(wave_vector)
    for i, prime in enumerate(prime_lattice_a):
        phase = wave_vector * prime
        sum_cosine_a += np.cos(phase)
        sum_sine_a += np.sin(phase)
        sum_cosine_squared_a = sum_cosine_a ** 2
        sum_sine_squared_a = sum_sine_a ** 2
        sum_cosine_sine_a = sum_cosine_squared_a + sum_sine_squared_a
        sum_magnitude_a += np.sqrt(sum_cosine_sine_a)

    scattering_amplitude_1d_a.append(sum_magnitude_a)
    
    for i, prime in enumerate(prime_lattice_b):
        phase = wave_vector * prime
        sum_cosine_b += np.cos(phase)
        sum_sine_b += np.sin(phase)
        sum_cosine_squared_b = sum_cosine_b ** 2
        sum_sine_squared_b = sum_sine_b ** 2
        sum_cosine_sine_b = sum_cosine_squared_b + sum_sine_squared_b
        sum_magnitude_b += np.sqrt(sum_cosine_sine_b)

    scattering_amplitude_1d_b.append(sum_magnitude_b)

k_min_1d = 0
k_max_1d = max(momentum_1d) 
fig, ax1 = plt.subplots(figsize=(10, 8))  # Set figure size

# Plot the first amplitude on the left y-axis
ax1.scatter(momentum_1d, scattering_amplitude_1d_a, s=10, c='b', label='Scattering amplitude $L_{{\chi}}$ = {}'.format(num_primes_1da))
for i, zero in enumerate(zeta_zeros):
    if i == 0:
        ax1.scatter(zero, 0, color='r', marker='x', label='RZF zeros')
        ax1.axvline(x=zero, color='r', linestyle='--', linewidth=0.5)
    else:
        ax1.scatter(zero, 0, color='r', marker='x')
        ax1.axvline(x=zero, color='r', linestyle='--', linewidth=0.5)
ax1.set_xlabel('Momentum (k in units of 2*pi/a)', fontsize=14)  # Larger font size
ax1.set_ylabel('Scattering Amplitude A', fontsize=14)  # Larger font size for the first amplitude
ax1.set_title('Scattering Amplitude vs Momentum (1D)', fontsize=16)  # Larger font size
ax1.grid(False)  # Turn off the grid
ax1.set_xlim(k_min_1d, k_max_1d)
ax1.set_ylim(0, 0.05*np.max(scattering_amplitude_1d_a))
ax1.legend(fontsize=12, loc='upper right')  # Larger font size and custom location

# Create a twin Axes for the second amplitude on the right y-axis
ax2 = ax1.twinx()
ax2.scatter(momentum_1d, scattering_amplitude_1d_b, s=10, c='g', label='Scattering amplitude $L_{{\chi}}$ = {}'.format(num_primes_1db))
ax2.set_ylabel('Scattering Amplitude B', fontsize=14)  # Larger font size for the second amplitude
ax2.set_ylim(0, 0.05*np.max(scattering_amplitude_1d_b))

plt.show()

