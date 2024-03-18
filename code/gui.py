import dearpygui.dearpygui as dpg
from Data_Structure import Data_Structure
import matplotlib.pyplot as plt
dpg.create_context()


class Button:
    def __init__(self, callback_source, label, parent):
        with dpg.stage():
            self.id = dpg.add_button(label=label, callback=callback_source, parent=parent.id, tag=label)
        return

    def set_call_back(self, callback_source):
        dpg.configure_item(self.id, callback=callback_source)
        return


class Main_Window:
    def __init__(self):
        self.sub_windows = []
        self.items = []
        with dpg.stage() as stage:
            self.id = dpg.add_window(label="Main Window", tag="Primary Window")
        self.stage = stage
        new_window_button = Button(callback_source=self.add_sub_window, label="New Window", parent=self)
        self.items.append(new_window_button)
        return

    def add_item(self, item):
        dpg.move_item(item.id, parent=self.id)
        self.items.append(item.id)
        return

    def add_sub_window(self):
        sub_window = Sub_Window(self)
        self.sub_windows.append(sub_window)
        return

    def delete(self):
        for sub_window in self.sub_windows:
            sub_window.delete()
        dpg.unstage(self.stage)


class Sub_Window:
    def __init__(self, parent):
        self.items = []
        self.data_structure = Data_Structure()
        self.x_axis = None
        self.y_axis = []
        self.x_axis_list = []
        self.y_axis_list = []

        with dpg.stage() as stage:
            self.id = dpg.add_window(label="sub_window_" + str(len(parent.sub_windows)), tag="sub_window_" + str(len(parent.sub_windows)))
            self.stage = stage
            self.label = "sub_window_" + str(len(parent.sub_windows))
            file_id = "file_dialog_id" + str(self.id)

        with dpg.file_dialog(directory_selector=False, show=False, callback=self.file_input_callback, tag=file_id, width=700, height=400):
            dpg.add_file_extension(".csv", custom_text="[CSV File]", color=(150, 255, 150, 255))

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
                                dpg.add_menu(label="x_axis", tag="x_axis"+str(self.id))
                            if j == 1:
                                dpg.add_button(label="load log file", tag="load_file" + str(self.id), callback=lambda: dpg.show_item("file_dialog_id" + self.id))
                            if j == 2:
                                dpg.add_menu(label= "y_axis", tag="y_axis"+str(self.id))
        return

    def file_input_callback(self, sender, app_data):
        self.data_structure.parse_file(app_data.get("file_path_name", ""))
        dpg.hide_item(sender)
        dpg.hide_item("load_file"+str(self.id))
        data_index, data_units = self.data_structure.get_variables()
        dpg.add_button(parent=self.id, label="graph", tag="graph"+str(self.id), callback=self.graph_data)
        print("file_input")
        print(str(len(data_index)))
        print(str(len(data_units)))
        for i in range(0, len(data_units)):
            dpg.add_checkbox(label=str(data_index[i]) + " " + str(data_units[i]), tag=str(data_index[i]) + "x" + str(self.id) + str(data_units[i]) + str(i), parent="x_axis"+str(self.id), callback=self.x_axis_callback, user_data=str(data_index[i]))
            self.x_axis_list.append(str(data_index[i]) + "x" + str(self.id) + str(data_units[i]) + str(i))
            dpg.add_checkbox(label=str(data_index[i]) + " " + str(data_units[i]), tag=str(data_index[i]) + "y" + str(self.id) + str(data_units[i] + str(i)), parent="y_axis"+str(self.id), callback=self.y_axis_callback, user_data=str(data_index[i]))
            self.y_axis_list.append(str(data_index[i]) + "y" + str(self.id) + str(data_units[i]) + str(i))
        return

    def x_axis_callback(self, sender, app_data, user_data):
        self.x_axis = user_data
        for tag in self.x_axis_list:
            if tag != str(sender):
                dpg.configure_item(item=tag, default_value=False)
        return

    def y_axis_callback(self, sender, app_data, user_data):
        if app_data:
            self.y_axis.append(user_data)
        else:
            for i in range(0, len(self.y_axis)):
                if self.y_axis[i] == user_data:
                    self.y_axis.pop(i)
                    return
        return

    def graph_data(self):
        print("y_axis_array:")
        for string in self.y_axis:
            print(str(string))
        x_data, y_data, x_name, y_name = self.data_structure.graph_data_array(self.x_axis, self.y_axis[0])
        plt.scatter(x_data,y_data)
        plt.xlabel(x_name)
        plt.ylabel(y_name)
        plt.title(x_name + " VS " + y_name)
        plt.savefig("../plots." + x_name + " VS " + y_name + ".png")

        width, height, channels, data = dpg.load_image("../plots." + x_name + " VS " + y_name + ".png")
        with dpg.texture_registry(show=True):
            dpg.add_static_texture(width=width, height=height, default_value=data, tag="texture_tag" + str(self.id))
        dpg.add_image("texture_tag" + str(self.id), parent=self.id)
        return

    def delete(self):
        dpg.unstage(self.stage)
        return


main_window = Main_Window()
dpg.create_viewport(title="Data Log Analysis")
dpg.setup_dearpygui()
dpg.show_viewport()
dpg.set_primary_window("Primary Window", True)
dpg.start_dearpygui()
dpg.destroy_context()
