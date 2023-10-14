import sys
#import numpy as np
from PyQt6 import QtWidgets, uic, QtCore
from PyQt6.QtCore import Qt
#from matplotlib.figure import Figure
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qtagg import FigureCanvas
#from matplotlib.ticker import ScalarFormatter





### ADD ALPHA AND MARKER SETTINGS FOR THE PLOTS
### FIX THE LEGEND ERROR WHEN PLOTTING BOTH SCATTER AND LINE PLOTS AND IT MAKING TWO LEGEND ENTRIES, PERHAPS HAVE ONE SINGLE COLOUR SELECTOR FOR BOTH AND THEN JUST HAVE A COLOUR LEGEND 

# SETTING DEFAULTS
x_data_1_str = ""
x_data_2_str = ""
x_data_3_str = ""
x_data_4_str = ""
y_data_1_str = ""
y_data_2_str = ""
y_data_3_str = ""
y_data_4_str = ""
x_data_1 = [float(x) for x in x_data_1_str.split(',') if x.strip()]
x_data_2 = [float(x) for x in x_data_2_str.split(',') if x.strip()]
x_data_3 = [float(x) for x in x_data_3_str.split(',') if x.strip()]
x_data_4 = [float(x) for x in x_data_4_str.split(',') if x.strip()]
y_data_1 = [float(y) for y in y_data_1_str.split(',') if y.strip()]
y_data_2 = [float(y) for y in y_data_2_str.split(',') if y.strip()]
y_data_3 = [float(y) for y in y_data_3_str.split(',') if y.strip()]
y_data_4 = [float(y) for y in y_data_4_str.split(',') if y.strip()]
legend_label_1 = ""
legend_label_2 = ""
legend_label_3 = ""
legend_label_4 = ""

x_label = ""
y_label = ""
plot_title = ""

x_lim = [0, 1]
y_lim = [0, 1]

x_lim_str = ""
y_lim_str = ""

grid_enabled = True
grid_alpha = 0.5

scatter_enabled_1 = True
scatter_enabled_2 = True
scatter_enabled_3 = True
scatter_enabled_4 = True

line_enabled_1 = True
line_enabled_2 = True
line_enabled_3 = True
line_enabled_4 = True

scatter_color_1 = 'blue'
scatter_color_2 = 'purple'
scatter_color_3 = 'green'
scatter_color_4 = 'red'

line_color_1 = 'blue'
line_color_2 = 'purple'
line_color_3 = 'green'
line_color_4 = 'red'

