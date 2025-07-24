import numpy as np
import matplotlib.pyplot as plt
from sympy import primerange
from mpmath import zetazero
import math

# Parameterization
num_primes_1da = 50000
num_primes_1db = 300000
num_primes_1dc = 900000
num_zeros = 100

dk_1d = 0.01  # Grid resolution in k-space for 1D plot
wave_number_max = 4000

# 1D Calculation and Plotting
prime_numbers_a = np.array(list(primerange(1, num_primes_1da + 1)))
prime_numbers_b = np.array(list(primerange(1, num_primes_1db + 1)))
prime_numbers_c = np.array(list(primerange(1, num_primes_1dc + 1)))
prime_lattice_a = np.array([math.log(x) for x in prime_numbers_a])
prime_lattice_b = np.array([math.log(x) for x in prime_numbers_b])
prime_lattice_c = np.array([math.log(x) for x in prime_numbers_c])

scattering_amplitude_1d_a = []
scattering_amplitude_1d_b = []
scattering_amplitude_1d_c = []
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
    sum_cosine_c, sum_sine_c, sum_magnitude_c = 0, 0, 0

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
    
    for i, prime in enumerate(prime_lattice_c):
        phase = wave_vector * prime
        sum_cosine_c += np.cos(phase)
        sum_sine_c += np.sin(phase)
        sum_cosine_squared_c = sum_cosine_c ** 2
        sum_sine_squared_c = sum_sine_c ** 2
        sum_cosine_sine_c = sum_cosine_squared_c + sum_sine_squared_c
        sum_magnitude_c += np.sqrt(sum_cosine_sine_c)
    
    scattering_amplitude_1d_c.append(sum_magnitude_c)


k_min_1d = 0
k_max_1d = max(momentum_1d)
fig, ax1 = plt.subplots(figsize=(10, 8))  # Set figure size
la, lb = 'Scattering amplitude $L_{{\chi}}$ = {}'.format(num_primes_1da), 'Scattering amplitude $L_{{\chi}}$ = {}'.format(num_primes_1db)
la, lb, lc = 'Scattering amplitude $L_{{\chi}}$ = {}'.format(num_primes_1da), 'Scattering amplitude $L_{{\chi}}$ = {}'.format(num_primes_1db), 'Scattering amplitude $L_{{\chi}}$ = {}'.format(num_primes_1dc)


# Plot the first amplitude on the left y-axis
ax1.scatter(momentum_1d, scattering_amplitude_1d_a, s=5, c='b', label=la)
for i, zero in enumerate(zeta_zeros):
    if i == 0:
        ax1.scatter(zero, 0, color='r', marker='x', label='RZF zeros')
        ax1.axvline(x=zero, color='r', linestyle='--', linewidth=0.5)
    else:
        ax1.scatter(zero, 0, color='r', marker='x')
        ax1.axvline(x=zero, color='r', linestyle='--', linewidth=0.5)
ax1.set_xlabel('Momentum (k in units of 2*pi/a)', fontsize=14)  # Larger font size
ax1.set_ylabel(la, fontsize=14)  # Larger font size for the first amplitude
ax1.set_title('Scattering Amplitude vs Momentum (1D)', fontsize=16)  # Larger font size
ax1.grid(False)  # Turn off the grid
ax1.set_xlim(k_min_1d, k_max_1d)
ax1.set_ylim(np.min(scattering_amplitude_1d_a), 0.05*np.max(scattering_amplitude_1d_a))

# Create a twin Axes for the second amplitude on the right y-axis
ax2 = ax1.twinx()
ax2.scatter(momentum_1d, scattering_amplitude_1d_b, s=5, c='g', label='Scattering amplitude $L_{{\chi}}$ = {}'.format(num_primes_1db))
ax2.set_ylabel(lb, fontsize=14)  # Larger font size for the second amplitude
ax2.set_ylim(np.min(scattering_amplitude_1d_b), 0.05*np.max(scattering_amplitude_1d_b))

ax3 = ax2.twinx()
ax3.scatter(momentum_1d, scattering_amplitude_1d_c, s=5, c='o', label='Scattering amplitude $L_{{\chi}}$ = {}'.format(num_primes_1dc))
ax3.set_ylabel(lc, fontsize=14)  # Larger font size for the second amplitude
ax3.set_ylim(np.min(scattering_amplitude_1d_c), 0.05*np.max(scattering_amplitude_1d_c))

# Combine the legends from both axes
handles1, labels1 = ax1.get_legend_handles_labels()
handles2, labels2 = ax2.get_legend_handles_labels()
handles3, labels3 = ax3.get_legend_handles_labels()

# Rearrange the handles and labels to put "RZF zeros" last
handles = handles1 + handles2 + handles3 
labels = labels1 + labels2 + labels3

# Find the index of the "RZF zeros" label
rzf_zeros_index = labels.index('RZF zeros')

# Move the "RZF zeros" handle and label to the end
handles.append(handles.pop(rzf_zeros_index))
labels.append(labels.pop(rzf_zeros_index))

ax1.legend(handles, labels, fontsize=12, loc='upper right')  # Larger font size and custom location
plt.show()
