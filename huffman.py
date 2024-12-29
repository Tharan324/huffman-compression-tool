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
        generate_code_helper(root, '', codes)
        return codes

def generate_code_helper(node, code, codes):
        if node is None:
                return
        generate_code_helper(node.left, code + '0', codes)
        generate_code_helper(node.right, code + '1', codes)
        codes[node.char] = code

def encode_data(data, codes):
        encoded_data = ''
        for char in data:
                encoded_data += codes[char]
        return encoded_data

def decode_data(encoded_data, root):
        codes = generate_codes(root)
        decoded_data = ''
        start = 0
        for i in range(1, len(encoded_data)+1):
                if encoded_data[start:i] in codes.values():
                        for key, value in codes.items():
                                if value == encoded_data[start:i]:
                                        decoded_data += key
                                        break
                        start = i
                        i += 1
        return decoded_data

def compress(filepath):
        with open(filepath, 'r') as f:
                data = f.read()

        frequency = calculate_frequency(data)
        root = build_huffman_tree(frequency)
        codes = generate_codes(root)
        print("Huffman codes: ", codes)
        encoded_data = encode_data(data, codes)

        with open(filepath+'.huff', 'wb') as f:
                pickle.dump((root, encoded_data), f)

        print("Compressed file is saved at: ", filepath+'.huff')

def decompress(filepath):
        with open(filepath, 'rb') as f:
                root, encoded_data = pickle.load(f)
        
        decoded_data = decode_data(encoded_data, root)
        
        with open(filepath[:-5], 'w') as f:
                f.write(decoded_data)

        print("Decompressed file is saved at: ", filepath[:-5])

if __name__ == "__main__":
        # ./huffman.py compress/decompress <src_filepath>
        if len(sys.argv) != 3:
                print("Usage: ./huffman.py compress/decompress <filename>")
                sys.exit(1)
        if sys.argv[1] != 'compress' and sys.argv[1] != 'decompress':
                print("Invalid operation. Use compress/decompress")
                sys.exit(1)
                
        operation = sys.argv[1]
        src_filepath = sys.argv[2]

        if os.path.exists(src_filepath) == False:
                print("Source file does not exist")
                sys.exit(1)

        if operation == 'compress':
                compress(src_filepath)      
        elif operation == 'decompress':
                decompress(src_filepath)
               