# CREATING APP
Form, Window = uic.loadUiType("SimpleGraph3.ui")
app = QtWidgets.QApplication([])

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Audiophile Crossovers V1.0.0")
        self.form = Form()
        self.form.setupUi(self)

    def init_plot(self, x_data_1, y_data_1, legend_label_1, x_label, y_label, plot_title, x_lim, y_lim, grid_enabled, grid_alpha, scatter_enabled_1, line_enabled_1, scatter_color_1, line_color_1):
        
        # Access the 'frame' widget from your UI
        frame_widget = self.form.plot_frame

        # Create a Matplotlib figure and add a subplot to it
        self.figure, ax = plt.subplots()


        self.x_data_1 = x_data_1
        self.x_data_2 = x_data_2
        self.x_data_3 = x_data_3
        self.x_data_4 = x_data_4

        self.y_data_1 = y_data_1
        self.y_data_2 = y_data_2
        self.y_data_3 = y_data_3
        self.y_data_4 = y_data_4

        self.legend_label_1 = legend_label_1
        self.legend_label_2 = legend_label_2
        self.legend_label_3 = legend_label_3
        self.legend_label_4 = legend_label_4
        
        self.x_label = x_label
        self.y_label = y_label
        self.plot_title = plot_title
        self.x_lim = x_lim
        self.y_lim = y_lim
        self.grid_enabled = grid_enabled
        self.grid_alpha = grid_alpha
        self.scatter_enabled_1 = scatter_enabled_1
        self.scatter_enabled_2 = scatter_enabled_2
        self.scatter_enabled_3 = scatter_enabled_3
        self.scatter_enabled_4 = scatter_enabled_4

        self.line_enabled_1 = line_enabled_1
        self.line_enabled_2 = line_enabled_2
        self.line_enabled_3 = line_enabled_3
        self.line_enabled_4 = line_enabled_4
        
        self.scatter_color_1 = scatter_color_1
        self.scatter_color_2 = scatter_color_2
        self.scatter_color_3 = scatter_color_3
        self.scatter_color_4 = scatter_color_4
        
        self.line_color_1 = line_color_1
        self.line_color_2 = line_color_2
        self.line_color_3 = line_color_3
        self.line_color_4 = line_color_4

        self.ax = ax
        # Create a canvas widget to display the Matplotlib figure
        self.canvas = FigureCanvas(self.figure)
        layout = QtWidgets.QVBoxLayout(frame_widget)
        layout.addWidget(self.canvas)
        
        
        self.update_plot() # call update_plot to plot the default values set in the backend

    def toggle_pin_to_top(self, checked):
        if checked:
            self.setWindowFlag(Qt.WindowType.WindowStaysOnTopHint)
        else:
            self.setWindowFlag(Qt.WindowType.WindowStaysOnTopHint, False)
        self.show()

    def show_grid_changed(self, checked):
        if checked:
            self.grid_enabled = True
        else:
            self.grid_enabled = False
        self.update_plot()

    def grid_alpha_changed(self, value):
        global grid_alpha
        grid_alpha = value / 100
        self.update_plot()

    def show_scatter_changed_1(self, checked):
        if checked:
            self.scatter_enabled_1 = True
        else:
            self.scatter_enabled_1 = False
        self.update_plot()

    def show_scatter_changed_2(self, checked):
        if checked:
            self.scatter_enabled_2 = True
        else:
            self.scatter_enabled_2 = False
        self.update_plot()
    
    def show_scatter_changed_3(self, checked):
        if checked:
            self.scatter_enabled_3 = True
        else:
            self.scatter_enabled_3 = False
        self.update_plot()
    
    def show_scatter_changed_4(self, checked):
        if checked:
            self.scatter_enabled_4 = True
        else:
            self.scatter_enabled_4 = False
        self.update_plot()




    def show_line_changed_1(self, checked):
        if checked:
            self.line_enabled_1 = True
        else:
            self.line_enabled_1 = False
        self.update_plot()

    def show_line_changed_2(self, checked):
        if checked:
            self.line_enabled_2 = True
        else:
            self.line_enabled_2 = False
        self.update_plot()

    def show_line_changed_3(self, checked):
        if checked:
            self.line_enabled_3 = True
        else:
            self.line_enabled_3 = False
        self.update_plot()

    def show_line_changed_4(self, checked):
        if checked:
            self.line_enabled_4 = True
        else:
            self.line_enabled_4 = False
        self.update_plot()

    




    def scatter_color_1_changed(self, color):
        self.scatter_color_1 = color
        self.update_plot()

    def scatter_color_2_changed(self, color):
        self.scatter_color_2 = color
        self.update_plot()
    
    def scatter_color_3_changed(self, color):
        self.scatter_color_3 = color
        self.update_plot()
    
    def scatter_color_4_changed(self, color):
        self.scatter_color_4 = color
        self.update_plot()




    def line_color_1_changed(self, color):
        self.line_color_1 = color
        self.update_plot()

    def line_color_2_changed(self, color):
        self.line_color_2 = color
        self.update_plot()
    
    def line_color_3_changed(self, color):
        self.line_color_3 = color
        self.update_plot()
    
    def line_color_4_changed(self, color):
        self.line_color_4 = color
        self.update_plot()





    def save_plot(self):
        file_path, _ = QtWidgets.QFileDialog.getSaveFileName(self, "Save Plot", "", "PNG files (*.png);;All files (*)")
        if file_path:
            self.figure.savefig(file_path, dpi=100)

    def define_x_lim(self):
        x_lim_str = self.form.x_limits_input.text()
        if x_lim_str.strip():
            self.x_lim = list(map(float, x_lim_str.split(',')))
        else:
            # Check if any of the text fields have data
            if self.x_data_1 or self.x_data_2 or self.x_data_3 or self.x_data_4:
                x_ranges = []
                x_mins = []
                x_maxs = []

                if self.x_data_1:
                    x_ranges.append(max(self.x_data_1) - min(self.x_data_1))
                    x_mins.append(min(self.x_data_1))
                    x_maxs.append(max(self.x_data_1))
                
                if self.x_data_2:
                    x_ranges.append(max(self.x_data_2) - min(self.x_data_2))
                    x_mins.append(min(self.x_data_2))
                    x_maxs.append(max(self.x_data_2))
                
                if self.x_data_3:
                    x_ranges.append(max(self.x_data_3) - min(self.x_data_3))
                    x_mins.append(min(self.x_data_3))
                    x_maxs.append(max(self.x_data_3))
                
                if self.x_data_4:
                    x_ranges.append(max(self.x_data_4) - min(self.x_data_4))
                    x_mins.append(min(self.x_data_4))
                    x_maxs.append(max(self.x_data_4))
                
                x_range = max(x_ranges)
                x_min = min(x_mins)
                x_max = max(x_maxs)

                self.x_lim = [x_min - 0.05 * x_range, x_max + 0.05 * x_range]

            else:
                self.x_lim = [0, 1]
        self.update_plot()

    def define_y_lim(self):
        y_lim_str = self.form.y_limits_input.text()
        if y_lim_str.strip(): # user has eneterd values in the y lim box
            self.y_lim = list(map(float, y_lim_str.split(',')))

        else: 
            # Check if any of the text fields have data
            if self.y_data_1 or self.y_data_2 or self.y_data_3 or self.y_data_4:
                y_ranges = []
                y_mins = []
                y_maxs = []

                if self.y_data_1:
                    y_ranges.append(max(self.y_data_1) - min(self.y_data_1))
                    y_mins.append(min(self.y_data_1))
                    y_maxs.append(max(self.y_data_1))
                
                if self.y_data_2:
                    y_ranges.append(max(self.y_data_2) - min(self.y_data_2))
                    y_mins.append(min(self.y_data_2))
                    y_maxs.append(max(self.y_data_2)),
                
                if self.y_data_3:
                    y_ranges.append(max(self.y_data_3) - min(self.y_data_3))
                    y_mins.append(min(self.y_data_3))
                    y_maxs.append(max(self.y_data_3))
                
                if self.y_data_4:
                    y_ranges.append(max(self.y_data_4) - min(self.y_data_4))
                    y_mins.append(min(self.y_data_4))
                    y_maxs.append(max(self.y_data_4))
                
                y_range = max(y_ranges)
                y_min = min(y_mins)
                y_max = max(y_maxs)

                self.y_lim = [y_min - 0.05 * y_range, y_max + 0.05 * y_range]
                
            else:            # user has not entered values in the y lim box or the y data box so set to default 0 - 1 limits
                self.y_lim = [0, 1]

        self.update_plot()

    def update_x_data_1(self):
        x_data_1_str = self.form.x_data_input_1.text()
        try:
            self.x_data_1 = [float(x) for x in x_data_1_str.split(',') if x.strip()]
            self.define_x_lim()
        except ValueError:   # protection from user entering illigal charecters in the data box. i.e anytihg other than numbers, spaces or commas. 
            pass

    def update_y_data_1(self):
        y_data_1_str = self.form.y_data_input_1.text()
        try:
            self.y_data_1 = [float(y) for y in y_data_1_str.split(',') if y.strip()]
            self.define_y_lim()
        except ValueError:
            pass

    def update_x_data_2(self):
        x_data_2_str = self.form.x_data_input_2.text()
        try:
            self.x_data_2 = [float(x) for x in x_data_2_str.split(',') if x.strip()]
            self.define_x_lim()
        except ValueError:
            pass

    def update_y_data_2(self):
        y_data_2_str = self.form.y_data_input_2.text()
        try:
            self.y_data_2 = [float(y) for y in y_data_2_str.split(',') if y.strip()]
            self.define_y_lim()
        except ValueError:
            pass

    def update_x_data_3(self):
        x_data_3_str = self.form.x_data_input_3.text()
        try:
            self.x_data_3 = [float(x) for x in x_data_3_str.split(',') if x.strip()]
            self.define_x_lim()
        except ValueError:
            pass

    def update_y_data_3(self):
        y_data_3_str = self.form.y_data_input_3.text()
        try:
            self.y_data_3 = [float(y) for y in y_data_3_str.split(',') if y.strip()]
            self.define_y_lim()
        except ValueError:
            pass

    def update_x_data_4(self):
        x_data_4_str = self.form.x_data_input_4.text()
        try:
            self.x_data_4 = [float(x) for x in x_data_4_str.split(',') if x.strip()]
            self.define_x_lim()
        except ValueError:
            pass

    def update_y_data_4(self):
        y_data_4_str = self.form.y_data_input_4.text()
        try:
            self.y_data_4 = [float(y) for y in y_data_4_str.split(',') if y.strip()]
            self.define_y_lim()
        except ValueError:
            pass
        
    def update_legend_label_1(self):
        self.legend_label_1 = self.form.data_label_1.text()
        self.update_plot()

    def update_legend_label_2(self):
        self.legend_label_2 = self.form.data_label_2.text()
        self.update_plot()
    
    def update_legend_label_3(self):
        self.legend_label_3 = self.form.data_label_3.text()
        self.update_plot()

    def update_legend_label_4(self):
        self.legend_label_4 = self.form.data_label_4.text()
        self.update_plot()



    def update_x_label(self):
        self.x_label = self.form.x_label_input.text()
        self.update_plot()

    def update_y_label(self):
        self.y_label = self.form.y_label_input.text()
        self.update_plot()

    def update_plot_title(self):
        self.plot_title = self.form.plot_title_input.text()
        self.update_plot()

    




    def update_plot(self):
        try:
            self.ax.clear()

            if self.scatter_enabled_1:
                self.ax.scatter(self.x_data_1, self.y_data_1, label=self.legend_label_1, c=self.scatter_color_1, alpha=0.6, marker='x')
            if self.scatter_enabled_2:
                self.ax.scatter(self.x_data_2, self.y_data_2, label=self.legend_label_2, c=self.scatter_color_2, alpha=0.6, marker='x')
            if self.scatter_enabled_3:
                self.ax.scatter(self.x_data_3, self.y_data_3, label=self.legend_label_3, c=self.scatter_color_3, alpha=0.6, marker='x')
            if self.scatter_enabled_4:
                self.ax.scatter(self.x_data_4, self.y_data_4, label=self.legend_label_4, c=self.scatter_color_4, alpha=0.6, marker='x')


            if self.line_enabled_1:
                self.ax.plot(self.x_data_1, self.y_data_1, label=self.legend_label_1, color=self.line_color_1, alpha=0.6)
            if self.line_enabled_2:
                self.ax.plot(self.x_data_2, self.y_data_2, label=self.legend_label_2, color=self.line_color_2, alpha=0.6)
            if self.line_enabled_3:
                self.ax.plot(self.x_data_3, self.y_data_3, label=self.legend_label_3, color=self.line_color_3, alpha=0.6)
            if self.line_enabled_4:
                self.ax.plot(self.x_data_4, self.y_data_4, label=self.legend_label_4, color=self.line_color_4, alpha=0.6)




            self.ax.set_xlabel(self.x_label)
            self.ax.set_ylabel(self.y_label)
            self.ax.set_title(self.plot_title)
            self.ax.set_xlim(self.x_lim)
            self.ax.set_ylim(self.y_lim)

            if self.grid_enabled:
                self.ax.grid(alpha=grid_alpha)

            # add check if any of the data labels is filled in by user if not ignore plotting legend to stop the legend error
            self.ax.legend()
            self.canvas.draw()
        
        # if exception is ValueError("x and y must be the same size") then user has finished entering data in either the x or y box and has not yet finshed entering data in the other box so ignore error and continue loop
        except ValueError:
            pass


