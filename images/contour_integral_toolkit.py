import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.patches import FancyArrowPatch, Circle, Wedge, Rectangle
from matplotlib.path import Path
import matplotlib.patches as mpatches

class ContourIntegralPlotter:
    """A class for creating beautiful contour integral diagrams in the complex plane."""
    
    def __init__(self, figsize=(8, 8), xlim=(-3, 3), ylim=(-3, 3)):
        self.fig, self.ax = plt.subplots(1, 1, figsize=figsize)
        self.ax.set_xlim(xlim)
        self.ax.set_ylim(ylim)
        self.ax.set_aspect('equal')
        self.ax.grid(True, alpha=0.3)
        self.ax.axhline(y=0, color='k', linewidth=0.5)
        self.ax.axvline(x=0, color='k', linewidth=0.5)
        self.ax.set_xlabel('Re(z)', fontsize=12)
        self.ax.set_ylabel('Im(z)', fontsize=12)
        
    def add_pole(self, z, order=1, label=None, color='red'):
        """Add a pole to the diagram."""
        x, y = z.real, z.imag
        if order == 1:
            # Simple pole - use X
            self.ax.plot(x, y, 'x', color=color, markersize=10, markeredgewidth=2)
        else:
            # Multiple pole - use circled X
            self.ax.plot(x, y, 'x', color=color, markersize=10, markeredgewidth=2)
            circle = Circle((x, y), 0.15, fill=False, color=color, linewidth=2)
            self.ax.add_patch(circle)
        
        if label:
            self.ax.annotate(label, (x, y), xytext=(5, 5), textcoords='offset points', fontsize=10)
    
    def add_zero(self, z, order=1, label=None, color='blue'):
        """Add a zero to the diagram."""
        x, y = z.real, z.imag
        if order == 1:
            # Simple zero - use O
            circle = Circle((x, y), 0.1, fill=False, color=color, linewidth=2)
            self.ax.add_patch(circle)
        else:
            # Multiple zero - use filled circle
            circle = Circle((x, y), 0.1, fill=True, color=color)
            self.ax.add_patch(circle)
        
        if label:
            self.ax.annotate(label, (x, y), xytext=(5, 5), textcoords='offset points', fontsize=10)
    
    def add_circular_contour(self, center=0+0j, radius=1, label=None, color='green', 
                           style='solid', arrows=True, direction='ccw'):
        """Add a circular contour."""
        theta = np.linspace(0, 2*np.pi, 200)
        if direction == 'cw':
            theta = theta[::-1]
        
        x = center.real + radius * np.cos(theta)
        y = center.imag + radius * np.sin(theta)
        
        line, = self.ax.plot(x, y, color=color, linewidth=2, linestyle=style)
        
        if arrows:
            # Add arrows to show direction
            for i in [50, 100, 150]:
                dx = x[i+1] - x[i]
                dy = y[i+1] - y[i]
                self.ax.arrow(x[i], y[i], dx*5, dy*5, head_width=0.1, 
                            head_length=0.05, fc=color, ec=color)
        
        if label:
            self.ax.text(center.real + radius*1.2, center.imag, label, fontsize=12, color=color)
        
        return line
    
    def add_line_segment(self, z1, z2, label=None, color='green', style='solid', arrows=True):
        """Add a straight line segment contour."""
        x = [z1.real, z2.real]
        y = [z1.imag, z2.imag]
        
        line, = self.ax.plot(x, y, color=color, linewidth=2, linestyle=style)
        
        if arrows:
            # Add arrow in the middle
            mid_x = (z1.real + z2.real) / 2
            mid_y = (z1.imag + z2.imag) / 2
            dx = z2.real - z1.real
            dy = z2.imag - z1.imag
            norm = np.sqrt(dx**2 + dy**2)
            self.ax.arrow(mid_x - dx/norm*0.1, mid_y - dy/norm*0.1, 
                        dx/norm*0.2, dy/norm*0.2,
                        head_width=0.1, head_length=0.05, fc=color, ec=color)
        
        if label:
            mid_x = (z1.real + z2.real) / 2
            mid_y = (z1.imag + z2.imag) / 2
            self.ax.text(mid_x, mid_y + 0.2, label, fontsize=12, color=color)
        
        return line
    
    def add_arc_contour(self, center=0+0j, radius=1, start_angle=0, end_angle=np.pi, 
                       label=None, color='green', style='solid', arrows=True):
        """Add an arc contour."""
        theta = np.linspace(start_angle, end_angle, 100)
        x = center.real + radius * np.cos(theta)
        y = center.imag + radius * np.sin(theta)
        
        line, = self.ax.plot(x, y, color=color, linewidth=2, linestyle=style)
        
        if arrows:
            # Add arrows
            for i in [25, 50, 75]:
                if i < len(x) - 1:
                    dx = x[i+1] - x[i]
                    dy = y[i+1] - y[i]
                    self.ax.arrow(x[i], y[i], dx*5, dy*5, head_width=0.1, 
                                head_length=0.05, fc=color, ec=color)
        
        if label:
            mid_angle = (start_angle + end_angle) / 2
            label_x = center.real + radius * 1.2 * np.cos(mid_angle)
            label_y = center.imag + radius * 1.2 * np.sin(mid_angle)
            self.ax.text(label_x, label_y, label, fontsize=12, color=color)
        
        return line
    
    def add_branch_cut(self, z1, z2, label=None, color='black', width=3):
        """Add a branch cut."""
        x = [z1.real, z2.real]
        y = [z1.imag, z2.imag]
        
        # Draw as a thick line with zigzag pattern
        line, = self.ax.plot(x, y, color=color, linewidth=width, linestyle='solid')
        
        # Add small perpendicular lines to indicate branch cut
        dx = z2.real - z1.real
        dy = z2.imag - z1.imag
        length = np.sqrt(dx**2 + dy**2)
        num_marks = int(length * 3)
        
        for i in range(1, num_marks):
            t = i / num_marks
            px = z1.real + t * dx
            py = z1.imag + t * dy
            # Perpendicular direction
            perp_dx = -dy / length * 0.1
            perp_dy = dx / length * 0.1
            self.ax.plot([px - perp_dx, px + perp_dx], 
                        [py - perp_dy, py + perp_dy], 
                        color=color, linewidth=1)
        
        if label:
            mid_x = (z1.real + z2.real) / 2
            mid_y = (z1.imag + z2.imag) / 2
            self.ax.text(mid_x, mid_y + 0.2, label, fontsize=10, color=color)
    
    def add_keyhole_contour(self, center=0+0j, outer_radius=2, inner_radius=0.5, 
                           gap_angle=0.1, color='green'):
        """Add a keyhole contour around a branch point."""
        # Outer circle (most of it)
        theta1 = np.linspace(gap_angle, 2*np.pi - gap_angle, 150)
        x1 = center.real + outer_radius * np.cos(theta1)
        y1 = center.imag + outer_radius * np.sin(theta1)
        self.ax.plot(x1, y1, color=color, linewidth=2)
        
        # Line from outer to inner (top)
        z_outer_top = center + outer_radius * np.exp(1j * gap_angle)
        z_inner_top = center + inner_radius * np.exp(1j * gap_angle)
        self.add_line_segment(z_outer_top, z_inner_top, color=color, arrows=False)
        
        # Inner circle (opposite direction)
        theta2 = np.linspace(gap_angle, 2*np.pi - gap_angle, 150)[::-1]
        x2 = center.real + inner_radius * np.cos(theta2)
        y2 = center.imag + inner_radius * np.sin(theta2)
        self.ax.plot(x2, y2, color=color, linewidth=2)
        
        # Line from inner to outer (bottom)
        z_inner_bottom = center + inner_radius * np.exp(1j * (-gap_angle))
        z_outer_bottom = center + outer_radius * np.exp(1j * (-gap_angle))
        self.add_line_segment(z_inner_bottom, z_outer_bottom, color=color, arrows=False)
        
        # Add direction arrows
        for theta in [np.pi/2, np.pi, 3*np.pi/2]:
            x = center.real + outer_radius * np.cos(theta)
            y = center.imag + outer_radius * np.sin(theta)
            dx = -outer_radius * np.sin(theta) * 0.1
            dy = outer_radius * np.cos(theta) * 0.1
            self.ax.arrow(x, y, dx, dy, head_width=0.1, head_length=0.05, 
                        fc=color, ec=color)
    
    def add_rectangular_contour(self, corners, label=None, color='green', arrows=True):
        """Add a rectangular contour given the four corners."""
        x = [c.real for c in corners] + [corners[0].real]
        y = [c.imag for c in corners] + [corners[0].imag]
        
        line, = self.ax.plot(x, y, color=color, linewidth=2)
        
        if arrows:
            # Add arrows on each side
            for i in range(len(corners)):
                z1 = corners[i]
                z2 = corners[(i+1) % len(corners)]
                mid_x = (z1.real + z2.real) / 2
                mid_y = (z1.imag + z2.imag) / 2
                dx = z2.real - z1.real
                dy = z2.imag - z1.imag
                norm = np.sqrt(dx**2 + dy**2)
                if norm > 0:
                    self.ax.arrow(mid_x - dx/norm*0.1, mid_y - dy/norm*0.1, 
                                dx/norm*0.2, dy/norm*0.2,
                                head_width=0.1, head_length=0.05, fc=color, ec=color)
        
        if label:
            center_x = sum(c.real for c in corners) / len(corners)
            center_y = sum(c.imag for c in corners) / len(corners)
            self.ax.text(center_x, center_y, label, fontsize=12, color=color, 
                        ha='center', va='center')
    
    def add_indented_contour(self, path_points, pole, indent_radius=0.3, color='green'):
        """Add a contour that indents around a pole."""
        # This creates a semicircular indent around the pole
        result_path = []
        
        for i in range(len(path_points) - 1):
            z1 = path_points[i]
            z2 = path_points[i + 1]
            
            # Check if the line segment passes near the pole
            # (Simplified check - in practice you'd want more sophisticated logic)
            dist_to_pole = abs((z1 + z2)/2 - pole)
            
            if dist_to_pole < indent_radius * 2:
                # Create indent
                # Find the angle of the indent
                angle = np.angle(pole - z1)
                start_angle = angle - np.pi/2
                end_angle = angle + np.pi/2
                
                # Add arc
                theta = np.linspace(start_angle, end_angle, 30)
                for t in theta:
                    indent_point = pole + indent_radius * np.exp(1j * t)
                    result_path.append(indent_point)
            else:
                # Normal line segment
                if i == 0 or dist_to_pole >= indent_radius * 2:
                    result_path.append(z1)
                if i == len(path_points) - 2:
                    result_path.append(z2)
        
        # Plot the path
        x = [p.real for p in result_path]
        y = [p.imag for p in result_path]
        self.ax.plot(x, y, color=color, linewidth=2)
        
        # Add arrows
        for i in range(0, len(result_path) - 1, len(result_path)//4):
            if i < len(result_path) - 1:
                dx = result_path[i+1].real - result_path[i].real
                dy = result_path[i+1].imag - result_path[i].imag
                self.ax.arrow(result_path[i].real, result_path[i].imag, 
                            dx*5, dy*5, head_width=0.1, head_length=0.05, 
                            fc=color, ec=color)
    
    def add_infinity_contour(self, color='green', label='R→∞'):
        """Add a contour at infinity (represented as a large circle)."""
        radius = max(abs(self.ax.get_xlim()[1]), abs(self.ax.get_ylim()[1])) * 0.9
        self.add_circular_contour(center=0+0j, radius=radius, color=color, 
                                style='dashed', label=label)
    
    def set_title(self, title):
        """Set the plot title."""
        self.ax.set_title(title, fontsize=14, pad=20)
    
    def add_text(self, z, text, **kwargs):
        """Add text at a specific complex position."""
        self.ax.text(z.real, z.imag, text, **kwargs)
    
    def show(self):
        """Display the plot."""
        plt.tight_layout()
        plt.show()
    
    def save(self, filename, dpi=150):
        """Save the plot to a file."""
        plt.tight_layout()
        plt.savefig(filename, dpi=dpi, bbox_inches='tight')


# Example usage demonstrating various contour integrals
if __name__ == "__main__":
    # Example 1: Simple contour around poles
    plotter = ContourIntegralPlotter(xlim=(-3, 3), ylim=(-3, 3))
    plotter.set_title(r"$\oint_C \frac{1}{z^2 - 1} dz$")
    
    # Add poles
    plotter.add_pole(1+0j, label='z=1')
    plotter.add_pole(-1+0j, label='z=-1')
    
    # Add contour
    plotter.add_circular_contour(center=0+0j, radius=2, label='C')
    
    plotter.show()
    
    # Example 2: Keyhole contour
    plotter2 = ContourIntegralPlotter(xlim=(-3, 3), ylim=(-3, 3))
    plotter2.set_title("Keyhole Contour for Branch Cut")
    
    # Add branch point and cut
    plotter2.add_pole(0+0j, label='Branch point')
    plotter2.add_branch_cut(0+0j, 3+0j, label='Branch cut')
    
    # Add keyhole contour
    plotter2.add_keyhole_contour(center=0+0j, outer_radius=2, inner_radius=0.3)
    
    plotter2.show()
    
    # Example 3: Rectangular contour
    plotter3 = ContourIntegralPlotter(xlim=(-4, 4), ylim=(-3, 3))
    plotter3.set_title("Rectangular Contour with Multiple Poles")
    
    # Add poles and zeros
    plotter3.add_pole(1+1j, label='Pole')
    plotter3.add_pole(-1+0.5j)
    plotter3.add_zero(0+1.5j, label='Zero')
    
    # Add rectangular contour
    corners = [-3-2j, 3-2j, 3+2j, -3+2j]
    plotter3.add_rectangular_contour(corners, label='Γ')
    
    plotter3.show()