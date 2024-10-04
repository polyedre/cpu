#!/usr/bin/env python3

with open("program.bin", "wb") as binary:
    for line in open("input.txt", "r").readlines():
        byte = int(line.strip(), 2).to_bytes()
        binary.write(byte)
