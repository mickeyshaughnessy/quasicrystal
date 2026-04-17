import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Wedge, Polygon, Circle
from mpl_toolkits.mplot3d import Axes3D
from contour_integral_toolkit import ContourIntegralPlotter

# Integral: ∫₀^∞ ln(x)/(x²+1) dx using keyhole contour

print("\n" + "="*70)
print("LOGARITHMIC INTEGRAL VISUALIZATION - CORRECTED VERSION")
print("Integral: ∫₀^∞ ln(x)/(x²+1) dx")
print("="*70)

# Diagram 1: The integrand and its singularities
print("\n--- Diagram 1: Identifying Singularities ---")
print("The integrand f(z) = ln(z)/(z²+1) has three types of singularities:")
print("• Two simple poles at z = ±i from the denominator z²+1 = 0")
print("• A branch point at z = 0 from the multi-valued logarithm")
print("IMPORTANT: We choose the branch cut along the POSITIVE real axis")
print("(where we want to integrate!)")

plotter1 = ContourIntegralPlotter(xlim=(-3, 3), ylim=(-3, 3))
plotter1.set_title(r"Logarithmic Integral: $\int_0^{\infty} \frac{\ln(x)}{x^2 + 1} dx$")

# Add poles at ±i
plotter1.add_pole(0+1j, label='z = i', color='red')
plotter1.add_pole(0-1j, label='z = -i', color='red')

# Add branch point at origin
plotter1.add_pole(0+0j, label='Branch point\nz = 0', color='purple')

# Add branch cut along POSITIVE real axis (corrected!)
plotter1.add_branch_cut(0+0j, 3+0j, label='Branch cut')

# Show the desired integral path (which is now along the branch cut)
plotter1.ax.plot([0.1, 3], [0.05, 0.05], 'g-', linewidth=3, alpha=0.7, label='Integration path (top)')
plotter1.ax.plot([3, 0.1], [-0.05, -0.05], 'b-', linewidth=3, alpha=0.7, label='Integration path (bottom)')
plotter1.ax.arrow(1.5, 0.05, 0.2, 0, head_width=0.1, head_length=0.1, fc='green', ec='green')
plotter1.ax.arrow(1.5, -0.05, -0.2, 0, head_width=0.1, head_length=0.1, fc='blue', ec='blue')

# Add text
plotter1.add_text(1.5+2.5j, r'$f(z) = \frac{\ln(z)}{z^2 + 1}$', fontsize=12,
                 bbox=dict(boxstyle="round,pad=0.3", facecolor="lightyellow"))
plotter1.add_text(1.5+1.8j, 'Poles from denominator', fontsize=10)
plotter1.add_text(2.5+0.5j, 'Branch cut along\npositive real axis', fontsize=10, color='orange')

plotter1.ax.legend(loc='upper left')
plotter1.show()

# Diagram 2: Understanding Branch Cuts
print("\n--- Diagram 2: Why We Place the Branch Cut on the Positive Real Axis ---")
print("For the integral ∫₀^∞ ln(x)/(x²+1) dx:")
print("• We need to integrate from 0 to ∞ along the positive real axis")
print("• By placing the branch cut there, the keyhole naturally surrounds our path")
print("• This creates different values of ln(z) above and below the cut")

plotter2 = ContourIntegralPlotter(xlim=(-3, 3), ylim=(-3, 3))
plotter2.set_title("Branch Cut Placement Strategy")

# Add singularities
plotter2.add_pole(0+1j, color='red')
plotter2.add_pole(0-1j, color='red')
plotter2.add_pole(0+0j, color='purple')

# Show branch cut on positive real axis
plotter2.add_branch_cut(0+0j, 3+0j, label='Branch cut')

# Show the principal branch
plotter2.add_text(-2+2j, 'Principal branch:', fontsize=11, weight='bold')
plotter2.add_text(-2+1.6j, r'$-\pi < \arg(z) \leq \pi$', fontsize=10)
plotter2.add_text(-2+1.2j, 'Single-valued everywhere\nexcept on the cut', fontsize=9)

# Show values near the cut
plotter2.ax.arrow(1.5, 0.5, 0, -0.35, head_width=0.08, head_length=0.05, fc='green', ec='green')
plotter2.add_text(1.5+0.7j, r'Just above: $\ln(z) = \ln|z| + i \cdot 0^+$', fontsize=10, color='green')

