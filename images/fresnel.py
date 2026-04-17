import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Wedge, Polygon
from contour_integral_toolkit import ContourIntegralPlotter

# Integral: ∫₀^∞ cos(x²) dx using e^(iz²)

# Diagram 1: The Fresnel integral and complex approach
plotter1 = ContourIntegralPlotter(xlim=(-3, 3), ylim=(-1, 3))
plotter1.set_title(r"Fresnel Integral: $\int_0^{\infty} \cos(x^2) dx$")

# Show real axis
plotter1.ax.plot([0, 3], [0, 0], 'r-', linewidth=3, label='Integration path')
plotter1.ax.arrow(1.5, 0, 0.2, 0, head_width=0.1, head_length=0.1, fc='red', ec='red')

# Add text explaining the approach
plotter1.add_text(-2.5+2.5j, r'$\cos(x^2) = \text{Re}(e^{ix^2})$', fontsize=12, 
                 bbox=dict(boxstyle="round,pad=0.3", facecolor="lightyellow"))
plotter1.add_text(-2.5+1.8j, r'Consider $f(z) = e^{iz^2}$', fontsize=12)
plotter1.add_text(-2.5+1.1j, r'$f(z)$ is entire (no poles!)', fontsize=12, color='blue')

# Show behavior on real axis
x_vals = np.linspace(0, 2.5, 100)
y_vals = 0.3 * np.cos(x_vals**2)
plotter1.ax.plot(x_vals, y_vals, 'k--', alpha=0.5, label=r'$\cos(x^2)$ oscillations')

plotter1.ax.legend()
plotter1.show()

# Diagram 2: The wedge contour idea
plotter2 = ContourIntegralPlotter(xlim=(-1, 4), ylim=(-1, 4))
plotter2.set_title("The Wedge Contour")

# Draw the wedge
R = 3
angle = np.pi/4  # 45 degrees

# Contour parts
# C1: along real axis
plotter2.ax.plot([0, R], [0, 0], 'g-', linewidth=2.5, label=r'$C_1$: real axis')
plotter2.ax.arrow(R/2, 0, 0.2, 0, head_width=0.1, head_length=0.1, fc='green', ec='green')

# C2: arc
theta = np.linspace(0, angle, 50)
x_arc = R * np.cos(theta)
y_arc = R * np.sin(theta)
plotter2.ax.plot(x_arc, y_arc, 'b-', linewidth=2.5, label=r'$C_2$: arc')
# Arrow on arc
mid_theta = angle/2
plotter2.ax.arrow(R*np.cos(mid_theta), R*np.sin(mid_theta), 
                 -0.2*np.sin(mid_theta), 0.2*np.cos(mid_theta),
                 head_width=0.1, head_length=0.1, fc='blue', ec='blue')

# C3: diagonal line
x_diag = R * np.cos(angle)
y_diag = R * np.sin(angle)
plotter2.ax.plot([x_diag, 0], [y_diag, 0], 'r-', linewidth=2.5, label=r'$C_3$: diagonal')
plotter2.ax.arrow(x_diag/2, y_diag/2, -0.14, -0.14, 
                 head_width=0.1, head_length=0.1, fc='red', ec='red')

# Fill the wedge
wedge = Wedge((0, 0), R, 0, 45, alpha=0.1, color='green')
plotter2.ax.add_patch(wedge)

# Add angle label
plotter2.ax.plot([0, 1], [0, 0], 'k-', linewidth=1)
plotter2.ax.plot([0, 0.707], [0, 0.707], 'k-', linewidth=1)
arc_small = Wedge((0, 0), 0.5, 0, 45, fill=False)
plotter2.ax.add_patch(arc_small)
plotter2.add_text(0.3+0.1j, r'$\pi/4$', fontsize=10)

plotter2.ax.legend()
plotter2.show()

# Diagram 3: Why π/4 angle?
plotter3 = ContourIntegralPlotter(xlim=(-3, 3), ylim=(-3, 3))
plotter3.set_title(r"Why $\pi/4$ Angle? Behavior of $e^{iz^2}$")

# Show different rays
angles = [0, np.pi/6, np.pi/4, np.pi/3, np.pi/2]
colors = ['red', 'orange', 'green', 'orange', 'red']
labels = [r'$\theta=0$', r'$\theta=\pi/6$', r'$\theta=\pi/4$', 
          r'$\theta=\pi/3$', r'$\theta=\pi/2$']

