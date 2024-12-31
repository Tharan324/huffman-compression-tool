def generate_large_file(file_path, size_mb=10):
    pattern = "AAAAAAAAAAAAAAAAAAAAABBBBBBCCCCCCCCDDDDDD"  # 44 bytes repeating pattern
    with open(file_path, 'w') as f:
        for _ in range((size_mb * 1024 * 1024) // len(pattern)):
            f.write(pattern)
    print(f"Large test file generated: {file_path}")

if __name__ == "__main__":
    generate_large_file("large_test.txt", size_mb=10)