plotter2.ax.arrow(1.5, -0.5, 0, 0.35, head_width=0.08, head_length=0.05, fc='blue', ec='blue')
plotter2.add_text(1.5-0.7j, r'Just below: $\ln(z) = \ln|z| + i \cdot 2\pi^-$', fontsize=10, color='blue')

plotter2.add_text(0.3+0j, 'Jump of 2πi', fontsize=11, color='red', weight='bold',
                 bbox=dict(boxstyle="round,pad=0.3", facecolor="yellow"))

plotter2.show()

# Diagram 3: The keyhole contour - CORRECTED
print("\n--- Diagram 3: The Corrected Keyhole Contour ---")
print("The keyhole contour with branch cut on POSITIVE real axis:")
print("• Large circle C_R (counterclockwise) encloses both poles")
print("• Line L₁ along TOP of positive real axis (right to left)")
print("• Small circle C_ε around origin (clockwise)")
print("• Line L₂ along BOTTOM of positive real axis (left to right)")
print("The 'keyhole' slot is where the branch cut is!")

plotter3 = ContourIntegralPlotter(xlim=(-3, 3), ylim=(-3, 3))
plotter3.set_title("Corrected Keyhole Contour")

# Add singularities
plotter3.add_pole(0+1j, color='red', label='z = i (inside)')
plotter3.add_pole(0-1j, color='red', label='z = -i (inside)')
plotter3.add_pole(0+0j, color='purple')
plotter3.add_branch_cut(0+0j, 3+0j)

# Draw keyhole contour
R = 2.5
eps = 0.2
gap = 0.03  # Small gap in angle for the keyhole slot

# Large circle C_R (avoiding the positive real axis)
theta = np.linspace(gap, 2*np.pi-gap, 200)
x = R * np.cos(theta)
y = R * np.sin(theta)
plotter3.ax.plot(x, y, 'g-', linewidth=2.5, label='Keyhole contour')

# Line L₁: Top of positive real axis (R to ε)
plotter3.ax.plot([R*np.cos(gap), eps], [0.03, 0.03], 'g-', linewidth=2.5)
plotter3.ax.arrow(1.5, 0.03, -0.2, 0, head_width=0.08, head_length=0.08, fc='green', ec='green')

# Small circle C_ε (clockwise)
theta_small = np.linspace(0, 2*np.pi, 100)
x_small = eps * np.cos(theta_small)
y_small = eps * np.sin(theta_small)
plotter3.ax.plot(x_small, y_small, 'g-', linewidth=2.5)
plotter3.ax.arrow(-eps*0.7, -eps*0.7, 0.05, -0.05, head_width=0.05, head_length=0.03, fc='green', ec='green')

# Line L₂: Bottom of positive real axis (ε to R)
plotter3.ax.plot([eps, R*np.cos(-gap)], [-0.03, -0.03], 'g-', linewidth=2.5)
plotter3.ax.arrow(1.5, -0.03, 0.2, 0, head_width=0.08, head_length=0.08, fc='green', ec='green')

# Fill to show inside
vertices = []
# Large circle
for t in theta:
    vertices.append((R*np.cos(t), R*np.sin(t)))
# Top line
vertices.append((eps, 0.03))
# Small circle (reversed)
for t in reversed(theta_small):
    vertices.append((eps*np.cos(t), eps*np.sin(t)))
# Bottom line
vertices.append((R*np.cos(-gap), -0.03))

patch = Polygon(vertices, alpha=0.1, color='lightgreen')
plotter3.ax.add_patch(patch)

# Label the parts
plotter3.add_text(1.8+1.8j, r'$C_R$', fontsize=12, color='darkgreen', weight='bold')
plotter3.add_text(1.2+0.25j, r'$L_1$', fontsize=12, color='darkgreen', weight='bold')
plotter3.add_text(0.35+0.35j, r'$C_\epsilon$', fontsize=12, color='darkgreen', weight='bold')
plotter3.add_text(1.2-0.25j, r'$L_2$', fontsize=12, color='darkgreen', weight='bold')

# Emphasize both poles are inside
plotter3.add_text(0+2.3j, 'Both poles are INSIDE\nthe keyhole contour!', fontsize=12, color='red', weight='bold',
                 bbox=dict(boxstyle="round,pad=0.3", facecolor="yellow"))

plotter3.ax.legend(loc='upper left')
plotter3.show()

