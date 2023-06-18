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
dk_2d = 0.01  # Grid resolution in k-space for 2D plot
k_min_1d = 0
k_max_1d = 500
k_min_2d = 0
k_max_2d = 10
wave_number_max = 1000

# 1D Calculation and Plotting
# Atle Selberg: Let's first explore the 1D world of prime lattice scattering.
prime_numbers_a = np.array(list(primerange(1, num_primes_1da + 1)))
prime_numbers_b = np.array(list(primerange(1, num_primes_1db + 1)))
prime_lattice_a = np.array([math.log(x) for x in prime_numbers_a])
prime_lattice_b = np.array([math.log(x) for x in prime_numbers_b])
#prime_lattice = prime_numbers

# Compute the density of the original and shifted lattices
# density = v/i for (i,v) in enumerate(prime_numbers) 
#density_prime_numbers = np.array([v/(i+1) for i,v in enumerate(prime_numbers)])
#density_prime_lattice = np.array([v/(i+1) for i,v in enumerate(prime_lattice)])
#
#print(density_prime_numbers)
#
## Plot the density
#fig, ax1 = plt.subplots()
#ax1.scatter(prime_numbers, density_prime_lattice, label='Prime Lattice')
#ax1.set_xlabel('x')
#ax1.set_ylabel('Density (Prime Lattice)')
#ax1.set_title('Density of Prime Lattice and Prime Numbers')
#
## Create a second y-axis for the density of prime numbers
#ax2 = ax1.twinx()
#ax2.scatter(prime_numbers, density_prime_numbers, color='orange', label='Prime Numbers')
#ax2.set_ylabel('Density (Prime Numbers)')
#
## Set the y-axis limits using the maximum density values
#ax1.set_ylim(0, np.max(density_prime_lattice))
#ax2.set_ylim(0, np.max(density_prime_numbers))
#
## Display the legend and grid
#lines_1, labels_1 = ax1.get_legend_handles_labels()
#lines_2, labels_2 = ax2.get_legend_handles_labels()
#ax1.legend(lines_1 + lines_2, labels_1 + labels_2, loc='upper left')
#ax1.grid(True)
#
#plt.show()

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


plt.scatter(momentum_1d, scattering_amplitude_1d, s=1, c='b')
plt.scatter(momentum_1d, scattering_amplitude_1d, s=1, c='g')
#plt.plot(momentum_1d, scattering_bmplitude_1d, s=1)
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

# 2D Calculation and Plotting
# Freeman Dyson: Now, let's venture into the intriguing 2D realm of prime lattice scattering.
#num_primes_2d = 1000
#num_wave_numbers = 200
#
#prime_numbers_2d = np.array(list(primerange(1, num_primes_2d + 1)))
#
## Generate the prime spiral
#prime_spiral = []
#angle = 0
#radius = 0
#for prime in prime_numbers_2d:
#    x = radius * np.cos(angle)
#    y = radius * np.sin(angle)
#    prime_spiral.append((x, y))
#    radius += 0.2 * math.log(prime)  # Adjust the radius based on the logarithm of prime
#
#scattering_amplitude_2d = []
#momentum_2d = []
#
#for wave_number_x in range(1, num_wave_numbers + 1):
#    for wave_number_y in range(1, num_wave_numbers + 1):
#        wave_vector_x = 2 * np.pi * wave_number_x * dk_2d
#        wave_vector_y = 2 * np.pi * wave_number_y * dk_2d
#        sum_cosine = 0
#        sum_sine = 0
#        sum_magnitude = 0
#
#        if wave_number_x % 3 == 0 and wave_number_y % 3 == 0:
#            print(f"Calculating scattering amplitude (2D): {wave_number_x}/{num_wave_numbers} (x) | {wave_number_y}/{num_wave_numbers} (y)...")
#
#        for i, (x, y) in enumerate(prime_spiral):
#            phase = wave_vector_x * x + wave_vector_y * y
#            sum_cosine += np.cos(phase)
#            sum_sine += np.sin(phase)
#            sum_cosine_squared = sum_cosine ** 2
#            sum_sine_squared = sum_sine ** 2
#            sum_cosine_sine = sum_cosine_squared + sum_sine_squared
#            sum_magnitude += np.sqrt(sum_cosine_sine)
#
#        scattering_amplitude_2d.append(sum_magnitude)
#        momentum_2d.append((wave_vector_x, wave_vector_y))
#
## Plot the prime spiral
#plt.scatter([p[0] for p in prime_spiral], [p[1] for p in prime_spiral], s=1)
#plt.xlabel('x')
#plt.ylabel('y')
#plt.title('Scattering Atom Locations (2D)')
#plt.grid(True)
#plt.show()
#
## Plot the 2D scattering amplitude
#plt.scatter([k[0] for k in momentum_2d], [k[1] for k in momentum_2d], c=scattering_amplitude_2d, s=1, cmap='viridis')
#cbar = plt.colorbar()
#cbar.set_label('Scattering Amplitude')
#plt.xlabel('Momentum (k_x in units of 2*pi/a)')
#plt.ylabel('Momentum (k_y in units of 2*pi/a)')
#plt.title('Scattering Amplitude vs Momentum (2D)')
#plt.grid(True)
#plt.xlim(k_min_2d, k_max_2d)
#plt.ylim(k_min_2d, k_max_2d)
#plt.show()