for angle, color, label in zip(angles, colors, labels):
    x = 2.5 * np.cos(angle)
    y = 2.5 * np.sin(angle)
    plotter3.ax.plot([0, x], [0, y], color=color, linewidth=2, label=label)

# Add text explaining decay
plotter3.add_text(-2.8+2.5j, r'On ray $z = re^{i\theta}$:', fontsize=11)
plotter3.add_text(-2.8+2j, r'$|e^{iz^2}| = |e^{ir^2e^{2i\theta}}| = e^{-r^2\sin(2\theta)}$', fontsize=11)
plotter3.add_text(-2.8+1.3j, r'Decay when $\sin(2\theta) > 0$', fontsize=11, color='blue')
plotter3.add_text(-2.8+0.8j, r'i.e., when $0 < \theta < \pi/2$', fontsize=11, color='blue')
plotter3.add_text(-2.8+0.1j, r'At $\theta = \pi/4$: $|e^{iz^2}| = e^{-r^2}$', fontsize=11, 
                 color='green', weight='bold')

plotter3.ax.legend(loc='lower right')
plotter3.show()

# Diagram 4: Cauchy's theorem application
plotter4 = ContourIntegralPlotter(xlim=(-1, 4), ylim=(-1, 4))
plotter4.set_title("Cauchy's Theorem: No Poles Inside")

# Redraw wedge
R = 3
angle = np.pi/4

# Draw filled wedge
vertices = [(0, 0), (R, 0)]
theta = np.linspace(0, angle, 30)
for t in theta:
    vertices.append((R*np.cos(t), R*np.sin(t)))
vertices.append((0, 0))
wedge_poly = Polygon(vertices, alpha=0.2, color='lightgreen')
plotter4.ax.add_patch(wedge_poly)

# Draw contour
plotter4.ax.plot([0, R], [0, 0], 'g-', linewidth=2.5)
plotter4.ax.plot(R*np.cos(theta), R*np.sin(theta), 'b-', linewidth=2.5)
plotter4.ax.plot([R*np.cos(angle), 0], [R*np.sin(angle), 0], 'r-', linewidth=2.5)

# Add text
plotter4.add_text(1+1.5j, r'$f(z) = e^{iz^2}$ is entire', fontsize=12)
plotter4.add_text(1+1j, 'No singularities!', fontsize=12, color='blue')
plotter4.add_text(0.5+2.5j, r'$\oint_{\text{wedge}} e^{iz^2} dz = 0$', fontsize=14,
                 bbox=dict(boxstyle="round,pad=0.3", facecolor="yellow"))

plotter4.show()

# Diagram 5: Parameterizing the contour parts
plotter5 = ContourIntegralPlotter(xlim=(-1, 4), ylim=(-1, 4))
plotter5.set_title("Parameterizing Each Contour Part")

R = 3
angle = np.pi/4

# C1
plotter5.ax.plot([0, R], [0, 0], 'g-', linewidth=3)
plotter5.add_text(1.5-0.5j, r'$C_1: z = x, \, 0 \leq x \leq R$', fontsize=10, color='green')

# C2
theta = np.linspace(0, angle, 50)
plotter5.ax.plot(R*np.cos(theta), R*np.sin(theta), 'b-', linewidth=3)
plotter5.add_text(2.5+1j, r'$C_2: z = Re^{i\theta}$', fontsize=10, color='blue')
plotter5.add_text(2.5+0.6j, r'$0 \leq \theta \leq \pi/4$', fontsize=10, color='blue')

# C3
plotter5.ax.plot([R/np.sqrt(2), 0], [R/np.sqrt(2), 0], 'r-', linewidth=3)
plotter5.add_text(0.7+1.5j, r'$C_3: z = te^{i\pi/4}$', fontsize=10, color='red')
plotter5.add_text(0.7+1.1j, r'$R \geq t \geq 0$', fontsize=10, color='red')

# Origin
plotter5.ax.plot(0, 0, 'ko', markersize=8)
plotter5.add_text(0.1+0.2j, 'Origin', fontsize=9)

plotter5.show()

# Diagram 6: The arc integral vanishes
plotter6 = ContourIntegralPlotter(xlim=(-1, 4), ylim=(-1, 4))
plotter6.set_title(r"Arc Integral $C_2$ Vanishes as $R \to \infty$")