# Diagram 4: Values of ln(z) on different parts
print("\n--- Diagram 4: How ln(z) Changes Across the Branch Cut ---")
print("The key insight for the positive real axis branch cut:")
print("• On L₁ (top): z approaches positive real from above, arg(z) → 0⁺")
print("  So ln(z) → ln(x) + i·0 = ln(x)")
print("• On L₂ (bottom): z approaches positive real from below, arg(z) → 2π⁻")
print("  So ln(z) → ln(x) + i·2π")
print("This 2πi difference is crucial!")

plotter4 = ContourIntegralPlotter(xlim=(-1, 4), ylim=(-2, 2))
plotter4.set_title(r"Values of $\ln(z)$ on Lines $L_1$ and $L_2$")

# Show branch cut
plotter4.add_branch_cut(0+0j, 3.5+0j, label='Branch cut')

# Show the two paths clearly
plotter4.ax.plot([0.1, 3.5], [0.15, 0.15], 'g-', linewidth=3, label=r'$L_1$ (top)')
plotter4.ax.plot([3.5, 0.1], [-0.15, -0.15], 'b-', linewidth=3, label=r'$L_2$ (bottom)')
plotter4.ax.arrow(2, 0.15, -0.2, 0, head_width=0.1, head_length=0.1, fc='green', ec='green')
plotter4.ax.arrow(2, -0.15, 0.2, 0, head_width=0.1, head_length=0.1, fc='blue', ec='blue')

# Add text explaining ln values
plotter4.add_text(1.75+0.6j, r'$L_1$: $\ln(z) = \ln(x)$', fontsize=12, color='green',
                 bbox=dict(boxstyle="round,pad=0.3", facecolor="lightgreen"))
plotter4.add_text(1.75-0.6j, r'$L_2$: $\ln(z) = \ln(x) + 2\pi i$', fontsize=12, color='blue',
                 bbox=dict(boxstyle="round,pad=0.3", facecolor="lightblue"))

plotter4.add_text(0.5+1.2j, 'For positive real x:', fontsize=11, weight='bold')
plotter4.add_text(0.5+0.9j, r'• Approaching from above: $\arg(z) = 0$', fontsize=10)
plotter4.add_text(0.5-0.9j, r'• Approaching from below: $\arg(z) = 2\pi$', fontsize=10)
plotter4.add_text(0.5-1.2j, '(going around counterclockwise)', fontsize=9, style='italic')

plotter4.ax.legend(loc='upper right')
plotter4.show()

# Diagram 5: Residue calculations
print("\n--- Diagram 5: Calculating the Residues ---")
print("Both poles z = ±i are simple poles.")
print("For f(z) = ln(z)/(z²+1), we factor: z²+1 = (z-i)(z+i)")
print("")
print("Residue at z = i:")
print("  Res(f,i) = lim[z→i] (z-i)·ln(z)/((z-i)(z+i))")
print("           = ln(i)/(2i) = (iπ/2)/(2i) = π/4")
print("")
print("Residue at z = -i:")
print("  Res(f,-i) = lim[z→-i] (z+i)·ln(z)/((z-i)(z+i))")
print("            = ln(-i)/(-2i) = (-iπ/2)/(-2i) = π/4")

plotter5 = ContourIntegralPlotter(xlim=(-3, 3), ylim=(-1.5, 2.5))
plotter5.set_title("Residue Calculations")

# Show both poles
plotter5.add_pole(0+1j, label='z = i', color='red')
plotter5.add_pole(0-1j, label='z = -i', color='red')

# Small contours around each pole
plotter5.add_circular_contour(center=0+1j, radius=0.3, color='blue', arrows=False)
plotter5.add_circular_contour(center=0-1j, radius=0.3, color='blue', arrows=False)

# Residue calculations
plotter5.add_text(-2.8+2.2j, 'At z = i:', fontsize=11, weight='bold', color='red')
plotter5.add_text(-2.8+1.85j, r'$\ln(i) = \ln|i| + i\arg(i) = 0 + i\frac{\pi}{2}$', fontsize=10)
plotter5.add_text(-2.8+1.5j, r'$\text{Res}(f,i) = \frac{\ln(i)}{2i} = \frac{i\pi/2}{2i} = \frac{\pi}{4}$', fontsize=10)

