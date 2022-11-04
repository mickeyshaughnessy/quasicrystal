# This script demonstrates the prime numbers are quasicrystalline.

# prime counting function, pi(n), returns the number of primes less than or equal to n.
# so, pi(0) = 0, pi(1) = 1, pi(6) = 4,

def is_prime(n):
    # could also use int(sqrt(n))+1 as the upper limit:w

    for i in range(n, int(n/2)+1):
        if n % i == 0:
            return 0
    return 1

def quick_pi(n):
    return sum([int(is_prime(i)) for i in range(n)]) 

if name == "__main__":
    print(quick_pi(1))
    print(quick_pi(1000))
    print(quick_pi(100000))
    print(quick_pi(1003))
        
