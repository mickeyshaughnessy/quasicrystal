import numpy as np
import matplotlib.pyplot as plt
from sympy import primerange
from mpmath import zetazero
import math

# Parameterization
num_primes_1da = 800000
num_primes_1db = 8000000
num_zeros = 300
dk_1d = 0.01  # Grid resolution in k-space for 1D plot
k_min_1d = 0
k_max_1d = 500
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


plt.scatter(momentum_1d, scattering_amplitude_1d_a, s=1, c='b')
plt.scatter(momentum_1d, scattering_amplitude_1d_b, s=1, c='g')
for zero in zeta_zeros:
    plt.scatter(zero, 0, color='r', marker='x')
    plt.axvline(x=zero, color='r', linestyle='--', linewidth=0.5)
plt.xlabel('Momentum (k in units of 2*pi/a)')
plt.ylabel('Scattering Amplitude')
plt.title('Scattering Amplitude vs Momentum (1D)')
plt.grid(True)
plt.xlim(k_min_1d, k_max_1d)
plt.ylim(0, np.max(scattering_amplitude_1d))
plt.show()
