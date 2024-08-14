import numpy as np
import matplotlib.pyplot as plt

def is_prime(n):
    if n < 2:
        return False
    for i in range(2, int(np.sqrt(n)) + 1):
        if n % i == 0:
            return False
    return True

def pi(x):
    return sum(1 for i in range(2, int(x)+1) if is_prime(i))

def generate_chi(n):
    primes = [x for x in range(2, n+1) if is_prime(x)][:20]  # Limit to first 20 primes
    chi = [p * (1 / pi(p)) for p in primes]
    return primes, chi

n = 100  # This will give us more than 20 primes
primes, chi = generate_chi(n)

plt.figure(figsize=(12, 8))

# Plot original prime positions
plt.scatter(primes, [0]*len(primes), color='blue', s=100, label='Original prime positions')

# Plot shifted positions (Chi)
plt.scatter(chi, [1]*len(chi), color='orange', s=100, label='Shifted positions (Chi)')

# Add connecting lines
for p, c in zip(primes, chi):
    plt.plot([p, c], [0, 1], 'k--', alpha=0.3)

plt.xlabel('Position', fontsize=12)
plt.ylabel('Distribution', fontsize=12)
plt.title('Shift Operation: First ~20 Prime Numbers to Chi', fontsize=14)
plt.legend(fontsize=10)
plt.grid(True, alpha=0.3)
plt.ylim(-0.1, 1.1)
plt.xlim(0, max(primes))

# Add annotations only for original prime numbers
for p in primes:
    plt.annotate(f'{p}', (p, -0.05), ha='center', va='top', fontsize=8)

plt.tight_layout()
plt.show()
