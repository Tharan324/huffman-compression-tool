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

def generate_codes(node, current_code="", codes=None):
        if codes is None:
                codes = {}
        
        # Base Case - Leaf Node
        if node.char is not None:  # Only assign code if the node has a character
                codes[node.char] = current_code
                return
        
        # Recursive Case - Traverse Left and Right
        if node.left:  # Check if left exists
                generate_codes(node.left, current_code + "0", codes)
        if node.right:  # Check if right exists
                generate_codes(node.right, current_code + "1", codes)
        
        return codes

def compress_codes(codes):
        b = bytearray()
        for char, code in codes.items():
                b.append(ord(char))
                b.append(int(code, 2))
        return b

def encode_data(data, codes):
        encoded_data = ''
        for char in data:
                encoded_data += codes[char]
        
        b = bytearray()
        padding = 8 - len(encoded_data) % 8

        first_byte = (padding & 0b111) << 5  # Shift padding to the top 3 bits
        first_byte |= int(encoded_data[:5], 2)  # Pack the next 5 bits
        b.append(first_byte)

        for i in range(5, len(encoded_data), 8):
                b.append(int(encoded_data[i:i+8], 2))
        
        return b

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
        compressed_codes = compress_codes(codes)
        print("Huffman codes: ", codes)
        encoded_data = encode_data(data, codes)

        # pickle dump needs to be changed
        # the root should not be shared, instead give the codes in binary format
        with open(filepath+'.huff', 'wb') as f:
                pickle.dump((compressed_codes, encoded_data), f)

        print("Compressed file is saved at: ", filepath+'.huff')
        print("Compression ratio: ", os.path.getsize(filepath)/os.path.getsize(filepath+'.huff'))

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
               