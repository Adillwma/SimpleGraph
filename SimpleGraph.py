# SimpleGraph - Simple Windows GUI to create publication ready plots, with no code needed.
# Author: Adill Al-Ashgar

### Improvements to make:
### SIMPLIFY THE SAVING OF THE TEXT FILE WITH RAW DATA TO USE THE NEW LOOPING CODE 
### MAKE SURE FILE SAVE DIALOG GOES TO LAST SAVED IN DIRECTORY FROM THE PROGRAM TO SAAVE USER HUNTING FOR DIR EACH TME
### Offer user checkbox for legend on plot or to side of plot
### Adjust plot save quality with either plot size or dpi ??
### IMPORTANT!!! _ FIX bug where program crashes if user enters text into the limits fileds, also check all fiels for entry of wrong types and add protections

#%% - Dependencies
import sys
import matplotlib.pyplot as plt
from PyQt6.QtCore import Qt
from PyQt6 import QtWidgets, uic
from matplotlib.backends.backend_qtagg import FigureCanvas
import numpy as np
from scipy.stats import linregress 
from scipy.optimize import curve_fit
import pyi_splash

# Close the splash screen. It does not matter when the call
# to this function is made, the splash screen remains open until
# this function is called or the Python program is terminated.
pyi_splash.close()

def fit_data(x, y, fit_selection, num_points=100):
    # Generate a new range of x-values for the fit line
    x_fit = np.linspace(min(x), max(x), num_points)

    if fit_selection == "Linear":
        slope, intercept, r_value, p_value, std_err = linregress(x, y)
        y_fit = [(slope * xi) + intercept for xi in x_fit]

    elif fit_selection == "Exponential":
        popt, _ = curve_fit(lambda x, a, b: a * np.exp(b * x), x, y)
        y_fit = popt[0] * np.exp(popt[1] * x_fit)

    else: # Fit is polynomial
        # Strip the order of the polynomial from the fit_selection string in form "Polynomial (2nd Order)", "Polynomial (3rd Order)", "Polynomial (4th Order)"
        degree = int(fit_selection.split(" ")[1][1])
        coeffs = np.polyfit(x, y, degree)
        y_fit = np.polyval(coeffs, x_fit)

    return x_fit, y_fit

#%% - SETTING DEFAULTS
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
save_raw_data = True

scatter_enabled_1 = True
scatter_enabled_2 = True
scatter_enabled_3 = True
scatter_enabled_4 = True

line_enabled_1 = True
line_enabled_2 = True
line_enabled_3 = True
line_enabled_4 = True

data_color_1 = 'blue'
data_color_2 = 'purple'
data_color_3 = 'green'
data_color_4 = 'red'

line_color_1 = 'blue'
line_color_2 = 'purple'
line_color_3 = 'green'
line_color_4 = 'red'

