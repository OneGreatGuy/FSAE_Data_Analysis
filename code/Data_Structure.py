import csv


class Data_Structure:
    def __init__(self):
        self.linked_list = Linked_List()
        self.data_index = []
        self.data_index_units = []
        self.log_name = "No_Log_loaded"
        self.file = ""
        self.num_data_points = 0

    def parse_file(self, input_file_path):
        line_number = 0
        self.file = input_file_path

        with open(self.file, mode='r') as file:
            csvfile = csv.reader(file)
            for line in csvfile:
                node_data = []
                for string in line:
                    if line_number < 3:

                        if line_number == 0:
                            self.log_name = string

                        if line_number == 1:
                            self.data_index.append(string)

                        if line_number == 2:
                            self.data_index_units.append(string)
                    else:
                        node_data.append(string)

                if line_number > 3:
                    self.linked_list.insert_node(node_data)
                line_number = line_number + 1

        self.num_data_points = line_number
        self.validate_linked_list()
        print(str(len(self.data_index)))
        print(str(len(self.data_index_units)))
        return

    def graph_data_array(self, x_name, y_name):
        x_index = -1
        y_index = -1
        array_current_index = 0

        while x_index == -1 or y_index == -1 and array_current_index <= len(self.data_index):
            if self.data_index[array_current_index] == x_name:
                x_index = array_current_index
            if self.data_index[array_current_index] == y_name:
                y_index = array_current_index
                print("y index set: y=" + str(y_index))

            array_current_index = array_current_index + 1

        x_array, y_array = self.linked_list.get_x_and_y_arrays(x_index, y_index)

        x_axis_name = str(x_name) + " (" + str(self.data_index_units[x_index]) + ")"
        y_axis_name = str(y_name) + " (" + str(self.data_index_units[y_index]) + ")"

        print(y_index)
        print(x_index)
        return x_array, y_array, x_axis_name, y_axis_name

    def get_knock_data(self):
        knock_1_index = -1
        knock_2_index = -1
        knock_3_index = -1
        knock_4_index = -1
        current_index = 0

        while knock_1_index == -1 or knock_2_index == -1 or knock_3_index == -1 or knock_4_index == -1 and current_index <= len(self.data_index):
            if self.data_index[current_index] == "Knock Table 1 Level":
                knock_1_index = current_index
            if self.data_index[current_index] == "Knock Table 2 Level":
                knock_2_index = current_index
            if self.data_index[current_index] == "Knock Table 3 Level":
                knock_3_index = current_index
            if self.data_index[current_index] == "Knock Table 4 Level":
                knock_4_index = current_index
            current_index = current_index + 1

        return self.linked_list.get_data_array_from_index(knock_1_index), self.linked_list.get_data_array_from_index(knock_2_index), self.linked_list.get_data_array_from_index(knock_3_index), self.linked_list.get_data_array_from_index(knock_4_index)

    def get_data_array_from_name(self, name):
        index = -1
        for current_index in range(len(self.data_index)):
            if self.data_index[current_index] == name:
                index = current_index
                break
        if index == -1:
            print("could not find index for " + name)
            return []
        return self.linked_list.get_data_array_from_index(index)

    def print_data_index(self):
        for string in self.data_index:
            print(string)
        return

    def print_data_units(self):
        for string in self.data_index_units:
            print(string)
        return

    def validate_linked_list(self):

        node_count = 4  # start at 4 due to a line for name of csv, parameters, and units, and blank line
        bad_data_count = -4  # start at -4 because the first 4 lines are stored in Datastructure, not Linked List
        with open(self.file, mode='r') as file:
            csvfile = csv.reader(file)

            for string in csvfile:
                current_node, previous_node = self.linked_list.find_node_from_data(string)
                if current_node is not None:
                    node_count = node_count + 1
                else:
                    bad_data_count = bad_data_count + 1

        if node_count != self.num_data_points:
            print(" Data in Linked list does not equal nodes in csv")
            print("Number of Bad Nodes: " + str(bad_data_count))
            print("number of good nodes: " + str(node_count))
            print("Number of total nodes: " + str(self.num_data_points))

        return

    def get_variables(self):
        return self.data_index, self.data_index_units


class Node:
    def __init__(self, data):
        self.data = data
        self.next = None


class Linked_List:
    def __init__(self):
        self.head = None
        self.num_nodes = 0

    def print_linked_list(self):
        current_node = self.head
        node_num = 0
        while current_node is not None:
            print(str(node_num) + ": " + str(current_node.data))
            current_node = current_node.next
            node_num = node_num + 1

        return

    def insert_node(self, data):
        new_node = Node(data)
        temp_node = self.head
        self.head = new_node
        new_node.next = temp_node
        self.num_nodes = self.num_nodes + 1
        return

    def delete_node(self, node, previous_node):
        if not isinstance(node, Node):
            node, previous_node = self.find_node_from_data(node)

        if previous_node is None:
            previous_node = self.get_previous_node(node)

        if previous_node is None:
            self.head = node.next
            del node
            return

        next_node = node.next
        previous_node.next = next_node
        del node
        return

    def find_node_from_data(self, data):
        if self.head.data == data:
            return self.head, None

        current_node = self.head.next
        previous_node = self.head
        while current_node is not None:
            if current_node.data == data:
                return current_node, previous_node
            previous_node = current_node
            current_node = current_node.next

        return None, None

    def get_previous_node(self,node):
        if node == self.head:
            return None

        current_node = self.head

        while current_node.next is not None:
            if current_node.next == node:
                return current_node
            current_node = current_node.next

        return None

    def get_tail_node(self):
        node = self.head
        while node.next is not None:
            node = node.next
        return node

    def get_x_and_y_arrays(self, x_index, y_index):
        node = self.head
        x_array = []
        y_array = []
        while node is not None:
            x_array.append(node.data[x_index])
            y_array.append(node.data[y_index])
            node = node.next

        return x_array, y_array

    def get_data_array_from_index(self, index):
        node = self.head
        array = []
        while node is not None:
            array.append(node.data[index])
            node = node.next
        return array
