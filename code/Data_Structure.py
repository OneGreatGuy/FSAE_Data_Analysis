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
        return

    def graph_data_array(self, x_name, y_name):
        x_index = -1
        y_index = -1
        array_current_index = 0
        data_array = []

        while x_index == -1 and y_index == -1 and array_current_index <= len(self.data_index):
            if self.data_index[array_current_index] == x_name:
                x_index = array_current_index
            if self.data_index[array_current_index] == y_name:
                y_index = array_current_index

            array_current_index = array_current_index + 1

        self.linked_list.quick_sort(self.linked_list.head, self.linked_list.get_tail_node(), x_index)

        x_array, y_array = self.linked_list.get_x_and_y_arrays(x_index,y_index)
        i = 0
        while i < len(x_array):
            data_array.append([x_array[i],y_array[i]])
            i = i+1

        x_axis_name = str(x_name) + " (" + str(self.data_index_units[x_index]) + ")"
        y_axis_name = str(y_name) + " (" + str(self.data_index_units[y_index]) + ")"

        return data_array, x_axis_name, y_axis_name

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

    def quick_sort(self, first, last, data_index):
        if first == last:
            return

        pivot = self.quick_sort_pivot(first, last, data_index)

        if pivot is not None and pivot.next is not None:
            self.quick_sort(pivot.next, last, data_index)

        if pivot is not None and first != pivot:
            self.quick_sort(first,last, data_index)

        return

    def quick_sort_pivot(self, head, tail, data_index):
        pivot = head
        front = head
        while front is not None and front != tail:
            if front.data[data_index] < tail.data[data_index]:
                pivot = head
                temp_data = head.data
                head.data = front.data
                front.data = temp_data
                head = head.next

            front = front.next

        temp_data = head.data
        head.data = tail.data
        tail.data = temp_data
        return pivot

    def get_tail_node(self):
        node = self.head
        while node.next is not None:
            node = node.next
        return node

    def get_x_and_y_arrays(self, x_index, y_index):
        self.quick_sort(self.head, self.get_tail_node(), x_index)
        node = self.head
        x_array = []
        y_array = []
        while node is not None:
            x_array.append(node.data[x_index])
            y_array.append(node.data[y_index])
            node = node.next

        return x_array, y_array