#%% - CREATING APP
Form, Window = uic.loadUiType("SimpleGraph3.ui")
app = QtWidgets.QApplication([])

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Audiophile Crossovers V1.0.0")
        self.form = Form()
        self.form.setupUi(self)

    def init_plot(self, x_data_1, y_data_1, legend_label_1, x_label, y_label, plot_title, x_lim, y_lim, grid_enabled, grid_alpha, scatter_enabled_1, line_enabled_1, data_color_1, save_raw_data):
        
        self.save_raw_data = save_raw_data

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
        
        self.data_color_1 = data_color_1
        self.data_color_2 = data_color_2
        self.data_color_3 = data_color_3
        self.data_color_4 = data_color_4
    
        self.x_error_1 = []
        self.x_error_2 = []
        self.x_error_3 = []
        self.x_error_4 = []

        self.y_error_1 = []
        self.y_error_2 = []
        self.y_error_3 = []
        self.y_error_4 = []

        self.error_enabled_1 = False
        self.error_enabled_2 = False
        self.error_enabled_3 = False
        self.error_enabled_4 = False

        self.fit_selection_1 = "None"
        self.fit_selection_2 = "None"
        self.fit_selection_3 = "None"
        self.fit_selection_4 = "None"



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

    

    def show_errors_changed_1(self, checked):
        if checked:
            self.error_enabled_1 = True
        else:
            self.error_enabled_1 = False
        self.update_plot()

    def show_errors_changed_2(self, checked):
        if checked:
            self.error_enabled_2 = True
        else:
            self.error_enabled_2 = False
        self.update_plot()

    def show_errors_changed_3(self, checked):
        if checked:
            self.error_enabled_3 = True
        else:
            self.error_enabled_3 = False
        self.update_plot()

    def show_errors_changed_4(self, checked):
        if checked:
            self.error_enabled_4 = True
        else:
            self.error_enabled_4 = False
        self.update_plot()




    def data_color_1_changed(self, color):
        self.data_color_1 = color
        self.update_plot()

    def data_color_2_changed(self, color):
        self.data_color_2 = color
        self.update_plot()
    
    def data_color_3_changed(self, color):
        self.data_color_3 = color
        self.update_plot()
    
    def data_color_4_changed(self, color):
        self.data_color_4 = color
        self.update_plot()




    def save_plot(self):
        file_path, _ = QtWidgets.QFileDialog.getSaveFileName(self, "Save Plot", "", "PNG files (*.png);;All files (*)")
        if file_path:
            self.figure.savefig(file_path, dpi=100)

            if self.save_raw_data:
                # take the file path and remove the file extension and add .txt to the end to create a text file with the same name as the plot file
                raw_data_file_path = file_path[:-4] + ".txt"

                # open the file in write mode and write the raw data to it
                with open(raw_data_file_path, "w") as f:
                    
                    # check if any of the plot titles or axis titles have been changed by the user, if so then write to file
                    if self.plot_title or self.x_label or self.y_label:
                        if self.plot_title:
                            f.write("Plot Title: " + self.plot_title + "\n")
                        if self.x_label:
                            f.write("X Label: " + self.x_label + "\n")
                        if self.y_label:
                            f.write("Y Label: " + self.y_label + "\n")

                        f.write("\n") # add a blank line to the file to seperate the data


                    
                    if self.legend_label_1:                                    # Add data label 1 if exists to the file, if not add a string saying "Data 1" to the file
                        f.write("Data: " + self.legend_label_1 + "\n")
                    else:
                        f.write("Data: Data 1\n")
                    f.write("X Data:" + str(self.x_data_1) + "\n") 
                    f.write("Y Data:" + str(self.y_data_1) + "\n")
                    f.write("X Errors:" + str(self.x_error_1) + "\n")
                    f.write("Y Errors:" + str(self.y_error_1) + "\n")

                    f.write("\n") # add a blank line to the file to seperate the data
                    if self.legend_label_2:                                   # Add data label 2 if exists to the file, if not add a string saying "Data 2" to the file
                        f.write("Data: " + self.legend_label_2 + "\n")
                    else:
                        f.write("Data: Data 2\n")
                    f.write("X Data:" + str(self.x_data_2) + "\n")
                    f.write("Y Data:" + str(self.y_data_2) + "\n")
                    f.write("X Errors:" + str(self.x_error_2) + "\n")
                    f.write("Y Errors:" + str(self.y_error_2) + "\n")

                    f.write("\n") # add a blank line to the file to seperate the data
                    if self.legend_label_3:                                    # Add data label 3 if exists to the file, if not add a string saying "Data 3" to the file
                        f.write("Data: " + self.legend_label_3 + "\n")
                    else:
                        f.write("Data: Data 3\n")
                    f.write("X Data:" + str(self.x_data_3) + "\n")
                    f.write("Y Data:" + str(self.y_data_3) + "\n")
                    f.write("X Errors:" + str(self.x_error_3) + "\n")
                    f.write("Y Errors:" + str(self.y_error_3) + "\n")


                    f.write("\n") # add a blank line to the file to seperate the data
                    if self.legend_label_4:                                # Add data label 4 if exists to the file, if not add a string saying "Data 4" to the file
                        f.write("Data: " + self.legend_label_4 + "\n")
                    else:
                        f.write("Data: Data 4\n")
                    f.write("X Data:" + str(self.x_data_4) + "\n")
                    f.write("Y Data:" + str(self.y_data_4) + "\n")
                    f.write("X Errors:" + str(self.x_error_4) + "\n")
                    f.write("Y Errors:" + str(self.y_error_4) + "\n")


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
            x_data_1_str = x_data_1_str.replace(',', ' ')
            self.x_data_1 = [float(x) for x in x_data_1_str.split() if x.strip()]            
            self.define_x_lim()
        except ValueError:   # protection from user entering illigal charecters in the data box. i.e anytihg other than numbers, spaces or commas. 
            pass

    def update_y_data_1(self):
        y_data_1_str = self.form.y_data_input_1.text()
        try:
            y_data_1_str = y_data_1_str.replace(',', ' ')
            self.y_data_1 = [float(y) for y in y_data_1_str.split() if y.strip()]
            self.define_y_lim()
        except ValueError:
            pass

    def update_x_data_2(self):
        x_data_2_str = self.form.x_data_input_2.text()
        try:
            x_data_2_str = x_data_2_str.replace(',', ' ')
            self.x_data_2 = [float(x) for x in x_data_2_str.split() if x.strip()]
            self.define_x_lim()
        except ValueError:
            pass

    def update_y_data_2(self):
        y_data_2_str = self.form.y_data_input_2.text()
        try:
            y_data_2_str = y_data_2_str.replace(',', ' ')
            self.y_data_2 = [float(y) for y in y_data_2_str.split() if y.strip()]
            self.define_y_lim()
        except ValueError:
            pass

    def update_x_data_3(self):
        x_data_3_str = self.form.x_data_input_3.text()
        try:
            x_data_3_str = x_data_3_str.replace(',', ' ')
            self.x_data_3 = [float(x) for x in x_data_3_str.split() if x.strip()]
            self.define_x_lim()
        except ValueError:
            pass

    def update_y_data_3(self):
        y_data_3_str = self.form.y_data_input_3.text()
        try:
            y_data_3_str = y_data_3_str.replace(',', ' ')
            self.y_data_3 = [float(y) for y in y_data_3_str.split() if y.strip()]
            self.define_y_lim()
        except ValueError:
            pass

    def update_x_data_4(self):
        x_data_4_str = self.form.x_data_input_4.text()
        try:
            x_data_4_str = x_data_4_str.replace(',', ' ')
            self.x_data_4 = [float(x) for x in x_data_4_str.split() if x.strip()]
            self.define_x_lim()
        except ValueError:
            pass

    def update_y_data_4(self):
        y_data_4_str = self.form.y_data_input_4.text()
        try:
            y_data_4_str = y_data_4_str.replace(',', ' ')
            self.y_data_4 = [float(y) for y in y_data_4_str.split() if y.strip()]
            self.define_y_lim()
        except ValueError:
            pass




    def update_x_err_1(self):
        x_err_1_str = self.form.x_error_input_1.text()
        try:
            x_err_1_str = x_err_1_str.replace(',', ' ')
            self.x_error_1 = [float(x) for x in x_err_1_str.split() if x.strip()]
            self.update_plot()
        except ValueError:
            pass

    def update_y_err_1(self):
        y_err_1_str = self.form.y_error_input_1.text()
        try:
            y_err_1_str = y_err_1_str.replace(',', ' ')
            self.y_error_1 = [float(y) for y in y_err_1_str.split() if y.strip()]
            self.update_plot()
        except ValueError:
            pass

    def update_x_err_2(self):
        x_err_2_str = self.form.x_error_input_2.text()
        try:
            x_err_2_str = x_err_2_str.replace(',', ' ')
            self.x_error_2 = [float(x) for x in x_err_2_str.split() if x.strip()]
            self.update_plot()
        except ValueError:
            pass

    def update_y_err_2(self):
        y_err_2_str = self.form.y_error_input_2.text()
        try:
            y_err_2_str = y_err_2_str.replace(',', ' ')
            self.y_error_2 = [float(y) for y in y_err_2_str.split() if y.strip()]
            self.update_plot()
        except ValueError:
            pass

    def update_x_err_3(self):
        x_err_3_str = self.form.x_error_input_3.text()
        try:
            x_err_3_str = x_err_3_str.replace(',', ' ')
            self.x_error_3 = [float(x) for x in x_err_3_str.split() if x.strip()]
            self.update_plot()
        except ValueError:
            pass

    def update_y_err_3(self):
        y_err_3_str = self.form.y_error_input_3.text()
        try:
            y_err_3_str = y_err_3_str.replace(',', ' ')
            self.y_error_3 = [float(y) for y in y_err_3_str.split() if y.strip()]
            self.update_plot()
        except ValueError:
            pass

    def update_x_err_4(self):
        x_err_4_str = self.form.x_error_input_4.text()
        try:
            x_err_4_str = x_err_4_str.replace(',', ' ')
            self.x_error_4 = [float(x) for x in x_err_4_str.split() if x.strip()]
            self.update_plot()
        except ValueError:
            pass

    def update_y_err_4(self):
        y_err_4_str = self.form.y_error_input_4.text()
        try:
            y_err_4_str = y_err_4_str.replace(',', ' ')
            self.y_error_4 = [float(y) for y in y_err_4_str.split() if y.strip()]
            self.update_plot()
        except ValueError:
            pass




    def update_fit_selection_1(self, text):
        self.fit_selection_1 = text
        self.update_plot()

    def update_fit_selection_2(self, text):
        self.fit_selection_2 = text
        self.update_plot()


    def update_fit_selection_3(self, text):
        self.fit_selection_3 = text
        self.update_plot()

    def update_fit_selection_4(self, text):
        self.fit_selection_4 = text
        self.update_plot()





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

    
    def update_save_raw_data(self, checked):
        if checked:
            self.save_raw_data = True
        else:
            self.save_raw_data = False
        self.update_plot()


    def update_plot(self):
        try:
            self.ax.clear()
            if self.scatter_enabled_1:
                self.ax.scatter(self.x_data_1, self.y_data_1, c=self.data_color_1, alpha=0.6, marker='x')
            if self.scatter_enabled_2:
                self.ax.scatter(self.x_data_2, self.y_data_2, c=self.data_color_2, alpha=0.6, marker='x')
            if self.scatter_enabled_3:
                self.ax.scatter(self.x_data_3, self.y_data_3, c=self.data_color_3, alpha=0.6, marker='x')
            if self.scatter_enabled_4:
                self.ax.scatter(self.x_data_4, self.y_data_4, c=self.data_color_4, alpha=0.6, marker='x')


            if self.line_enabled_1:
                self.ax.plot(self.x_data_1, self.y_data_1, color=self.data_color_1, alpha=0.6)
            if self.line_enabled_2:
                self.ax.plot(self.x_data_2, self.y_data_2, color=self.data_color_2, alpha=0.6)
            if self.line_enabled_3:
                self.ax.plot(self.x_data_3, self.y_data_3, color=self.data_color_3, alpha=0.6)
            if self.line_enabled_4:
                self.ax.plot(self.x_data_4, self.y_data_4, color=self.data_color_4, alpha=0.6)


            if self.error_enabled_1:   #COULD MAYBE USE THIS TO ADD THE LINE AND SCATTER PLOTS TOGETHER IN ONE AS THE ERRO RPLOT ALLOS BOTH, BUT WOULD NEED TO BEA BLE TO HIDE THE ERRORS IF SO 
                self.ax.errorbar(self.x_data_1, self.y_data_1, xerr=self.x_error_1, yerr=self.y_error_1, c=self.data_color_1, linestyle='', fmt='', capsize=5, alpha=0.6)
            if self.error_enabled_2:
                self.ax.errorbar(self.x_data_2, self.y_data_2, xerr=self.x_error_2, yerr=self.y_error_2, c=self.data_color_2, linestyle='', fmt='', capsize=5, alpha=0.6)
            if self.error_enabled_3:
                self.ax.errorbar(self.x_data_3, self.y_data_3, xerr=self.x_error_3, yerr=self.y_error_3, c=self.data_color_3, linestyle='', fmt='', capsize=5, alpha=0.6)
            if self.error_enabled_4:
                self.ax.errorbar(self.x_data_4, self.y_data_4, xerr=self.x_error_4, yerr=self.y_error_4, c=self.data_color_4, linestyle='', fmt='', capsize=5, alpha=0.6)



            # Consolidate legend labels for both scatter and line plots into one item in the legend, ALSO ADDING FITS,            
            if self.scatter_enabled_1 or self.line_enabled_1 or self.error_enabled_1:    
                self.ax.plot([], [], 's', color=self.data_color_1, label=self.legend_label_1)

            if self.fit_selection_1 != "None":
                x_fit_1, y_fit_1 = fit_data(self.x_data_1, self.y_data_1, self.fit_selection_1)
                self.ax.plot(x_fit_1, y_fit_1, color=self.data_color_1, linestyle='--', alpha=0.5, label=f"{self.fit_selection_1} Fit")


            if self.scatter_enabled_2 or self.line_enabled_2 or self.error_enabled_2:
                self.ax.plot([], [], 's', color=self.data_color_2, label=self.legend_label_2)

            if self.fit_selection_2 != "None":
                x_fit_2, y_fit_2 = fit_data(self.x_data_2, self.y_data_2, self.fit_selection_2)
                self.ax.plot(x_fit_2, y_fit_2, color=self.data_color_2, linestyle='--', alpha=0.5, label=f"{self.fit_selection_2} Fit")

            if self.scatter_enabled_3 or self.line_enabled_3 or self.error_enabled_3:
                self.ax.plot([], [], 's', color=self.data_color_3, label=self.legend_label_3)

            if self.fit_selection_3 != "None":
                x_fit_3, y_fit_3 = fit_data(self.x_data_3, self.y_data_3, self.fit_selection_3)
                self.ax.plot(x_fit_3, y_fit_3, color=self.data_color_3, linestyle='--', alpha=0.5, label=f"{self.fit_selection_3} Fit")
            
            if self.scatter_enabled_4 or self.line_enabled_4 or self.error_enabled_4:
                self.ax.plot([], [], 's', color=self.data_color_4, label=self.legend_label_4)

            if self.fit_selection_4 != "None":
                x_fit_4, y_fit_4 = fit_data(self.x_data_4, self.y_data_4, self.fit_selection_4)
                self.ax.plot(x_fit_4, y_fit_4, color=self.data_color_4, linestyle='--', alpha=0.5, label=f"{self.fit_selection_4} Fit")




            self.ax.set_xlabel(self.x_label)
            self.ax.set_ylabel(self.y_label)
            self.ax.set_title(self.plot_title)
            self.ax.set_xlim(self.x_lim)
            self.ax.set_ylim(self.y_lim)

            if self.grid_enabled:
                self.ax.grid(alpha=grid_alpha)

            # add check if any of the data labels is filled in by user if not ignore plotting legend to stop the legend error
            self.ax.legend()
            #self.figure.tight_layout()

            self.canvas.draw()
        
        # if exception is ValueError("x and y must be the same size") then user has finished entering data in either the x or y box and has not yet finshed entering data in the other box so ignore error and continue loop
        except ValueError as e:
            print(e)
            pass


