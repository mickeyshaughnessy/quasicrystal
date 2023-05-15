import numpy as np
import matplotlib.pyplot as plt

# Define arrays
prime_numbers = np.zeros(1000)  # Prime numbers
shifted_prime_numbers = np.zeros((1000,500))  # Shifted prime numbers
prime_number_holder = np.zeros(5000)  # Holder for prime numbers read from file

# Open the input files
with open('prime', 'r') as f_prime, open('cosida', 'w') as f_cosida:
    # Read prime numbers from 'prime' file
    prime_number_holder[:61] = np.fromfile(f_prime, sep=" ", count=61)

    # Assign prime numbers
    prime_numbers[:61] = prime_number_holder[:61]

    # Write prime numbers to 'cosida' file
    np.savetxt(f_cosida, prime_numbers[:61], fmt='%10i')

    # Constants
    pi = 3.14159
    two_pi = 2*pi

    sum_id = 0
    limit_prime = 61
    limit_array = 53
    sum_id = np.sum(prime_numbers[:limit_prime])
    shift_number = sum_id/limit_prime

    # Scattering amplitude data for plot
    scattering_amplitude = []
    momentum = []

    for move_count in range(1, 4):
        move_number = prime_number_holder[move_count] if move_count != 0 else 0
        shift_total = shift_number + move_number

        # Shift the prime numbers
        shifted_prime_numbers[:limit_array,move_count] = prime_numbers[:limit_array] - shift_number
        prime_numbers[:limit_array] = shifted_prime_numbers[:limit_array,move_count]

        f_cosida.write(f'{sum_id:<10}{move_count:<10}{shift_number:<10}{move_number:<10}{shift_total:<10}\n')
        np.savetxt(f_cosida, shifted_prime_numbers[:50, move_count], fmt='%10i')

        # Scattering process
        for wave_number in range(1, 21):
            wave_vector = two_pi * wave_number * 0.1  # wave vector (k) in units of 2*pi/a
            sum_cosine = 0  # Sum of cosines
            sum_sine = 0  # Sum of sines
            sum_magnitude = 0  # Sum of magnitudes

            for prime_index in range(1, limit_array+1):
                prime = prime_numbers[prime_index]
                phase = wave_vector * prime  # Phase = k * prime number
                sum_cosine += np.cos(phase)  # Summing cosines
                sum_sine += np.sin(phase)  # Summing sines

                if prime_index <= 5:
                    f_cosida.write(f'{prime_numbers[prime_index]:<10}{phase:<15.5f}{sum_cosine:<15.5f}{sum_sine:<15.5f}\n')

                sum_cosine_squared = sum_cosine ** 2
                sum_sine_squared = sum_sine ** 2
                sum_cosine_sine = sum_cosine_squared + sum_sine_squared
                sum_magnitude += np.sqrt(sum_cosine_sine)  # Magnitude of the scattering amplitude

            f_cosida.write(f'{wave_number:<10}{wave_vector:<12.5f}{sum_cosine:<12.5f}{sum_sine:<12.5f}{sum_magnitude:<12.5f}\n')

            # Append computed data for plotting
            scattering_amplitude.append(sum_magnitude)
            momentum.append(wave_vector)

# After the computations, we can now plot the scattering amplitude
plt.figure(figsize=(10, 6))
plt.plot(momentum, scattering_amplitude, label='Scattering Amplitude')
plt.xlabel('Momentum (k in units of 2*pi/a)')
plt.ylabel('Scattering Amplitude')
plt.title('Scattering Amplitude vs Momentum')
plt.grid(True)
plt.legend()
plt.show()