plotter5.add_text(-2.8+0.7j, 'At z = -i:', fontsize=11, weight='bold', color='red')
plotter5.add_text(-2.8+0.35j, r'$\ln(-i) = \ln|-i| + i\arg(-i) = 0 - i\frac{\pi}{2}$', fontsize=10)
plotter5.add_text(-2.8+0j, r'$\text{Res}(f,-i) = \frac{\ln(-i)}{-2i} = \frac{-i\pi/2}{-2i} = \frac{\pi}{4}$', fontsize=10)

plotter5.add_text(-2.8-0.7j, 'Sum of residues:', fontsize=11, weight='bold')
plotter5.add_text(-2.8-1.1j, r'$\text{Res}(f,i) + \text{Res}(f,-i) = \frac{\pi}{4} + \frac{\pi}{4} = \frac{\pi}{2}$', 
                  fontsize=12, color='blue',
                  bbox=dict(boxstyle="round,pad=0.3", facecolor="lightgreen"))

plotter5.show()

# Diagram 6: Applying the Residue Theorem
print("\n--- Diagram 6: Applying the Residue Theorem ---")
print("By the Residue Theorem:")
print("∮_keyhole f(z)dz = 2πi × (sum of residues inside)")
print("                = 2πi × π/2 = iπ²")
print("")
print("But also:")
print("∮_keyhole = ∫_{C_R} + ∫_{L_1} + ∫_{C_ε} + ∫_{L_2}")

plotter6 = ContourIntegralPlotter(xlim=(-3, 3), ylim=(-3, 3))
plotter6.set_title("Residue Theorem Application")

# Redraw keyhole for reference
R = 2.5
eps = 0.2
gap = 0.03
theta = np.linspace(gap, 2*np.pi-gap, 100)
plotter6.ax.plot(R*np.cos(theta), R*np.sin(theta), 'g--', linewidth=1, alpha=0.5)
plotter6.ax.plot([R*np.cos(gap), eps], [0.03, 0.03], 'g--', linewidth=1, alpha=0.5)
plotter6.ax.plot([eps, R*np.cos(-gap)], [-0.03, -0.03], 'g--', linewidth=1, alpha=0.5)
theta_small = np.linspace(0, 2*np.pi, 50)
plotter6.ax.plot(eps*np.cos(theta_small), eps*np.sin(theta_small), 'g--', linewidth=1, alpha=0.5)

# Add both poles
plotter6.add_pole(0+1j, color='red')
plotter6.add_pole(0-1j, color='red')
plotter6.add_pole(0+0j, color='purple')
plotter6.add_branch_cut(0+0j, 3+0j)

# Add equation
plotter6.add_text(0+2.4j, r'$\oint_{\text{keyhole}} \frac{\ln(z)}{z^2+1} dz = 2\pi i \cdot \frac{\pi}{2} = i\pi^2$',
                 fontsize=12, bbox=dict(boxstyle="round,pad=0.3", facecolor="yellow"),
                 ha='center', weight='bold')

plotter6.add_text(-2.5-1.5j, r'Also: $\oint = \int_{C_R} + \int_{L_1} + \int_{C_\epsilon} + \int_{L_2}$',
                 fontsize=11)
plotter6.add_text(-2.5-2j, 'We need to evaluate each piece...', fontsize=10, style='italic')

plotter6.show()

# Diagram 7: Taking limits
print("\n--- Diagram 7: Taking Limits R→∞ and ε→0 ---")
print("As R → ∞:")
print("  |∫_{C_R}| ≤ 2πR · max|f(z)| ~ 2πR · ln(R)/R² → 0")
print("")
print("As ε → 0:")
print("  |∫_{C_ε}| ≤ 2πε · max|f(z)| ~ 2πε · |ln(ε)|/1 → 0")
print("  (since ε·ln(ε) → 0 as ε → 0)")
print("")
print("Therefore in the limit, only L₁ and L₂ survive!")

plotter7 = ContourIntegralPlotter(xlim=(-3, 3), ylim=(-3, 3))
plotter7.set_title(r"Taking Limits: $R \to \infty$, $\epsilon \to 0$")

# Show shrinking/expanding contours
for R, alpha in [(1.5, 0.3), (2, 0.6), (2.5, 1.0)]:
    theta = np.linspace(0.03, 2*np.pi-0.03, 100)
    plotter7.ax.plot(R*np.cos(theta), R*np.sin(theta), 'b-', linewidth=1.5, alpha=alpha)
    
