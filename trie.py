
from typing import Union, List, Optional
import pandas as pd

# TODO: INVESITGATE WHY THIS IMPLEMETATION DOES NOT WORK
class LetterDict():
    letter_dict = {}
    def __init__(self):
        self.letter_dict = self.get_letter_dict()

    def get_letter_dict(self):
        a_ASCII = 97
        z_ASCII = 122
        space_ASCII = 32

        for i in range(a_ASCII, z_ASCII+1):
            self.letter_dict[chr(i)] = None
        # include spaces
        self.letter_dict[chr(space_ASCII)] = None
        return self.letter_dict


def get_letter_dict():
    letter_dict = {}
    a_ASCII = 97
    z_ASCII = 122
    space_ASCII = 32

    for i in range(a_ASCII, z_ASCII+1):
        letter_dict[chr(i)] = None
    # include spaces
    letter_dict[chr(space_ASCII)] = None
    return letter_dict

class TrieNode():
    """
    A trie node part of the trie data structure
    """
    def __init__(self, char):
        """Declare an empty trie node containing children and word status
        """
        # create_dict = LetterDict()
        self.children = get_letter_dict()
        # print(self.children)
        self.is_word = False
        self.char = char
    
class Trie():
    def __init__(self):
        """Create a trie object
        """
        # initialize root as an asterisk 
        self.root = TrieNode('*')
        # print(self.root.children)

    def insert(self, word: str) -> None:
        # noramlize word to lower case
        word = word.lower()
        
        # initalize the node to start looping
        current_node = self.root

        # loop through each character in the word to expand the trie 
        for char in word:
            if current_node.children.get(char) == None:
                # check if no current child node exists
                # create a new node 
                current_node.children[char] = TrieNode(char)
            # switch nodes to child node
            print(current_node.children)
            current_node = current_node.children[char]
            print(current_node.char)
        
        # when the loop ends, the current node will contian the final node for the word
        current_node.is_word = True
        print(current_node.char)
        print(current_node.is_word)
    

    def find_all_strings(self, curr_word: str) -> Optional[List[str]]:
        all_strings = []
        """Search for a word in a trie"""
        curr_node = self.root
        # search the trie
        for char in curr_word:
            # print(curr_node.children.get(char))
            if curr_node.children.get(char) == None:
                # the search string does not exist in the trie, return none
                return None
            # move to the next node
            curr_node = curr_node.children[char]
            # print(char)
        else:
            # loop has ended, deal with last character in word
            if curr_node == None:
                return None
        
        # check if the final node was a word; if it was append the current search word
        if curr_node.is_word:
            all_strings.append(curr_word)

        # go through the remainder of the tree, keeping track of words and append it to all strings
        base_word = curr_word


        return all_strings
    
def return_ending(node: TrieNode):
    # BC1: check if we are at a leaf, return char
    is_empty = True
    for letter in node.children:
        if node.children[letter] != None:
            is_empty = False
    if is_empty:
        return node.char
    
    # BC2: The node is a word but not leaf node
    child_words = []
    if node.is_word:
        # loop through all the nodes and get leaves
        for letter in node.children:
            if node.children[letter] is not None:
                # recursive call on next node
                next_node = node.children[letter]
                # combine the current nodes characters with the next node's characters
                new_ending = node.char + return_ending(next_node)
                child_words.append(new_ending)
        return [node.char, *child_words]
    
    # not a word or a leaf node
    # loop through all the nodes and get leaves
    for letter in node.children:
        if node.children[letter] is not None:
            # recursive call on next node
            next_node = node.children[letter]
            # combine the current nodes characters with the next node's characters
            new_endings = node.char + return_ending(next_node)
            child_words.append(*new_endings)



test_trie = Trie()

test_trie.insert('bob')

test_trie.insert('hello')

print(test_trie.root.children['b'].char)
print(test_trie.root.children['h'].char)
print(test_trie.root.children)