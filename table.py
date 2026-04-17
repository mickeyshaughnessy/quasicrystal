#!/usr/bin/env python3
"""
Generate a LaTeX table of prime scatterer positions.
Columns: n, p_n, ln(p_n) [approx position], p_n/n [exact position], local density
"""
from sympy import primerange, pi as sympy_pi
import math

primes = list(primerange(2, 200))[:20]

print(r"\begin{table}[htbp]")
print(r"\centering")
print(r"\begin{tabular}{|c|c|c|c|c|}")
print(r"\hline")
print(r"$n$ & $p_n$ & $\ln(p_n)$ & $p_n / n$ & Local density \\")
print(r"\hline")

for i, p in enumerate(primes):
    n = i + 1
    ln_p = math.log(p)
    exact_pos = p / n
    # Local density: count primes in [p - window, p + window] / (2*window)
    # Use a window of ~p/4 or at least 5
    window = max(10, p // 4)
    count = len([q for q in primerange(max(2, p - window), p + window + 1)])
    interval_length = 2 * window
    local_density = count / interval_length if interval_length > 0 else 0
    print(f"  {n} & {p} & {ln_p:.4f} & {exact_pos:.4f} & {local_density:.4f} \\\\")

print(r"\hline")
print(r"\end{tabular}")
print(r"\caption{Prime scatterer positions under exact and approximate normalizations. "
      r"The exact position $\chi_n = p_n/n$ and the logarithmic approximation "
      r"$\tilde{\chi}_n = \ln(p_n)$ converge for large $n$ by the prime number theorem. "
      r"Local density is computed over a symmetric window around each prime.}")
print(r"\label{tab:positions}")
print(r"\end{table}")
