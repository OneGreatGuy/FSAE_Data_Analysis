import dearpygui.dearpygui as dpg
from Data_Structure import Data_Structure
import matplotlib.pyplot as plt
from matplotlib.ticker import AutoMinorLocator, MaxNLocator
dpg.create_context()


# define a button so it can be created during runtime
class Button:
    def __init__(self, callback_source, label, parent):
        with dpg.stage():
            self.id = dpg.add_button(label=label, callback=callback_source, parent=parent.id, tag=label)
        return

    # Specify a call back for a button, allows the callback for a button to change during runtime
    def set_call_back(self, callback_source):
        dpg.configure_item(self.id, callback=callback_source)
        return


# definition for the main window. All subwindows are displayed here. Also refered to as veiwport
class Main_Window:
    def __init__(self):
        self.sub_windows = []  # keeps track of all current subwindows
        self.items = []  # keeps track of all items in the Main window
        with dpg.stage() as stage:  # create the main window/ viewport
            self.id = dpg.add_window(label="Main Window", tag="Primary Window")
        self.stage = stage  # specify the stage for the main window
        new_window_button = Button(callback_source=self.add_sub_window, label="New Window", parent=self)  # create button to add a subwindow
        self.items.append(new_window_button)
        return

    # Add an item (button anything really) to the main window
    def add_item(self, item):
        dpg.move_item(item.id, parent=self.id)
        self.items.append(item.id)
        return

    # Adds a sub window to the viewport.
    def add_sub_window(self):
        sub_window = Sub_Window(self)
        self.sub_windows.append(sub_window)
        return

    # definition to delete the main window, making sure to delete all the sub windows as well.
    def delete(self):
        # delete all subwindows
        for sub_window in self.sub_windows:
            sub_window.delete()

        # delete main window/self
        dpg.unstage(self.stage)


