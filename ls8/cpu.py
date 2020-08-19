"""CPU functionality."""

import sys

class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.ram = [0] * 256
        self.reg = [0] * 8
        self.pc = 0
        self.sp = 7
        self.op_size = 1
        self.running = True

        # branchtable
        self.branchtable = {
            0b00000001: self.HLT,
            0b10000010: self.LDI,
            0b01000111: self.PRN,
            0b10100000: self.ADD,
            0b10100010: self.MUL,
            0b01000101: self.PUSH,
            0b01000110: self.POP
        }
        # self.HLT = 0b00000001
        # self.LDI = 0b10000010
        # self.PRN = 0b01000111
        # self.ADD = 0b10100000
        # self.MUL = 0b10100010
        # implement push and pop to implement stack day 3
        # self.PUSH = 0b01000101
        # self.POP = 0b01000110

    def ram_read(self, MAR):
        return self.ram[MAR]
    
    def ram_write(self, MAR, MDR):
        self.ram[MAR] =  MDR

    # operation methods
    def HLT(self, operand_a, operand_b):
        self.running = False
        self.pc += 1
    def LDI(self, operand_a, operand_b):
        self.reg[operand_a] = operand_b
        self.pc += 3
    def PRN(self, operand_a, operand_b):
        num = self.reg[int(str(operand_a))]
        print(num)
        self.pc += 2
    def ADD(self, operand_a, operand_b):
        self.alu("ADD", operand_a, operand_b)
        self.pc += 3
    def MUL(self, operand_a, operand_b):
        self.alu("MUL", operand_a, operand_b)
        self.pc += 3
    def PUSH(self, operand_a, operand_b):
        # set up, grap reg_index from memory and grab the value from reg
        reg_index = self.ram[self.pc + 1]
        value = self.reg[reg_index]
        # decrement the pointer
        self.reg[reg_index] -= 1
        # insert the value onto the stack, find the value of the SP in RAM
        self.ram[self.reg[self.sp]] = value
        # two ops
        self.pc += 2
    def POP(self, operand_a, operand_b):
        # set up, grab reg index from memory, set val with the SP in ram
        reg_index = self.ram[self.pc + 1]
        value = self.ram[self.reg[self.sp]]

        # take the value from the stack and put it in reg
        self.reg[reg_index] = value

        # increment SP
        self.reg[self.sp] += 1

        # two ops
        self.pc += 2

    def load(self, filename):
        """Load a program into memory."""

        try:
            address = 0
            with open(filename) as f:
                for line in f:
                    split_comment = line.split("#")
                    # strip the whitespace and other chars
                    n = split_comment[0].strip()
                    if n == '':
                        continue
                    value = int(n, 2)
                    self.ram[address] = value
                    address += 1
        except FileNotFoundError:
            print(f"{sys.argv[0]}: {filename} not found")

    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
        elif op == "MUL":
            self.reg[reg_a] *= self.reg[reg_b]
        #elif op == "SUB": etc
        else:
            raise Exception("Unsupported ALU operation")

    def trace(self):
        """
        Handy function to print out the CPU state. You might want to call this
        from run() if you need help debugging.
        """

        print(f"TRACE: %02X | %02X %02X %02X |" % (
            self.pc,
            #self.fl,
            #self.ie,
            self.ram_read(self.pc),
            self.ram_read(self.pc + 1),
            self.ram_read(self.pc + 2)
        ), end='')

        for i in range(8):
            print(" %02X" % self.reg[i], end='')

        print()

    def run(self):
        """Run the CPU."""
        # FETCH, DECODE, EXECUTE
        self.trace()

        while self.running:
            IR = self.ram_read(self.pc)
            operand_a = self.ram_read(self.pc + 1)
            operand_b = self.ram_read(self.pc + 2)

            self.branchtable[IR](operand_a, operand_b)

            # if IR == self.ADD:
            #     self.alu("ADD", operand_a, operand_b)
            #     self.pc += 3
            # if IR == self.MUL:
            #     self.alu("MUL", operand_a, operand_b)
            #     self.pc += 3
            # elif IR == self.HLT:
            #     self.running = False
            #     self.pc += 1
            # elif IR == self.LDI:
            #     self.reg[operand_a] = operand_b
            #     self.pc += 3
            # elif IR == self.PRN:
            #     num = self.reg[int(str(operand_a))]
            #     print(num)
            #     self.pc += 2
            # elif IR == self.PUSH:
            #     # set up, grap reg_index from memory and grab the value from reg
            #     reg_index = self.ram[self.pc + 1]
            #     value = self.reg[reg_index]
            #     # decrement the pointer
            #     self.reg[reg_index] -= 1
            #     # insert the value onto the stack, find the value of the SP in RAM
            #     self.ram[self.reg[self.sp]] = value
            #     # two ops
            #     self.pc += 2

            # elif IR == self.POP:
            #     # set up, grab reg index from memory, set val with the SP in ram
            #     reg_index = self.ram[self.pc + 1]
            #     value = self.ram[self.reg[self.sp]]

            #     # take the value from the stack and put it in reg
            #     self.reg[reg_index] = value

            #     # increment SP
            #     self.reg[self.sp] += 1

            #     # two ops
            #     self.pc += 2


