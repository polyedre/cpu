JMP main
LOAD r6, 0
JMP fail

main:
# JUMP TESTS
LOAD r0, 0x10
LOAD r1, 0x10
CMP r0, r1
LOAD r6, 0x1
JMP.NE fail
LOAD r6, 0x2
JMP.LT fail
LOAD r6, 0x3
JMP.GT fail

LOAD r0, 0x10
LOAD r1, 0x9
CMP r0, r1
LOAD r6, 5
JMP.EQ fail
LOAD r6, 6
JMP.LE fail
CMP r1, r0
LOAD r6, 7
JMP.GE fail

# ARITHMETIC TESTS
LOAD r0, 0x10
LOAD r1, 0x2
ADD r0, r1
LOAD r1, 0x12
CMP r0, r1
LOAD r6, 8
JMP.NE fail

LOAD r0, 0x10
LOAD r1, 0x2
SUB r0, r1
LOAD r1, 0xE
CMP r0, r1
LOAD r6, 9
JMP.NE fail

LOAD r0, 0x10
LOAD r1, 0x2
MUL r0, r1
LOAD r1, 0x20
CMP r0, r1
LOAD r6, 10
JMP.NE fail

LOAD r0, 0x11
LOAD r1, 0x2
DIV r0, r1
LOAD r2, 0x8
CMP r0, r2
LOAD r6, 11
JMP.NE fail
LOAD r2, 0x1
CMP r1, r2
LOAD r6, 12
JMP.NE fail

LOAD r0, 0x11
LOAD r1, 0xF0
AND r0, r1
LOAD r1, 0x10
CMP r0, r1
LOAD r6, 13
JMP.NE fail

LOAD r0, 0x11
LOAD r1, 0xF0
OR r0, r1
LOAD r1, 0xF1
CMP r0, r1
LOAD r6, 14
JMP.NE fail

LOAD r0, 0x11
LOAD r1, 0xF0
XOR r0, r1
LOAD r1, 0xE1
CMP r0, r1
LOAD r6, 15
JMP.NE fail

# MEMORY TESTS
LOAD r0, 0xAAAA
STORE r0, [0x8000]
LOAD r1, [0x8000]
CMP r0, r1
LOAD r6, 16
JMP.NE fail

LOAD r0, 0xBBBB
LOAD r1, 0x8000
STORE r0, [r1]
LOAD r2, [r1]
CMP r0, r2
LOAD r6, 17
JMP.NE fail

LOAD r0, 0xAAAA
LOAD r1, 0x8000
STORE r0, [r1]
LOAD r0, 0xBBBB
LOAD r1, 0x8002
STORE r0, [r1]
LOAD r0, 0xCCCC
LOAD r1, 0x8004
STORE r0, [r1]
LOAD r0, 0x8002
LOAD r1, [r0-2]
LOAD r2, 0xAAAA
CMP r1, r2
LOAD r6, 18
JMP.NE fail
LOAD r1, [r0+2]
LOAD r2, 0xCCCC
CMP r1, r2
LOAD r6, 19
JMP.NE fail

LOAD r0, 0xAAAA
LOAD r1, 0x9000
STORE r0, [r1-2]
LOAD r0, 0xBBBB
STORE r0, [r1]
LOAD r0, 0xCCCC
STORE r0, [r1+2]
LOAD r1, [0x8FFE]
LOAD r2, 0xAAAA
CMP r1, r2
LOAD r6, 20
JMP.NE fail
LOAD r1, [0x9002]
LOAD r2, 0xCCCC
CMP r1, r2
LOAD r6, 21
JMP.NE fail

# STACK TESTS
LOAD r0, 0x10
PUSH r0
POP r1
CMP r0, r1
LOAD r6, 23
JMP.NE fail

# CALL TESTS
CALL callTest
LOAD r1, 0xBEEF
CMP r0, r1
LOAD r6, 22
JMP.NE fail

success:
LOAD r0, 0xCAFE
BREAK

callTest:
LOAD r0, 0xBEEF
RET

fail:
LOAD r0, r6
BREAK