# Sub_Window class, most important element. Multiple subwindows per Main window
class Sub_Window:
    def __init__(self, parent):
        self.items = []  # keep track of all items in subwindow
        self.data_structure = Data_Structure()  # data structure for data to be analyzed in Sub window
        self.x_axis = None
        self.y_axis = None
        self.x_axis_list = []
        self.y_axis_list = []

        # create subwindow element, with a unique id.
        with dpg.stage() as stage:
            self.id = dpg.add_window(label="sub_window_" + str(len(parent.sub_windows)), tag="sub_window_" + str(len(parent.sub_windows)))
            self.stage = stage
            self.label = "sub_window_" + str(len(parent.sub_windows))
            file_id = "file_dialog_id" + str(self.id)

        # create directory selector window to specify the file to load into the program
        with dpg.file_dialog(directory_selector=False, show=False, callback=self.file_input_callback, tag=file_id, width=700, height=400):
            dpg.add_file_extension(".csv", custom_text="[CSV File]", color=(150, 255, 150, 255))

        # this is to organize the main Subwindow structure and add the items neccesary
        with dpg.table(parent=self.id, header_row=False):
            dpg.add_table_column()
            dpg.add_table_column()
            dpg.add_table_column()

            # add_table_next_column will jump to the next row
            # once it reaches the end of the columns
            # table next column use slot 1
            for i in range(0, 4):
                with dpg.table_row():
                    for j in range(0, 3):
                        if i == 0:
                            if j == 0:
                                # menu to select variable for x axis
                                dpg.add_menu(label="x_axis", tag="x_axis"+str(self.id))
                            if j == 1:
                                # button to load a file. Brings up file directory selector
                                dpg.add_button(label="load log file", tag="load_file" + str(self.id), callback=lambda: dpg.show_item("file_dialog_id" + self.id))
                            if j == 2:
                                # menu to select y axis
                                dpg.add_menu(label="y_axis", tag="y_axis"+str(self.id))
        return

    # definition for the callback for the file directory. Implies a file was selected
    # TODO check if the file is an acceptable file to load
    def file_input_callback(self, sender, app_data):
        # parse data into the data structure
        self.data_structure.parse_file(app_data.get("file_path_name", ""))
        # hide the directory selector and the load file button
        dpg.hide_item(sender)
        dpg.hide_item("load_file"+str(self.id))
        # get variables and units to make checkboxes for menus.
        data_index, data_units = self.data_structure.get_variables()
        # create the graphing button to actually make a graph. Prevents user from trying to make a graph with no loaded data
        dpg.add_button(parent=self.id, label="graph", tag="graph"+str(self.id), callback=self.graph_data)
        print("file_input")
        print("num of data" + str(len(data_index)))
        print("num units" + str(len(data_units)))

        # add checkboxes to the x and y menus for each varaible.
        for i in range(0, len(data_units)):
            dpg.add_checkbox(label=str(data_index[i]) + " " + str(data_units[i]), tag=str(data_index[i]) + "x" + str(self.id) + str(data_units[i]) + str(i), parent="x_axis"+str(self.id), callback=self.x_axis_callback, user_data=str(data_index[i]))
            self.x_axis_list.append(str(data_index[i]) + "x" + str(self.id) + str(data_units[i]) + str(i))
            dpg.add_checkbox(label=str(data_index[i]) + " " + str(data_units[i]), tag=str(data_index[i]) + "y" + str(self.id) + str(data_units[i] + str(i)), parent="y_axis"+str(self.id), callback=self.y_axis_callback, user_data=str(data_index[i]))
            self.y_axis_list.append(str(data_index[i]) + "y" + str(self.id) + str(data_units[i]) + str(i))
        return

    # specify the callback for when a checkbox in the x axis is clicked
    def x_axis_callback(self, sender, app_data, user_data):
        # sets the x_axis variable. Only one x value is allowed
        self.x_axis = user_data
        # make sure each other checkbox is unchecked
        for tag in self.x_axis_list:
            if tag != str(sender):
                dpg.configure_item(item=tag, default_value=False)
        return

    # specify behavior for when a checkbox in the y menu is clicked
    def y_axis_callback(self, sender, app_data, user_data):
        # sets the x_axis variable. Only one x value is allowed
        self.y_axis = user_data
        # make sure each other checkbox is unchecked
        for tag in self.y_axis_list:
            if tag != str(sender):
                dpg.configure_item(item=tag, default_value=False)
        return

    # Callback for the graph button
    def graph_data(self):
        print("y_axis_array:" + self.y_axis)

        # get data for the plot
        x_data, y_data, x_name, y_name = self.data_structure.graph_data_array(self.x_axis, self.y_axis)

        # create the scatter plot
        plt.scatter(x_data, y_data)
        plt.xlabel(x_name)
        plt.ylabel(y_name)
        plt.title(x_name + " VS " + y_name)

        ax = plt.gca()  # Get current axis
        ax.xaxis.set_major_locator(MaxNLocator(nbins='auto', prune = None))
        ax.yaxis.set_major_locator(MaxNLocator(nbins='auto', prune = None))
        ax.xaxis.set_minor_locator(AutoMinorLocator())
        ax.yaxis.set_minor_locator(AutoMinorLocator())

        # Set tick parameters for better readability
        ax.tick_params(axis='both', which='major', labelsize=12)
        ax.tick_params(axis='both', which='minor', labelsize=10, length=4, color='gray')

        # Show grid
        ax.grid(True, which='both', linestyle='--', linewidth=0.5)
        ax.invert_xaxis()  # Uncomment this line to reverse the x-axis
        ax.invert_yaxis()  # Uncomment this line to reverse the y-axis

        # Save the plot
        plt.tight_layout()  # Adjust layout to prevent clipping of tick-labels
        # save the plot
        plt.savefig("../plots." + x_name + " VS " + y_name + ".png")

        # specify the image dimensions and data
        width, height, channels, data = dpg.load_image("../plots." + x_name + " VS " + y_name + ".png")

        # display the image
        with dpg.texture_registry(show=False):
            dpg.add_static_texture(width=width, height=height, default_value=data, tag="texture_tag" + str(self.id))
        dpg.add_image("texture_tag" + str(self.id), parent=self.id)
        return

    # delete button for the subwindow
    def delete(self):
        dpg.unstage(self.stage)
        return


# dependencies for DearPyGui
main_window = Main_Window()
dpg.create_viewport(title="Data Log Analysis")
dpg.setup_dearpygui()
dpg.show_viewport()
dpg.set_primary_window("Primary Window", True)
dpg.start_dearpygui()
dpg.destroy_context()
