import csv

# This is the main data structure class.


class Data_Structure:
    def __init__(self):

        # Variables in the data structure, the linked list stores all the data
        self.linked_list = Linked_List()
        self.data_index = []
        self.data_index_units = []
        self.log_name = "No_Log_loaded"
        self.file = ""
        self.num_data_points = 0

    # Parses a csv from the input file path into the structures linked list
    # Needs to be edited to accept both Link and Haltech CSV's
    def parse_file(self, input_file_path):
        line_number = 0
        self.file = input_file_path

        with open(self.file, mode='r') as file:
            csvfile = csv.reader(file)
            for line in csvfile:
                node_data = []
                for string in line:
                    if line_number < 3:

                        # Initial declarations to idenitify log

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
        self.validate_linked_list()  # confirms linked list is correct for the data recieved
        return

    # returns axis elements and titles to be used in a matplotlib pyplot
    def graph_data_array(self, x_name, y_name):
        x_index = -1
        y_index = -1
        array_current_index = 0

        # find index for x and y variables in Linked List.
        while x_index == -1 or y_index == -1 and array_current_index <= len(self.data_index):
            if self.data_index[array_current_index] == x_name:
                x_index = array_current_index
            if self.data_index[array_current_index] == y_name:
                y_index = array_current_index
                print("y index set: y=" + str(y_index))

            array_current_index = array_current_index + 1

        # make the axis data arrays.
        x_array, y_array = self.linked_list.get_x_and_y_arrays(x_index, y_index)

        # make the titles for the axis. Also used for the graph title
        x_axis_name = str(x_name) + " (" + str(self.data_index_units[x_index]) + ")"
        y_axis_name = str(y_name) + " (" + str(self.data_index_units[y_index]) + ")"

        return x_array, y_array, x_axis_name, y_axis_name

    # prints every value in the data index. Useful to see what variables are stored
    def print_data_index(self):
        for string in self.data_index:
            print(string)
        return

    # prints every unit for each variable stored. Useful for checking the variables have the right untis
    def print_data_units(self):
        for string in self.data_index_units:
            print(string)
        return

    # confirms the number of nodes in linked list is equal to the number of lines in the csv.
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

        # error statement if the linked list is not valid for the given csv.
        # TODO move to an error message in the GUI
        if node_count != self.num_data_points:
            print(" Data in Linked list does not equal nodes in csv")
            print("Number of Bad Nodes: " + str(bad_data_count))
            print("number of good nodes: " + str(node_count))
            print("Number of total nodes: " + str(self.num_data_points))

        return

    def get_variables(self):
        return self.data_index, self.data_index_units


# Node class used for linked List.
class Node:
    def __init__(self, data):
        self.data = data
        self.next = None


# Linked List data structure for use in the actual data structure
class Linked_List:
    def __init__(self):
        self.head = None
        self.num_nodes = 0

    # Print every node's data and its position that is in the linked list
    # TODO move print to an output box in the GUI
    def print_linked_list(self):
        current_node = self.head
        node_num = 0
        while current_node is not None:
            print(str(node_num) + ": " + str(current_node.data))
            current_node = current_node.next
            node_num = node_num + 1

        return

    # Adds a node to the Linked List given the data.
    # TODO check if you can get rid of temp_node
    def insert_node(self, data):
        new_node = Node(data)  # create new node
        temp_node = self.head
        self.head = new_node
        new_node.next = temp_node
        self.num_nodes = self.num_nodes + 1
        return

    # Delete a node based on a node or its previous node/data. the node parameter can also be data
    def delete_node(self, node, previous_node):
        if not isinstance(node, Node):
            node, previous_node = self.find_node_from_data(node)

        # find previous node if not specified so the linked list structure can be maintained
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

    # Returns the node structure that has the same data as specified, as well as the node before it
    def find_node_from_data(self, data):
        # check if head node is the right node Has to be this way due to no previous node
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

    # returns the node that comes before the node specified.
    # TODO make a check to make sure that a node is supplied, and an error message if not
    def get_previous_node(self, node):
        if node == self.head:
            return None

        current_node = self.head

        # iterate through linked list to find the node specified.
        while current_node.next is not None:
            if current_node.next == node:
                return current_node
            current_node = current_node.next

        return None

    # TODO check if this actually works, I don't think it does tbh
    def quick_sort(self, first, last, data_index):
        if first == last:
            return

        pivot = self.quick_sort_pivot(first, last, data_index)

        if pivot is not None and pivot.next is not None:
            self.quick_sort(pivot.next, last, data_index)

        if pivot is not None and first != pivot:
            self.quick_sort(first,last, data_index)

        return

    # TODO check if it actually works
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

    # returns the last node in the linked list.
    # TODO print an error message to GUI if linked list is empty
    def get_tail_node(self):
        node = self.head
        while node.next is not None:
            node = node.next
        return node

    # Returns two arays based on the index for the data
    # TODO error message if linked list is empty or try to access an element outside of index
    def get_x_and_y_arrays(self, x_index, y_index):
        # self.quick_sort(self.head, self.get_tail_node(), x_index)
        node = self.head
        x_array = []
        y_array = []
        while node is not None:
            x_array.append(node.data[x_index])
            y_array.append(node.data[y_index])
            node = node.next

        return x_array, y_array