# Draw multiple arcs
for R in [1.5, 2.25, 3]:
    theta = np.linspace(0, np.pi/4, 50)
    alpha = (R - 1.5) / 1.5
    plotter6.ax.plot(R*np.cos(theta), R*np.sin(theta), 'b-', 
                    linewidth=2, alpha=0.3 + 0.7*alpha)

plotter6.add_text(2.5+2.5j, r'$R \to \infty$', fontsize=12, color='blue')

# Add calculation
plotter6.add_text(-0.5+3j, r'$\left|\int_{C_2} e^{iz^2} dz\right| \leq \int_0^{\pi/4} |e^{iR^2e^{2i\theta}}| R d\theta$',
                 fontsize=10)
plotter6.add_text(-0.5+2.4j, r'$= R \int_0^{\pi/4} e^{-R^2\sin(2\theta)} d\theta$', fontsize=10)
plotter6.add_text(-0.5+1.8j, r'$\leq R \int_0^{\pi/4} e^{-R^2 \cdot \frac{4\theta}{\pi}} d\theta$', fontsize=10)
plotter6.add_text(-0.5+1.2j, r'$= \frac{\pi}{4R}(1 - e^{-R^2}) \to 0$', fontsize=10, color='blue')

plotter6.show()

# Diagram 7: The diagonal integral
plotter7 = ContourIntegralPlotter(xlim=(-1, 4), ylim=(-1, 4))
plotter7.set_title(r"Evaluating the Diagonal Integral $C_3$")

# Draw diagonal
R = 3
plotter7.ax.plot([0, R/np.sqrt(2)], [0, R/np.sqrt(2)], 'r-', linewidth=3)
plotter7.ax.arrow(R/(2*np.sqrt(2)), R/(2*np.sqrt(2)), -0.1, -0.1,
                 head_width=0.1, head_length=0.1, fc='red', ec='red')

# Add parameterization
plotter7.add_text(0.5+2.5j, r'$z = te^{i\pi/4} = \frac{t}{\sqrt{2}}(1 + i)$', fontsize=12)
plotter7.add_text(0.5+2j, r'$z^2 = t^2 e^{i\pi/2} = it^2$', fontsize=12, color='blue')
plotter7.add_text(0.5+1.5j, r'$dz = e^{i\pi/4} dt = \frac{1+i}{\sqrt{2}} dt$', fontsize=12)

plotter7.add_text(-0.8+0.5j, r'$\int_{C_3} e^{iz^2} dz = -\int_0^R e^{i \cdot it^2} \frac{1+i}{\sqrt{2}} dt$',
                 fontsize=11, bbox=dict(boxstyle="round,pad=0.3", facecolor="lightpink"))
plotter7.add_text(-0.8-0.1j, r'$= -\frac{1+i}{\sqrt{2}} \int_0^R e^{-t^2} dt$', fontsize=11)

plotter7.show()

# Diagram 8: Combining the results
plotter8 = ContourIntegralPlotter(xlim=(-3, 3), ylim=(-2, 3))
plotter8.set_title("Combining All Three Integrals")

# Show the equation
plotter8.add_text(-2.5+2.5j, r'$\oint = \int_{C_1} + \int_{C_2} + \int_{C_3} = 0$', 
                 fontsize=14, bbox=dict(boxstyle="round,pad=0.3", facecolor="lightgreen"))

plotter8.add_text(-2.5+1.7j, r'$\int_0^R e^{ix^2} dx + 0 - \frac{1+i}{\sqrt{2}} \int_0^R e^{-t^2} dt = 0$',
                 fontsize=12)

plotter8.add_text(-2.5+0.9j, 'Taking the limit as $R \\to \\infty$:', fontsize=11)

plotter8.add_text(-2.5+0.2j, r'$\int_0^{\infty} e^{ix^2} dx = \frac{1+i}{\sqrt{2}} \int_0^{\infty} e^{-t^2} dt$',
                 fontsize=12, color='blue')

plotter8.add_text(-2.5-0.6j, r'Using $\int_0^{\infty} e^{-t^2} dt = \frac{\sqrt{\pi}}{2}$:', fontsize=11)

plotter8.add_text(-2.5-1.4j, r'$\int_0^{\infty} e^{ix^2} dx = \frac{1+i}{\sqrt{2}} \cdot \frac{\sqrt{\pi}}{2}$',
                 fontsize=12, color='red')

