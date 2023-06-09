import numpy as np
import matplotlib.pyplot as plt
from sympy import primerange
from mpmath import zetazero, li
import math

# We'll start by defining some arrays. We're going to need prime numbers - that's what our electrons will be bouncing off.
prime_numbers = np.array(list(primerange(1, 3200000)))  # Generate the first 800000 prime numbers
prime_lattice = np.array([math.log(x) for x in prime_numbers])

# Now, we'll shift the prime numbers, by the prime density function, pi(x) ~ ln(x).
# Physically, this makes the density of scatterers constant, over a long enough length.
# The shifted scattering centers form a quasicrystal, being a sum of point-like dirac delta distributions, separated by a finite distance, > O(1/ln(x))   
# and a constant density.

# prime_numbers = np.array([x/math.log(x) for x in _prime_numbers])
# this is incorrect^
# here do a better job with pi(x):
prime_lattice = np.array([math.log(x) for x in prime_numbers])
#prime_lattice = np.array([pi(x) for x in prime_numbers])
#prime_lattice = np.array([li(x) for x in prime_numbers])
# print out the density of the shifted lattice:
for i, lp in enumerate(prime_lattice):
    print(i, lp, i/lp)
    input()

# And we need some constants, like pi.
pi = 3.141592653589793 
two_pi = 2 * pi
_dk = 0.01 # grid resolution in k-space

# We'll be plotting the scattering amplitude, so we need arrays to store that data.
scattering_amplitude = []
momentum = []

# Now here's where the magic happens. We're going to calculate the zeros of the Riemann Zeta Function.
zeta_zeros = []
for n in range(1, int(9001*_dk)):
    zeta_zeros.append(zetazero(n).imag)
    # We'll print a progress update every ~15 steps so you know the script hasn't fallen asleep on you.
    if n % 15 == 0:
        print(f"Calculating Riemann Zeta Function zeros: {n}/300...")

# Now we get to the scattering process. This is where we calculate how much each electron scatters off the lattic of prime numbers.
for wave_number in range(1, 6001):
    wave_vector = two_pi * wave_number * _dk  # Wave vector (k) in units of 2*pi/a
    sum_cosine = 0  # Sum of cosines
    sum_sine = 0  # Sum of sines
    sum_magnitude = 0  # Sum of magnitudes
    if wave_number % 3 == 0:
        print(f"Calculating scattering amplitude: {i}/{len(prime_lattice)}...")

    for i, prime in enumerate(prime_lattice):
        phase = wave_vector * prime  # Phase = k * prime number
        sum_cosine += np.cos(phase)  # Summing cosines
        sum_sine += np.sin(phase)  # Summing sines

        # Here's where we calculate the magnitude of the scattering amplitude. We're squaring the sums, adding them together, and taking the square root.
        sum_cosine_squared = sum_cosine ** 2
        sum_sine_squared = sum_sine ** 2
        sum_cosine_sine = sum_cosine_squared + sum_sine_squared
        sum_magnitude += np.sqrt(sum_cosine_sine)  # Magnitude of the scattering amplitude

    # Append computed data for plotting
    scattering_amplitude.append(sum_magnitude)
    momentum.append(wave_vector)

# Plot time! We're going to make a scatter plot of the scattering amplitude.
plt.scatter(momentum, scattering_amplitude, s=1)
#plt.plot(momentum, scattering_amplitude)

# And here we add the zeros of the Riemann Zeta Function to the plot. These are really important - they tell us where we expect the scattering amplitude to peak.
for zero in zeta_zeros:
    plt.scatter(zero, 0, color='r', marker='x')  # 'x' marker for zeta zero
    plt.axvline(x=zero, color='r', linestyle='--', linewidth=0.5)  # Vertical line through zeta zero
plt.xlabel('Momentum (k in units of 2*pi/a)')
plt.ylabel('Scattering Amplitude')
plt.title('Scattering Amplitude vs Momentum')
plt.grid(True)
plt.legend(['Scattering Amplitude', 'Zeta Zeros'])
plt.xlim(0, 200)  # Set the limits of the x-axisplt.show()
plt.show()
