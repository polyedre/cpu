#!/usr/bin/env python3

import sys
binary = sys.argv[1]

with open(binary, 'rb') as bin_file:
    program = bin_file.read()

global ram
global PC

ram = bytearray(70000)
for i, byte in enumerate(program):
    ram[i] = byte

memory = {7: 0xFEFE}
PC = 0
states = []

def set_to_ram(address, value):
    for offset, byte in enumerate(value.to_bytes(length=2)):
        ram[address + offset] = byte

def load1():
    X = ram[PC] & int("111", 2)
    memory[X] = int.from_bytes(ram[PC+1:PC+3], byteorder='big')
    print(f"load1: r{X} = {memory[X]}")

def load2():
    X = ram[PC] & int("111", 2)
    ADDRESS = int.from_bytes(ram[PC+1:PC+3], byteorder='big')
    memory[X] = int.from_bytes(ram[ADDRESS:ADDRESS+2], byteorder='big')
    print(f"load2: r{X} = RAM[{ADDRESS}] (value {ram[ADDRESS]})")

def load3():
    X = ram[PC] & int("111", 2)
    Y = (ram[PC+1] & int("11100000", 2)) >> 5
    memory[X] = memory[Y]
    print(f"load3: r{X} = r{Y}")

def loadz():
    X = ram[PC] & int("111", 2)
    Y = (ram[PC+1] & int("11100000", 2)) >> 5
    Z = ram[PC+1] & int("00011111", 2)
    if Z >= 0b10000:
        Z = Z - 0b100000
    memory[X] = int.from_bytes(ram[memory[Y] + Z:memory[Y] + Z + 2], byteorder='big')
    print(f"loadz: r{X} = *(r{Y} + {Z}) = {memory[X]}")

def add():
    X = ram[PC] & int("111", 2)
    Y = (ram[PC+1] & int("11100000", 2)) >> 5
    memory[X] += memory[Y]
    print(f"add: r{X} += r{Y}")

def mul():
    X = ram[PC] & int("111", 2)
    Y = (ram[PC+1] & int("11100000", 2)) >> 5
    memory[X] *= memory[Y]
    print(f"mul: r{X} *= r{Y}")

def andop():
    X = ram[PC] & int("111", 2)
    Y = (ram[PC+1] & int("11100000", 2)) >> 5
    memory[X] &= memory[Y]
    print(f"andop: r{X} &= r{Y}")

def orop():
    X = ram[PC] & int("111", 2)
    Y = (ram[PC+1] & int("11100000", 2)) >> 5
    memory[X] |= memory[Y]
    print(f"orop: r{X} |= r{Y}")

def xorop():
    X = ram[PC] & int("111", 2)
    Y = (ram[PC+1] & int("11100000", 2)) >> 5
    memory[X] ^= memory[Y]
    print(f"xorop: r{X} ^= r{Y}")

def store():
    X = ram[PC] & int("111", 2)
    ADDRESS = int.from_bytes(ram[PC+1:PC+3], byteorder='big')
    set_to_ram(ADDRESS, memory[X])
    print(f"store: RAM[{ADDRESS}] = r{X}")

def store2():
    X = ram[PC] & int("111", 2)
    Y = (ram[PC+1] & int("11100000", 2)) >> 5
    Z = ram[PC+1] & int("00011111", 2)
    if Z >= 0b10000:
        Z = Z - 0b100000
    set_to_ram(memory[Y] + Z, memory[X])
    print(f"store2: RAM[r{Y} + {Z}] = r{X}")

def div():
    X = ram[PC] & int("111", 2)
    Y = (ram[PC+1] & int("11100000", 2)) >> 5
    div_res = memory[X] // memory[Y]
    mod_res = memory[X] % memory[Y]
    memory[X] = div_res
    memory[Y] = mod_res
    print(f"div: r{X} /= r{Y}")
    print(f"div: r{X} %= r{Y}")