for eps, alpha in [(0.4, 0.3), (0.25, 0.6), (0.1, 1.0)]:
    theta_small = np.linspace(0, 2*np.pi, 50)
    plotter7.ax.plot(eps*np.cos(theta_small), eps*np.sin(theta_small), 'r-', linewidth=1.5, alpha=alpha)

plotter7.add_text(2+2j, r'$C_R \to 0$', fontsize=12, color='blue')
plotter7.add_text(0.5+0.5j, r'$C_\epsilon \to 0$', fontsize=12, color='red')

# Add vanishing calculations
plotter7.add_text(-2.8+1.5j, r'$\left|\int_{C_R}\right| \leq \frac{2\pi R \ln R}{R^2-1} \to 0$', 
                 fontsize=11, color='blue')
plotter7.add_text(-2.8+0.8j, r'$\left|\int_{C_\epsilon}\right| = O(\epsilon \ln \epsilon) \to 0$', 
                 fontsize=11, color='red')

plotter7.add_text(-2.8-0.5j, 'In the limit:', fontsize=11, weight='bold')
plotter7.add_text(-2.8-1j, r'$\int_{L_1} + \int_{L_2} = i\pi^2$', fontsize=12,
                 bbox=dict(boxstyle="round,pad=0.3", facecolor="lightcyan"))

plotter7.show()

# Diagram 8: Evaluating the line integrals
print("\n--- Diagram 8: The Line Integrals L₁ and L₂ ---")
print("On L₁ (top of cut): z = x + i0⁺, so ln(z) = ln(x)")
print("  ∫_{L₁} = ∫_∞^0 ln(x)/(x²+1) dx = -∫_0^∞ ln(x)/(x²+1) dx")
print("")
print("On L₂ (bottom of cut): z = x + i0⁻, so ln(z) = ln(x) + 2πi")
print("  ∫_{L₂} = ∫_0^∞ (ln(x) + 2πi)/(x²+1) dx")
print("         = ∫_0^∞ ln(x)/(x²+1) dx + 2πi·∫_0^∞ 1/(x²+1) dx")
print("         = I + 2πi·(π/2) = I + iπ²")
print("")
print("Therefore: ∫_{L₁} + ∫_{L₂} = -I + (I + iπ²) = iπ²")

plotter8 = ContourIntegralPlotter(xlim=(-1, 4), ylim=(-2, 2))
plotter8.set_title(r"Evaluating $L_1$ and $L_2$")

# Show the two paths
plotter8.ax.plot([0, 3.5], [0.2, 0.2], 'g-', linewidth=3, label=r'$L_1$')
plotter8.ax.plot([3.5, 0], [-0.2, -0.2], 'b-', linewidth=3, label=r'$L_2$')
plotter8.ax.arrow(1.75, 0.2, -0.2, 0, head_width=0.1, head_length=0.1, fc='green', ec='green')
plotter8.ax.arrow(1.75, -0.2, 0.2, 0, head_width=0.1, head_length=0.1, fc='blue', ec='blue')

# Show ln values and integrals
plotter8.add_text(1.75+0.7j, r'$\int_{L_1} = -I$', fontsize=12, color='green',
                 bbox=dict(boxstyle="round,pad=0.3", facecolor="lightgreen"))
plotter8.add_text(1.75-0.7j, r'$\int_{L_2} = I + i\pi^2$', fontsize=12, color='blue',
                 bbox=dict(boxstyle="round,pad=0.3", facecolor="lightblue"))

plotter8.add_text(0.5-1.5j, r'$\int_{L_1} + \int_{L_2} = -I + (I + i\pi^2) = i\pi^2$', 
                 fontsize=12, weight='bold',
                 bbox=dict(boxstyle="round,pad=0.3", facecolor="yellow"))

plotter8.ax.legend(loc='upper right')
plotter8.show()

# Diagram 9: Putting it all together
print("\n--- Diagram 9: Solving for the Integral ---")
print("From the Residue Theorem:")
print("  ∮_keyhole = iπ²")
print("")
print("From the limit calculation:")
print("  ∮_keyhole = ∫_{L₁} + ∫_{L₂} = iπ²")
print("")
print("Since ∫_{L₁} + ∫_{L₂} = -I + (I + iπ²) = iπ²")
print("This equation is already satisfied for ANY value of I!")
print("")
print("We need another approach...")

