import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Button, Slider, TextBox
import matplotlib.patches as patches

class ChaikinVisualizer:
    def __init__(self):
        self.vertices = []
        self.previous_vertices = None
        self.u = 0.25
        self.v = 0.25
        self.current_iteration = 0
        self.is_closed = False
        self.setup_plot()
        
    def setup_plot(self):
        self.fig, self.ax = plt.subplots(figsize=(10, 8))
        plt.subplots_adjust(bottom=0.25)
        
        # Setup the main plotting area with larger limits
        self.ax.set_xlim(-20, 20)
        self.ax.set_ylim(-20, 20)
        self.ax.set_aspect('equal')
        self.ax.grid(True, linestyle='-', alpha=0.3)
        
        # Add sliders for u and v
        ax_u = plt.axes([0.2, 0.1, 0.3, 0.03])
        ax_v = plt.axes([0.2, 0.05, 0.3, 0.03])
        self.u_slider = Slider(ax_u, 'u', 0, 0.5, valinit=0.25)
        self.v_slider = Slider(ax_v, 'v', 0, 0.5, valinit=0.25)
        
        # Add text boxes for u and v
        ax_u_text = plt.axes([0.55, 0.1, 0.05, 0.03])
        ax_v_text = plt.axes([0.55, 0.05, 0.05, 0.03])
        self.u_textbox = TextBox(ax_u_text, '', initial=str(self.u))
        self.v_textbox = TextBox(ax_v_text, '', initial=str(self.v))
        
        # Add buttons
        ax_reset = plt.axes([0.65, 0.1, 0.1, 0.04])
        ax_iterate = plt.axes([0.75, 0.1, 0.1, 0.04])
        ax_clear = plt.axes([0.85, 0.1, 0.1, 0.04])
        ax_toggle = plt.axes([0.65, 0.05, 0.2, 0.04])
        
        self.btn_reset = Button(ax_reset, 'Reset')
        self.btn_iterate = Button(ax_iterate, 'Iterate')
        self.btn_clear = Button(ax_clear, 'Clear')
        self.btn_toggle = Button(ax_toggle, 'Toggle Open/Closed')
        
        # Add status text at the bottom
        self.status_text = plt.figtext(0.02, 0.02, '', fontsize=10)
        
        # Connect events
        self.fig.canvas.mpl_connect('button_press_event', self.on_click)
        self.btn_reset.on_clicked(self.reset)
        self.btn_iterate.on_clicked(self.iterate)
        self.btn_clear.on_clicked(self.clear)
        self.btn_toggle.on_clicked(self.toggle_closed)
        self.u_slider.on_changed(self.update_params_from_slider)
        self.v_slider.on_changed(self.update_params_from_slider)
        self.u_textbox.on_submit(self.update_params_from_textbox)
        self.v_textbox.on_submit(self.update_params_from_textbox)
        
        self.update_status_text()
        #plt.title("Click to add vertices. Press 'Iterate' to apply corner cutting.")
        
    def update_status_text(self):
        curve_type = "CLOSED" if self.is_closed else "OPEN"
        status = f"Curve Type: {curve_type} | Iteration: {self.current_iteration}"
        self.status_text.set_text(status)
        
    def update_params_from_slider(self, val):
        if val == self.u_slider.val:
            self.u = val
            self.u_textbox.set_val(f"{val:.3f}")
        else:
            self.v = val
            self.v_textbox.set_val(f"{val:.3f}")
            
        self.enforce_constraints()
        
    def update_params_from_textbox(self, text):
        try:
            if text == self.u_textbox.text:
                self.u = float(text)
                self.u_slider.set_val(self.u)
            else:
                self.v = float(text)
                self.v_slider.set_val(self.v)
                
            self.enforce_constraints()
        except ValueError:
            # If invalid input, reset to current slider value
            self.u_textbox.set_val(f"{self.u:.3f}")
            self.v_textbox.set_val(f"{self.v:.3f}")
            
    def enforce_constraints(self):
        # Ensure u and v are within valid ranges and u + v ≤ 1
        self.u = max(0, min(0.5, self.u))
        self.v = max(0, min(0.5, self.v))
        
        if self.u + self.v > 1:
            self.v = 1 - self.u
            self.v_slider.set_val(self.v)
            self.v_textbox.set_val(f"{self.v:.3f}")
        
    def toggle_closed(self, event):
        self.is_closed = not self.is_closed
        self.draw_shape()
        
    def on_click(self, event):
        if event.inaxes == self.ax and event.button == 1:
            self.vertices.append([event.xdata, event.ydata])
            self.draw_shape()
            
    def draw_shape(self):
        self.ax.clear()
        self.ax.set_xlim(-20, 20)
        self.ax.set_ylim(-20, 20)
        #self.ax.set_xticks([])
        #self.ax.set_yticks([])
        self.ax.grid(True, linestyle='-', alpha=0.3)
        
        # Draw previous shape if it exists
        if self.previous_vertices is not None and len(self.previous_vertices) > 0:
            prev_vertices = np.array(self.previous_vertices)
            if len(prev_vertices) >= 2:
                if self.is_closed:
                    prev_vertices_to_plot = np.vstack((prev_vertices, prev_vertices[0]))
                else:
                    prev_vertices_to_plot = prev_vertices
                self.ax.plot(prev_vertices_to_plot[:, 0], prev_vertices_to_plot[:, 1], 'b-', alpha=0.3)
        
        # Draw current shape
        if len(self.vertices) > 0:
            vertices = np.array(self.vertices)
            
            # Draw the lines
            if len(vertices) >= 2:
                if self.is_closed:
                    vertices_to_plot = np.vstack((vertices, vertices[0]))
                else:
                    vertices_to_plot = vertices
                    
                self.ax.plot(vertices_to_plot[:, 0], vertices_to_plot[:, 1], 'b-', linewidth=2)
        
        self.update_status_text()
        plt.draw()
        
    def chaikin_iteration(self, points):
        if len(points) < 2:
            return points
            
        new_points = []
        n = len(points)
        
        if self.is_closed:
            points = np.vstack((points, points[0]))
            n_iterations = n
        else:
            n_iterations = n - 1
            
        # First point for open curves
        if not self.is_closed:
            new_points.append(points[0])
            
        # Generate new points
        for i in range(n_iterations):
            p0 = points[i]
            p1 = points[i + 1]
            
            q = p0 + self.u * (p1 - p0)
            r = p0 + (1 - self.v) * (p1 - p0)
            
            new_points.extend([q, r])
            
        # Last point for open curves
        if not self.is_closed:
            new_points.append(points[-1])
            
        return np.array(new_points)
        
    def iterate(self, event):
        if len(self.vertices) < 2:
            plt.title("Need at least 2 points to apply corner cutting!")
            return
            
        # Store current vertices as previous
        self.previous_vertices = self.vertices.copy()
        
        points = np.array(self.vertices)
        new_points = self.chaikin_iteration(points)
        self.vertices = new_points.tolist()
        self.current_iteration += 1
        self.draw_shape()
        
    def reset(self, event):
        self.current_iteration = 0
        self.vertices = []
        self.previous_vertices = None
        self.draw_shape()
        
    def clear(self, event):
        self.vertices = []
        self.current_iteration = 0
        self.previous_vertices = None
        self.draw_shape()

if __name__ == "__main__":
    visualizer = ChaikinVisualizer()
    plt.show()