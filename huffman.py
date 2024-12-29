import heapq
from collections import defaultdict, Counter
import pickle
import sys

class HuffmanNode:
        def __init__(self, char, freq):
                self.char = char
                self.freq = freq
                self.left = None
                self.right = None
        
        def __lt__(self, other):
                return self.freq < other.freq
        
def calculate_frequency(data):
        return Counter(data)

def build_huffman_tree(frequency):
        pass

def encode_data(data, frequency):
        pass

def compress(data):
        pass

def decompress(data):
        pass

if __name__ == "__main__":
        