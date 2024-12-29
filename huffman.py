import heapq
from collections import defaultdict, Counter
import pickle
import sys
import os

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
        # create a min heap of nodes
        heap = []
        for char, freq in frequency.items():
                heap.append(HuffmanNode(char, freq))
        heapq.heapify(heap)

        # build huffman tree
        while len(heap) > 1:
                # take two lowest frequency nodes
                left = heapq.heappop(heap)
                right = heapq.heappop(heap)
                # merge them into a new node and push it back to heap
                node = HuffmanNode(None, left.freq + right.freq)
                node.left = left
                node.right = right
                heapq.heappush(heap, node)
        
        # return the only remaining root of the tree
        return heap[0]

def generate_codes(root):
        codes = {}
        generate_codes_helper(root, '', codes)
        return codes

def generate_code_helper(node, code, codes):
        if node is None:
                return
        generate_codes_helper(root.left, code + '0', codes)
        generate_codes_helper(root.right, code + '1', codes)
        codes[node.char] = code

def encode_data(data, codes):
        encoded_data = ''
        for char in data:
                encoded_data += codes[char]
        return encoded_data

def compress(filepath):
        with open(filepath, 'r') as f:
                data = f.read()

        frequency = calculate_frequency(data)
        root = build_huffman_tree(frequency)
        codes = generate_codes(root)
        encoded_data = encode_data(data, codes)

        with open(filepath+'.huff', 'wb') as f:
                pickle.dump((root, encoded_data), f)

        print("Compressed file is saved at: ", filepath+'.huff')

def decompress(filepath):
        #with open(filepath, 'rb') as f:
        #        root, encoded_data = pickle.load(f)
        pass

if __name__ == "__main__":
        # ./huffman.py compress/decompress <src_filepath> <dest_filepath>
        if len(sys.argv) != 4:
                print("Usage: ./huffman.py compress/decompress <src_filepath> <dest_filepath>")
                sys.exit(1)
        if sys.argv[1] != 'compress' and sys.argv[1] != 'decompress':
                print("Invalid operation. Use compress/decompress")
                sys.exit(1)
                
        operation = sys.argv[1]
        src_filepath = sys.argv[2]
        dest_filepath = sys.argv[3]

        if src_filepath == dest_filepath:
                print("Source and destination files cannot be same")
                sys.exit(1)
        elif os.path.exists(src_filepath) == False:
                print("Source file does not exist")
                sys.exit(1)

        if operation == 'compress':
                compress(src_filepath)
                print("Compressed file is saved at: ", dest_filepath)
        elif operation == 'decompress':
                pass
                # call decompress function
                # print("Decompressed file is saved at: ", dest_filepath)
               
                