plotter9 = ContourIntegralPlotter(xlim=(-3, 3), ylim=(-3, 3))
plotter9.set_title("The Apparent Problem")

plotter9.add_text(0+2j, "From residues: ∮ = iπ²", fontsize=12, ha='center',
                 bbox=dict(boxstyle="round,pad=0.3", facecolor="lightblue"))
plotter9.add_text(0+1.3j, "From contour parts: ∮ = iπ²", fontsize=12, ha='center',
                 bbox=dict(boxstyle="round,pad=0.3", facecolor="lightgreen"))
plotter9.add_text(0+0.5j, "These agree, but don't determine I!", fontsize=12, ha='center', color='red',
                 bbox=dict(boxstyle="round,pad=0.3", facecolor="yellow"))

plotter9.add_text(0-1j, "Solution: Use the substitution x = 1/t", fontsize=12, ha='center', weight='bold')
plotter9.add_text(0-1.6j, "This shows I = -I, hence I = 0", fontsize=12, ha='center')

plotter9.show()

# Diagram 10: The substitution trick
print("\n--- Diagram 10: The Brilliant Substitution ---")
print("To find I = ∫₀^∞ ln(x)/(x²+1) dx, use substitution x = 1/t:")
print("")
print("When x = 1/t: dx = -dt/t², and x²+1 = (1+t²)/t²")
print("")
print("I = ∫_∞^0 ln(1/t)/((1+t²)/t²) · (-dt/t²)")
print("  = ∫_∞^0 -ln(t)/(1+t²) · (-dt)")
print("  = -∫_0^∞ ln(t)/(1+t²) dt")
print("  = -I")
print("")
print("Therefore: I = -I, which implies 2I = 0, so I = 0!")

plotter10 = ContourIntegralPlotter(xlim=(-0.5, 4), ylim=(-1.5, 1.5))
plotter10.set_title("The Symmetry: Why I = 0")

# Plot the integrand
x = np.linspace(0.01, 4, 400)
y = np.log(x) / (x**2 + 1)
plotter10.ax.plot(x, y, 'b-', linewidth=2.5, label=r'$\frac{\ln(x)}{x^2+1}$')
plotter10.ax.fill_between(x[x<1], 0, y[x<1], alpha=0.3, color='red', label='Negative area')
plotter10.ax.fill_between(x[x>1], 0, y[x>1], alpha=0.3, color='green', label='Positive area')
plotter10.ax.axhline(y=0, color='k', linewidth=0.5)
plotter10.ax.axvline(x=1, color='k', linewidth=0.5, linestyle='--', alpha=0.5)

# Add text
plotter10.add_text(0.3+0.8j, 'x = 1/t maps:', fontsize=11,
                 bbox=dict(boxstyle="round,pad=0.3", facecolor="lightyellow"))
plotter10.add_text(0.3+0.5j, '[0,1] → [∞,1]', fontsize=10)
plotter10.add_text(0.3+0.3j, '[1,∞] → [1,0]', fontsize=10)

plotter10.add_text(2.5-0.8j, 'Equal areas\ncancel out!', fontsize=11, color='purple', weight='bold',
                 bbox=dict(boxstyle="round,pad=0.3", facecolor="lightcyan"))

plotter10.ax.legend(loc='upper right')
plotter10.ax.set_xlim(0, 4)
plotter10.ax.set_ylim(-1.2, 0.8)
plotter10.show()

# Final summary
print("\n" + "="*70)
print("COMPLETE SOLUTION SUMMARY")
print("="*70)
print("\n∫₀^∞ ln(x)/(x²+1) dx = 0")
print("\nKey steps:")
print("1. Place branch cut along positive real axis (where we integrate)")
print("2. Use keyhole contour that encloses both poles z = ±i")
print("3. Apply Residue Theorem: ∮ = 2πi·(π/4 + π/4) = iπ²")
print("4. Evaluate contour parts:")
print("   - C_R → 0 as R → ∞")
print("   - C_ε → 0 as ε → 0")
print("   - L₁ + L₂ = -I + (I + iπ²) = iπ²")
print("5. This confirms the residue result but doesn't determine I")
print("6. Use substitution x = 1/t to show I = -I")
print("7. Therefore I = 0")
print("\nThe beauty: The logarithm's odd symmetry about x = 1 makes the integral vanish!")
print("="*70)