#%% - Initialising the app
window = MainWindow()



#%% - Connect signals to slots for various controls
window.form.showgrid_checkbox.stateChanged.connect(window.show_grid_changed)
window.form.grid_alpha_slider.valueChanged.connect(window.grid_alpha_changed)

window.form.showscatter_checkbox_1.stateChanged.connect(window.show_scatter_changed_1)
window.form.data_color_input_1.currentTextChanged.connect(window.data_color_1_changed)
window.form.showline_checkbox_1.stateChanged.connect(window.show_line_changed_1)

window.form.showscatter_checkbox_2.stateChanged.connect(window.show_scatter_changed_2)
window.form.data_color_input_2.currentTextChanged.connect(window.data_color_2_changed)
window.form.showline_checkbox_2.stateChanged.connect(window.show_line_changed_2)

window.form.showscatter_checkbox_3.stateChanged.connect(window.show_scatter_changed_3)
window.form.data_color_input_3.currentTextChanged.connect(window.data_color_3_changed)
window.form.showline_checkbox_3.stateChanged.connect(window.show_line_changed_3)

window.form.showscatter_checkbox_4.stateChanged.connect(window.show_scatter_changed_4)
window.form.data_color_input_4.currentTextChanged.connect(window.data_color_4_changed)
window.form.showline_checkbox_4.stateChanged.connect(window.show_line_changed_4)

