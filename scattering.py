import numpy as np
import matplotlib.pyplot as plt
from sympy import primerange
from mpmath import zetazero, li
import math

# Parameters
num_primes = 80000
num_zeros = 100
dk = 0.01  # Grid resolution in k-space
k_min = 0
k_max = 100 

# Generating and shifting prime numbers
prime_numbers = np.array(list(primerange(1, num_primes + 1)))
prime_lattice = np.log(prime_numbers)

# Compute the density of the shifted lattice
density_prime_lattice = np.arange(len(prime_lattice)) / prime_lattice
density_prime_numbers = np.arange(len(prime_numbers)) / prime_numbers

# Plot the density
fig, ax1 = plt.subplots()
ax1.scatter(prime_numbers, density_prime_lattice, label='Prime Lattice')
ax1.set_xlabel('x')
ax1.set_ylabel('Density (Prime Lattice)')
ax1.set_title('Density of Prime Lattice and Prime Numbers')

# Create a second y-axis for the density of prime numbers
ax2 = ax1.twinx()
ax2.scatter(prime_numbers, density_prime_numbers, color='orange', label='Prime Numbers')
ax2.set_ylabel('Density (Prime Numbers)')

# Set the y-axis limits using the maximum density values
ax1.set_ylim(0, np.max(density_prime_lattice))
ax2.set_ylim(0, np.max(density_prime_numbers))

# Display the legend and grid
lines_1, labels_1 = ax1.get_legend_handles_labels()
lines_2, labels_2 = ax2.get_legend_handles_labels()
ax1.legend(lines_1 + lines_2, labels_1 + labels_2, loc='upper left')
ax1.grid(True)

plt.show()

# Constants
pi = 3.141592653589793
two_pi = 2 * pi

# Arrays for plotting
scattering_amplitude = []
momentum = []

# Calculating the zeros of the Riemann Zeta Function
zeta_zeros = []
for n in range(1, num_zeros + 1):
    zeta_zeros.append(zetazero(n).imag)
    if n % 15 == 0:
        print(f"Calculating Riemann Zeta Function zeros: {n}/{num_zeros}...")

# Scattering process in 2D
for wave_number_x in range(1, 6001):
    for wave_number_y in range(1, 6001):
        wave_vector_x = two_pi * wave_number_x * dk
        wave_vector_y = two_pi * wave_number_y * dk
        sum_cosine = 0
        sum_sine = 0
        sum_magnitude = 0

        if wave_number_x % 3 == 0 and wave_number_y % 3 == 0:
            print(f"Calculating scattering amplitude: {wave_number_x}/{6000} (x) | {wave_number_y}/{6000} (y)...")

        for i, prime in enumerate(prime_lattice):
            phase = wave_vector_x * prime + wave_vector_y * prime
            sum_cosine += np.cos(phase)
            sum_sine += np.sin(phase)

            sum_cosine_squared = sum_cosine ** 2
            sum_sine_squared = sum_sine ** 2
            sum_cosine_sine = sum_cosine_squared + sum_sine_squared
            sum_magnitude += np.sqrt(sum_cosine_sine)

        scattering_amplitude.append(sum_magnitude)
        momentum.append((wave_vector_x, wave_vector_y))

# Scatter plot of the scattering amplitude in 2D
plt.scatter([k[0] for k in momentum], [k[1] for k in momentum], c=scattering_amplitude, s=1, cmap='viridis')
cbar = plt.colorbar()
cbar.set_label('Scattering Amplitude')
plt.xlabel('Momentum (k_x in units of 2*pi/a)')
plt.ylabel('Momentum (k_y in units of 2*pi/a)')
plt.title('Scattering Amplitude vs Momentum (2D)')
plt.grid(True)
plt.legend(['Scattering Amplitude'])
plt.xlim(k_min, k_max)
plt.ylim(k_min, k_max)
plt.show()

# Scatter plot with zeros of the Riemann Zeta Function
plt.scatter([k[0] for k in momentum], [k[1] for k in momentum], c=scattering_amplitude, s=1, cmap='viridis')
for zero in zeta_zeros:
    plt.scatter(zero, 0, color='r', marker='x')
    plt.axvline(x=zero, color='r', linestyle='--',linewidth=0.5)
plt.xlabel('Momentum (k_x in units of 2pi/a)')
plt.ylabel('Momentum (k_y in units of 2pi/a)')
plt.title('Scattering Amplitude vs Momentum (2D) with Zeta Zeros')
plt.grid(True)
cbar = plt.colorbar()
cbar.set_label('Scattering Amplitude')
plt.xlim(k_min, k_max)
plt.ylim(k_min, k_max)
plt.show()
