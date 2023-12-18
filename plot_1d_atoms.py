import numpy as np
import matplotlib.pyplot as plt
from sympy import primerange
from mpmath import zetazero
import math

num_primes = 5000
size = 3 
# 1D Calculation and Plotting
prime_numbers = np.array(list(primerange(1, num_primes + 1)))

plt.scatter(prime_numbers, [0]*len(prime_numbers), s=size, color='red')
plt.scatter(prime_numbers, [sum([1 for j in prime_numbers if j < p]) for p in prime_numbers], s=1, color='red') 

prime_lattice = np.array([math.log(x) for x in prime_numbers])
plt.scatter(prime_lattice, [1.0]*len(prime_lattice), s=size, color='blue')
plt.scatter(prime_lattice, [sum([1 for j in prime_lattice if j < p]) for p in prime_lattice], s=1, color='blue') 

plt.xlim(-1,max(prime_lattice))
plt.ylim(-1,max(prime_lattice))
plt.xlabel('Position')
plt.ylabel('Counting function')
plt.grid(True, which='both', axis='x', linestyle='--', linewidth=0.5)
#plt.title('One-Dimensional Lattice of primes')
plt.show()

plt.scatter(prime_lattice, [0]*len(prime_lattice), s=size, color='blue')

# Set the limits for the plot to make sure all atoms are visible

# Add grid, title and show the plot
plt.grid(True, which='both', axis='x', linestyle='--', linewidth=0.5)
plt.title('One-Dimensional Lattice of primes')
plt.show()




