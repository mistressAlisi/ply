# We will use a Trie structure to efficiently search through the words loaded from the supplied text file.
# Since Tries are a type of tree; we must define two classes, the Trie's tree struct,
# and the TrieNode struch which will represent Nodes inside the Trie.
# To keep track if we have found the end of a string, each TrieNode also carries an endOfString Boolean Flag.
class TrieNode:
    def __init__(self, char):
        self.char = char
        self.is_end = False
        self.children = {}

class Trie(object):
    def __init__(self):
        self.root = TrieNode("")

    # The Insert function implements inserting a word into a Trie tree, creating nodes as needed and inserting nodes in the right position of the tree:
    def insert(self, word):
        node = self.root
        #traverse the word character by character
        for char in word:
            #check if the character is there in the list of children
            if char in node.children:
                node = node.children[char]
            else:
                # else make a new TrieNode corresponding to that character
                new_node = TrieNode(char)
                # add the new node to the list of children
                node.children[char] = new_node
                node = new_node
        #after traversing the word set .is_end to true for the last #char
        node.is_end = True

    # Depth-first-search is the basic algorithm that we will use to traverse the Trie: It is an efficient,
    # and fast way to traverse a tree and create a "breadcrumb" of letters in the stack:
    def dfs(self, node, pre):
        if node.is_end:
            self.output.append((pre + node.char))
        for child in node.children.values():
            self.dfs(child, pre + node.char)

    # search merely implements our DFS algorithm and returns the number of children (or an empty array) with the nodes
    # that match the search string supplied to the function:
    def search(self, x):
        node = self.root
        for char in x:
            if char in node.children:
                node = node.children[char]
            else:
                return []

        self.output = []
        self.dfs(node, x[:-1])
        return self.output