def comp():
    X = ram[PC] & int("111", 2)
    Y = (ram[PC+1] & int("11100000", 2)) >> 5

    print(f"comp: CMP r{X} ({memory[X]}), r{Y} ({memory[Y]})")

    X = memory[X]
    Y = memory[Y]
    global states
    states = []

    if X == Y:
        states.append("EQ")
    if X >= Y:
        states.append("GE")
    if X > Y:
        states.append("GT")
    if X <= Y:
        states.append("LE")
    if X < Y:
        states.append("LT")
    if X != Y:
        states.append("NE")

def jump():
    global PC
    C = ram[PC] & int("111", 2)
    ADDRESS = int.from_bytes(ram[PC+1:PC+3], byteorder='big')

    print(f"JMP {C} => {ADDRESS}")

    if (C == 0) or (C == 1 and "EQ" in states) or (C == 2 and "NE" in states) or (C == 3 and "LE" in states) or (C == 4 and "LT" in states) or (C == 5 and "GE" in states) or (C == 6 and "GT" in states):
        PC = ADDRESS
    else:
        PC += 3

def sub():
    X = ram[PC] & int("111", 2)
    Y = (ram[PC+1] & int("11100000", 2)) >> 5
    memory[X] -= memory[Y]
    print(f"r{X} -= r{Y}")

def push():
    X = ram[PC] & int("111", 2)
    set_to_ram(memory[7], memory[X])
    memory[7] -= 2
    print("push")

def pop():
    memory[7] += 2
    X = ram[PC] & int("111", 2)
    memory[X] = int.from_bytes(ram[memory[7]:memory[7] + 2], byteorder='big')
    print("pop")

def call():
    global PC
    set_to_ram(memory[7], PC + 3)
    memory[7] -= 2
    ADDRESS = int.from_bytes(ram[PC+1:PC+3], byteorder='big')
    PC = ADDRESS
    print("call")

def ret():
    global PC
    memory[7] += 2
    ADDRESS = int.from_bytes(ram[memory[7]:memory[7]+2], byteorder='big')
    PC = ADDRESS
    print("ret")

for count in range(2000):
    byte = f"{ram[PC]:08b}"

    print(f"{memory}, {states} - ", end="")
    # a = input("")
    # if a == "ram":
        # print(ram[0:1000])
    # print(ram[1:1000])

    if byte.startswith("00000"):
        load1()
        PC += 3
        continue
    if byte.startswith("00001"):
        load2()
        PC += 3
        continue
    if byte.startswith("00010"):
        load3()
        PC += 2
        continue
    if byte.startswith("01000"):
        add()
        PC += 2
        continue
    if byte.startswith("01010"):
        mul()
        PC += 2
        continue
    if byte.startswith("01011"):
        div()
        PC += 2
        continue
    if byte.startswith("10000"):
        comp()
        PC += 2
        continue
    if byte.startswith("10010"):
        jump()
        continue
    if byte.startswith("01001"):
        sub()
        PC += 2
        continue
    if byte.startswith("01100"):
        andop()
        PC += 2
        continue
    if byte.startswith("01101"):
        orop()
        PC += 2
        continue
    if byte.startswith("01110"):
        xorop()
        PC += 2
        continue
    if byte.startswith("00100"):
        store()
        PC += 3
        continue
    if byte.startswith("00101"):
        store2()
        PC += 2
        continue
    if byte.startswith("00011"):
        loadz()
        PC += 2
        continue
    if byte.startswith("11111"):
        print("BREAK, ", byte)
        print(count)
        break
    if byte.startswith("11000"):
        push()
        PC += 1
        continue
    if byte.startswith("11001"):
        pop()
        PC += 1
        continue
    if byte.startswith("10011"):
        call()
        continue
    if byte.startswith("10100"):
        ret()
        continue
    raise Exception(f"{byte} is not implemented")

index = memory[0]
while ram[index] != 0:
    print(chr(ram[index]), end="")
    index += 1