plotter8.show()

# Diagram 9: Final calculation
plotter9 = ContourIntegralPlotter(xlim=(-3, 3), ylim=(-3, 3))
plotter9.set_title("Final Result: Fresnel Integrals")

# Show the calculation
plotter9.add_text(-2.8+2.5j, r'$\int_0^{\infty} e^{ix^2} dx = \frac{1+i}{\sqrt{2}} \cdot \frac{\sqrt{\pi}}{2}$',
                 fontsize=12)

plotter9.add_text(-2.8+1.8j, r'$= \frac{\sqrt{\pi}}{2} \cdot \frac{1+i}{\sqrt{2}} = \frac{\sqrt{\pi}}{2} \cdot \frac{e^{i\pi/4}}{\sqrt[4]{2}}$',
                 fontsize=11)

plotter9.add_text(-2.8+1j, r'$= \frac{\sqrt{\pi}}{2\sqrt{2}}(1 + i)$', fontsize=12, color='blue')

plotter9.add_text(-2.8+0j, 'Taking real and imaginary parts:', fontsize=11)

plotter9.add_text(-2.8-0.8j, r'$\int_0^{\infty} \cos(x^2) dx = \text{Re}\left(\int_0^{\infty} e^{ix^2} dx\right) = \frac{\sqrt{\pi}}{2\sqrt{2}}$',
                 fontsize=12, color='red', bbox=dict(boxstyle="round,pad=0.3", facecolor="yellow"))

plotter9.add_text(-2.8-1.6j, r'$\int_0^{\infty} \sin(x^2) dx = \text{Im}\left(\int_0^{\infty} e^{ix^2} dx\right) = \frac{\sqrt{\pi}}{2\sqrt{2}}$',
                 fontsize=12, color='red', bbox=dict(boxstyle="round,pad=0.3", facecolor="yellow"))

plotter9.add_text(-2.8-2.5j, r'Both Fresnel integrals equal $\frac{1}{2}\sqrt{\frac{\pi}{2}}$', 
                 fontsize=11, weight='bold')

plotter9.show()

# Diagram 10: Summary visualization
plotter10 = ContourIntegralPlotter(xlim=(-1, 4), ylim=(-1, 4))
plotter10.set_title(r"Fresnel Integral: Complete Solution")

# Draw the final wedge with annotations
R = 3.5
angle = np.pi/4

# Wedge contour
plotter10.ax.plot([0, R], [0, 0], 'g-', linewidth=3, label=r'$\int_0^{\infty} e^{ix^2}dx$')
theta = np.linspace(0, angle, 50)
plotter10.ax.plot(R*np.cos(theta), R*np.sin(theta), 'b--', linewidth=2, 
                 label=r'Vanishes as $R \to \infty$')
plotter10.ax.plot([R/np.sqrt(2), 0], [R/np.sqrt(2), 0], 'r-', linewidth=3,
                 label=r'Becomes Gaussian')

# Fill
vertices = [(0, 0), (R, 0)]
for t in theta:
    vertices.append((R*np.cos(t), R*np.sin(t)))
vertices.append((0, 0))
wedge_poly = Polygon(vertices, alpha=0.15, color='lightblue')
plotter10.ax.add_patch(wedge_poly)

# Key insight
plotter10.add_text(0.3+2.8j, 
    r'Key insight: Rotate to $e^{i\pi/4}$ direction' + '\n' +
    r'where $e^{iz^2}$ becomes Gaussian $e^{-t^2}$!',
    fontsize=11, bbox=dict(boxstyle="round,pad=0.4", facecolor="lightcyan"))

# Result
plotter10.add_text(1.5+0.6j, r'$\int_0^{\infty} \cos(x^2) dx = \frac{1}{2}\sqrt{\frac{\pi}{2}}$',
                 fontsize=14, color='red', weight='bold',
                 bbox=dict(boxstyle="round,pad=0.5", facecolor="yellow"))

plotter10.ax.legend(loc='upper left')
plotter10.show()

print("\nFresnel Integral Analysis Complete!")
print(f"\n∫₀^∞ cos(x²) dx = {np.sqrt(np.pi/8):.6f}")
print(f"∫₀^∞ sin(x²) dx = {np.sqrt(np.pi/8):.6f}")
print("\nThe wedge contour brilliantly transforms the oscillatory integral")
print("into a Gaussian integral by rotating into the complex plane!")