window = MainWindow()
window.show()

window.init_plot(x_data_1, y_data_1, legend_label_1, x_label, y_label, plot_title, x_lim, y_lim, grid_enabled, grid_alpha, scatter_enabled_1, line_enabled_1, scatter_color_1, line_color_1)

# Connect signals to slots for various controls
window.form.showgrid_checkbox.stateChanged.connect(window.show_grid_changed)
window.form.grid_alpha_slider.valueChanged.connect(window.grid_alpha_changed)

window.form.showscatter_checkbox_1.stateChanged.connect(window.show_scatter_changed_1)
window.form.scatter_color_input_1.currentTextChanged.connect(window.scatter_color_1_changed)
window.form.showline_checkbox_1.stateChanged.connect(window.show_line_changed_1)
window.form.line_color_input_1.currentTextChanged.connect(window.line_color_1_changed)

window.form.showscatter_checkbox_2.stateChanged.connect(window.show_scatter_changed_2)
window.form.scatter_color_input_2.currentTextChanged.connect(window.scatter_color_2_changed)
window.form.showline_checkbox_2.stateChanged.connect(window.show_line_changed_2)
window.form.line_color_input_2.currentTextChanged.connect(window.line_color_2_changed)

window.form.showscatter_checkbox_3.stateChanged.connect(window.show_scatter_changed_3)
window.form.scatter_color_input_3.currentTextChanged.connect(window.scatter_color_3_changed)
window.form.showline_checkbox_3.stateChanged.connect(window.show_line_changed_3)
window.form.line_color_input_3.currentTextChanged.connect(window.line_color_3_changed)