window.form.showerrors_checkbox_1.stateChanged.connect(window.show_errors_changed_1)
window.form.showerrors_checkbox_2.stateChanged.connect(window.show_errors_changed_2)
window.form.showerrors_checkbox_3.stateChanged.connect(window.show_errors_changed_3)
window.form.showerrors_checkbox_4.stateChanged.connect(window.show_errors_changed_4)

window.form.fit_selection_1.currentTextChanged.connect(window.update_fit_selection_1)
window.form.fit_selection_2.currentTextChanged.connect(window.update_fit_selection_2)
window.form.fit_selection_3.currentTextChanged.connect(window.update_fit_selection_3)
window.form.fit_selection_4.currentTextChanged.connect(window.update_fit_selection_4)


window.form.saveplot_button.clicked.connect(window.save_plot)
window.form.save_rawdata_checkbox.stateChanged.connect(window.update_save_raw_data)
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

window.form.x_error_input_1.editingFinished.connect(window.update_x_err_1)
window.form.x_error_input_2.editingFinished.connect(window.update_x_err_2)
window.form.x_error_input_3.editingFinished.connect(window.update_x_err_3)
window.form.x_error_input_4.editingFinished.connect(window.update_x_err_4)

window.form.y_error_input_1.editingFinished.connect(window.update_y_err_1)
window.form.y_error_input_2.editingFinished.connect(window.update_y_err_2)
window.form.y_error_input_3.editingFinished.connect(window.update_y_err_3)
window.form.y_error_input_4.editingFinished.connect(window.update_y_err_4)

window.form.plot_title_input.editingFinished.connect(window.update_plot_title)
window.form.x_label_input.editingFinished.connect(window.update_x_label)
window.form.y_label_input.editingFinished.connect(window.update_y_label)

window.form.x_limits_input.editingFinished.connect(window.define_x_lim)
window.form.y_limits_input.editingFinished.connect(window.define_y_lim)




window.init_plot(x_data_1, y_data_1, legend_label_1, x_label, y_label, plot_title, x_lim, y_lim, grid_enabled, grid_alpha, scatter_enabled_1, line_enabled_1, data_color_1, save_raw_data)

# Set default value for the "Pin GUI to Top" checkbox
window.form.pingui_checkbox.setChecked(True)  # Set to True if you want it checked by default
window.form.save_rawdata_checkbox.setChecked(True)  # Set to True if you want it checked by default

#%% - Start the Qt event loop
window.show()

sys.exit(app.exec())
