# This script demonstrates the distribution of prime numbers is quasicrystalline.

# A quasicrystal is an arrangement of atoms without strict periodicity, but having a point-like diffraction spectrum

# An infinite periodic lattice   

# prime counting function, pi(n), returns the number of primes less than or equal to n.
# so, pi(0) = 0, pi(1) = 1, pi(6) = 4,

from numpy import log as ln
from mpmath import li
from scipy.fft import fft
import math

def is_prime(n):
    if n < 2: return False

    for i in range(2,int(math.sqrt(n))+1):
        if (n%i) == 0:
            return False
    return True

def quick_pi(n):
    return sum([int(is_prime(i)) for i in range(1,n)]) 

def is_primes(n):
    return [int(is_prime(i)) for i in range(0,n)]

def primes(n):
    # returns all primes up to n
    return [i for i in range(1,n) if is_prime(i)]

def ln_transform(seq):
    return [s/ln(s) for s in seq]

def li_transform(seq):
    return [s/li(s) for s in seq]

def li_transform2(seq):
    return [i/li(i) if s !=0 else 0 for i, s in enumerate(seq)]

def RZF_trunc(x, N):
    return sum([1/(s^x) for s in range(N)])

def RZF_zeros(N, tol=1E-6):
    # return the first N RZF zeros
    zeros = []
    while len(zeros) < N:
        # get next zero
        pass         
    return zeros


#for z in [100, 1000, 10000, 100000, 1000000]:
#    p = primes(z)
    
#print(primes(100))    
#print(ln_transform(primes(100)))
#print(len(ln_transform(primes(100)))/ln_transform(primes(100))[-1])
#print(len(ln_transform(primes(1000)))/ln_transform(primes(1000))[-1])
#print(len(ln_transform(primes(10000)))/ln_transform(primes(10000))[-1])
#print(len(ln_transform(primes(100000)))/ln_transform(primes(100000))[-1])
#print(len(ln_transform(primes(1000000)))/ln_transform(primes(1000000))[-1])
#print(len(ln_transform(primes(10000000)))/ln_transform(primes(10000000))[-1])


#print(li(10))
#input()
#print('done')
from scipy.special import zeta
#print(zeta(10))
#input()

# Consider the integral from (0,inf) of the 
X = 500    
import matplotlib.pyplot as plt
#plt.plot([i for i in range(X)],is_primes(X), label="primes")
print(li_transform2(is_primes(X)))




#plt.plot([li_transform(primes(X))], [int(bool(primes(X))])) 


#plt.plot([i/ln(i) for i in range(X*1)],primes(X*1), label="log transformed primes")
#plt.plot([i for i in range(X)], [quick_pi(i)/X for i in range(X)], label="pi(x)")
#plt.plot([i/ln(i) for i in range(X*1)], [quick_pi(i)/(X*1) for i in range(X*1)], label="log transformed pi(x)")
#plt.plot(fft(primes(3000)))

#plt.legend()

plt.show()


     
