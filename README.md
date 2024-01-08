# File Compression with Huffman Encoding

This program compresses a file using Huffman coding. This is an type of lossless encoding that assigns a shorter encoding to more frequent bytes and a longer encoding to less frequent bytes.

Because it is written in Python, it is extremely slow for files over 10 MB. A faster version of the code written in C++ can be provided upon request.

Running compression agorithm:
```
python compress <original_file> <compressed_file>
```

Uncompressing file:
```
python uncompress <compressed_file> <uncompressed_file>
```