window.form.showscatter_checkbox_4.stateChanged.connect(window.show_scatter_changed_4)
window.form.scatter_color_input_4.currentTextChanged.connect(window.scatter_color_4_changed)
window.form.showline_checkbox_4.stateChanged.connect(window.show_line_changed_4)
window.form.line_color_input_4.currentTextChanged.connect(window.line_color_4_changed)














window.form.saveplot_button.clicked.connect(window.save_plot)
window.form.pingui_checkbox.stateChanged.connect(window.toggle_pin_to_top)

window.form.x_data_input_1.editingFinished.connect(window.update_x_data_1)
window.form.x_data_input_2.editingFinished.connect(window.update_x_data_2)
window.form.x_data_input_3.editingFinished.connect(window.update_x_data_3)
window.form.x_data_input_4.editingFinished.connect(window.update_x_data_4)

window.form.y_data_input_1.editingFinished.connect(window.update_y_data_1)
window.form.y_data_input_2.editingFinished.connect(window.update_y_data_2)
window.form.y_data_input_3.editingFinished.connect(window.update_y_data_3)
window.form.y_data_input_4.editingFinished.connect(window.update_y_data_4)

window.form.data_label_1.editingFinished.connect(window.update_legend_label_1)
window.form.data_label_2.editingFinished.connect(window.update_legend_label_2)
window.form.data_label_3.editingFinished.connect(window.update_legend_label_3)
window.form.data_label_4.editingFinished.connect(window.update_legend_label_4)


window.form.plot_title_input.editingFinished.connect(window.update_plot_title)
window.form.x_label_input.editingFinished.connect(window.update_x_label)
window.form.y_label_input.editingFinished.connect(window.update_y_label)

window.form.x_limits_input.editingFinished.connect(window.define_x_lim)
window.form.y_limits_input.editingFinished.connect(window.define_y_lim)




# setting defulats for backend 


# Set default value for the "Pin GUI to Top" checkbox
window.form.pingui_checkbox.setChecked(True)  # Set to True if you want it checked by default




sys.exit(app.exec())
