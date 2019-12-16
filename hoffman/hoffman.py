"""
    title: hoffman.py
    date: 12/15/19
    description: simple implementation of the hoffman compression alg
"""

import copy
from datetime import datetime

class Node():
    """ node obj  """
    def __init__(self, value, left=None, right=None):
        self.value = value
        self._left = left
        self._right = right

    def get_left(self):
        return self._left

    def set_left(self, node):
        self._left = node

    def get_right(self):
        return self._right

    def set_right(self, node):
        self._right = node

    def get_value(self):
        return self.value

class binary_tree():
    """ Simple Binary Tree for Hoffman """

    def __init__(self):
        self._tree_root = None
        self._map = {}

    def add_leaf(self, path, value):
        """
        path: string path to where leaf should be
        value: value to create leaf
        """

        n = self._tree_root

        for x in path[0:-2]:
            if x == '0':
                n = n.get_left()
            else:
                n = n.get_right()
        if path[-1] == '0':
            n.set_left = node(value)
        else:
            n.set_right = node(value)

        self._map[value] = path

    def add_node(self, value, update_root=False, new_root_value=None):
        new_node = Node(value)

        if self._tree_root is None:
            self._tree_root = Node(new_root_value, new_node)
            self._map[value] = '0'

        elif update_root:
            if value <= self._tree_root.get_value():
                new_tree_root = Node(new_root_value, new_node, self._tree_root)
                self._tree_root = copy.deepcopy(new_tree_root)
                self._update_map_new_root('1')
                self._map[value] = 0
            else:
                new_tree_root = Node(new_root_value, new_node, self._tree_root)
                self._tree_root = copy.deepcopy(new_tree_root)
                self._update_map_new_root('0')
                self._map[value] = '1'

    def add_node_pair(self, pair_root_value=None, left_value=None, right_value=None, update_root=False, new_root_value=None):
        """
        root_value: value of the root of the pair
        left_value: value of the left leaf
        right_value: value of the right leaf
        node: specify a node if adding the pair onto pre-existing, root_value should not
              be set if node is specified
        """
        left_node = Node(left_value)
        right_node = Node(right_value)

        if self._tree_root is None:
            root_node = Node(pair_root_value, left_node, right_node)
            self._tree_root = root_node
            self._map[left_value] = '0'
            self._map[right_value] = '1'
        
        elif update_root:
            pair_root_node = (pair_root_value, left_node, right_node)
            if pair_root_value <= self._tree_root.get_value():
                new_tree_root = Node(new_root_value, pair_root_node, self._tree_root)
                self._tree_root = copy.deepcopy(new_tree_root)
                self._update_map_new_root('1')
                self._map[left_value] = '00'
                self._map[right_value] = '01'
                
            else:
                new_tree_root = Node(new_root_value, self._tree_root, pair_root_node)
                self._tree_root = copy.deepcopy(new_tree_root)
                self._update_map_new_root('0')
                self._map[left_value] = '10'
                self._map[right_value] = '11'

    def get_node_path(self, value):
        """ return node path for value if exists """
        return self._map.get(value, None)
        

    def get_seq_map(self):
        return self._map

    def _update_map_new_root(self, prepend=0):
        for key in self._map.keys():
            self._map[key] = "{}{}".format(prepend, self._map[key])

        
    def _generate_seq_table(self):
        pass

    def get_root_value(self):
        if self._tree_root:
            return self._tree_root.get_value()
        else:
            return 0


class Hoffman():
    """ Hoffman Example Class """
    
    def __init__(self):
        self._encode_stats = {}
        self._decode_stats = {}

    def _get_char_freq(self, string):
        char_freq = {}
        for i in string:
            if i in char_freq:
                char_freq[i] += 1
            else:
                char_freq[i] = 1

        sorted_tuple = sorted(char_freq.items(), key = lambda kv:(kv[1], kv[0]))

        return sorted_tuple

    def encode_string(self, string):
        self._encode_stats['string'] = string
        self._encode_stats['length'] = len(string)
        

        # Get Frequency
        char_freq = self._get_char_freq(string)
        self._encode_stats['char_freq'] = char_freq
        print('length of frequency list: {}'.format(len(char_freq)))

        # Create Graph
        bt = binary_tree()

        start_index = 0
        if len(char_freq) % 2 == 1:
            bt.add_node(char_freq[0][0], True, char_freq[0][1])
            start_index = 1 

        for i in range(start_index, len(char_freq), 2):
            root_value = char_freq[i][1] + char_freq[i+1][1]
            bt.add_node_pair(root_value, 
                             char_freq[i+1][0],
                             char_freq[i][0],
                             update_root=True,
                             new_root_value=(bt.get_root_value() + root_value))

        # Get Seq Table
        seq_table = bt.get_seq_map()
        print(seq_table)
        
        # Replace Characters w/ sequence
        encoded_string = ''
        for char in string:
            encoded_string += seq_table[char]

        # Return encoded string
        return encoded_string, seq_table

    def decode_string(self, encoded_string, seq_table):
        # Set variables
        decoded_string = ''
        encoded_seq = ''

        # Flip sequence table
        flipped_seq_table = {}
        for key, value in seq_table.items():
            flipped_seq_table[value] = key

        # loop through encoded_string & check if there is a char_seq to decode
        for char in encoded_string:
            encoded_seq += char
            x = flipped_seq_table.get(encoded_seq, None)
            if x:
                decoded_string += x
                encoded_seq = ''
        return decoded_string

    def print_string_stats(self, encoded_stats=None, decoded_stats=None):
        pass


if __name__ == '__main__':
    hf = Hoffman()
    string = open('../data/text_data.txt', 'r').read()

    start = datetime.now()
    encoded_string, seq_table = hf.encode_string(string)
    encoded_time = datetime.now()
    print('Encoding Took: {}'.format(encoded_time-start))

    decoded_string = hf.decode_string(encoded_string, seq_table)
    print('Decoding Took: {}'.format(datetime.now() - encoded_time))

    print('String Match: {}'.format(string == decoded_string))
