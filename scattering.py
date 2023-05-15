import numpy as np
import matplotlib.pyplot as plt
from sympy import primerange

# Define arrays
prime_numbers = np.zeros(1000)  # Prime numbers
shifted_prime_numbers = np.zeros((1000,500))  # Shifted prime numbers

# Generate prime numbers
prime_numbers[:61] = list(primerange(1, 300))[:61]  # Getting the first 61 primes less than 300

# Constants
pi = 3.14159
two_pi = 2 * pi

sum_id = 0
limit_prime = 61
limit_array = 53
sum_id = np.sum(prime_numbers[:limit_prime])
shift_number = sum_id / limit_prime

# Scattering amplitude data for plot
scattering_amplitude = []
momentum = []

for move_count in range(1, 4):
    move_number = prime_numbers[move_count] if move_count != 0 else 0
    shift_total = shift_number + move_number

    # Shift the prime numbers
    shifted_prime_numbers[:limit_array, move_count] = prime_numbers[:limit_array] - shift_number
    prime_numbers[:limit_array] = shifted_prime_numbers[:limit_array, move_count]

    # Scattering process
    for wave_number in range(1, 21):
        wave_vector = two_pi * wave_number * 0.1  # Wave vector (k) in units of 2*pi/a
        sum_cosine = 0  # Sum of cosines
        sum_sine = 0  # Sum of sines
        sum_magnitude = 0  # Sum of magnitudes

        for prime_index in range(1, limit_array + 1):
            prime = prime_numbers[prime_index]
            phase = wave_vector * prime  # Phase = k * prime number
            sum_cosine += np.cos(phase)  # Summing cosines
            sum_sine += np.sin(phase)  # Summing sines

            sum_cosine_squared = sum_cosine ** 2
            sum_sine_squared = sum_sine ** 2
            sum_cosine_sine = sum_cosine_squared + sum_sine_squared
            sum_magnitude += np.sqrt(sum_cosine_sine)  # Magnitude of the scattering amplitude

        # Append computed data for plotting
        scattering_amplitude.append(sum_magnitude)
        momentum.append(wave_vector)

# Split the data into segments, each of length 20 (corresponding to the 20 iterations of wave_number in the inner loop)
segments = [range(i, i + 20) for i in range(0, len(momentum), 20)]

# Plot each segment individually
for segment in segments:
    plt.plot([momentum[i] for i in segment], [scattering_amplitude[i] for i in segment])

plt.xlabel('Momentum (k in units of 2*pi/a)')
plt.ylabel('Scattering Amplitude')
plt.title('Scattering Amplitude vs Momentum')
plt.grid(True)
plt.legend(['Scattering Amplitude'])
plt.show()

