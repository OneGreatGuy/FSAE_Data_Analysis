import dearpygui.dearpygui as dpg
from Data_Structure import Data_Structure


class Main_Window:
    def __init__(self):
        self.sub_windows = []
        with dpg.stage() as stage:
            self.id = dpg.add_window(label="Main Window", tag="Primary Window")
        self.stage = stage()

    def add_sub_window(self):
        sub_window = Sub_Window(self)
        self.sub_windows.append(sub_window)
        return


class Sub_Window:
    def __init__(self, parent):
        self.items = []
        self.data_structure = Data_Structure()
        with dpg.stage() as stage:
            self.id = dpg.add_window(label="sub_window_" + str(len(parent.sub_windows)), tag="sub_window_" + str(len(parent.sub_windows)))
        self.stage = stage()


dpg.create_context()
dpg.create_viewport(title="Data Log Analysis")
dpg.setup_dearpygui()
dpg.show_viewport()
dpg.set_primary_window("Primary Window", True)
dpg.start_dearpygui()
dpg.destroy_context()
