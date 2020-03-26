"""CPU functionality.

Constructor method not filled out.
Load method filled out and straight forward from Monday class
Alu method ADD completed, needs the rest of the mathematical operations
Trace method filled out so print out cpu state, useful for debugging
Run method to be completed, will run the program from load
"""


## QUESTIONS FOR MATT
    # did I initialize ram and register correctly? 
    # Should HLT be a class variable?
    # Why do we need to convert into an int?
## END QUESTIONS

import sys


class CPU:
    """Main CPU class."""

    SP = 7
    # OP codes
    HLT = 0b00000001
    PRN = 0b01000111
    LDI = 0b10000010
    MUL = 0b10100010
    PUSH = 0b01000101
    POP = 0b01000110

    def __init__(self):
        """Construct a new CPU."""
        self.ram = [0] * 256
        self.register = [0] * 8
        self.pc = 0
        self.branchtable = {}

        # Insert OP codes into branchtable
        # Values point to f(x) for carrying out OP code
        self.branchtable[CPU.PRN] = self._handle_prn
        self.branchtable[CPU.LDI] = self._handle_ldi
        self.branchtable[CPU.PUSH] = self._handle_push
        self.branchtable[CPU.POP] = self._handle_pop

    def load(self):
        if len(sys.argv) < 2:
            print("Usage: ls8.py filename")
            sys.exit(1)

        filename = sys.argv[1]
        index = 0
        try:
            with open(filename) as f:

                for line in f:
                    command = line.split("#")[0].strip()
                    if command == "":
                        continue

                    num = int(command, 2)
                    self.ram[index] = num
                    index += 1

        except FileNotFoundError:
            print("File not found.")

    def handle_hlt(self):
        return (0, False)  

    def _handle_prn(self):
        reg_a = self.ram_read(self.pc + 1)
        print(self.register[reg_a])
        return (2, True)

    def _handle_ldi(self):
        reg_a = self.ram_read(self.pc + 1)
        reg_b = self.ram_read(self.pc + 2)
        print(f"reg_a {reg_a}, reg_b {reg_b}")
        self.register[reg_a] = reg_b
        return (3, True)

    def _handle_push(self):
        reg_a = self.ram_read(self.pc + 1)
        val = self.register[reg_a]

        self.register[CPU.SP] -= 1 % 255
        self.ram[self.register[CPU.SP]] = val

        return (2, True)

    def _handle_pop(self):
        reg_a = self.ram_read(self.pc + 1)
        val = self.ram[self.register[CPU.SP]]

        self.register[reg_a] = val
        self.register[CPU.SP] += 1

        return (2, True)

    def ram_read(self, index):
        return self.ram[index]

    def ram_write(self, index, value):
        self.ram[index] = value

    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.register[reg_a] += self.register[reg_b]
        # elif op == "SUB": etc
        elif op == CPU.MUL:
            self.register[reg_a] *= self.register[reg_b]
        else:
            raise Exception("Unsupported ALU operation")

    def trace(self):
        """
        Handy function to print out the CPU state. You might want to call this
        from run() if you need help debugging.
        """

        print(f"TRACE: %02X | %02X %02X %02X |" % (
            self.pc,
            # self.fl,
            # self.ie,
            self.ram_read(self.pc),
            self.ram_read(self.pc + 1),
            self.ram_read(self.pc + 2)
        ), end='')

        for i in range(8):
            print(" %02X" % self.reg[i], end='')

        print()

    def run(self):
        """Run the CPU."""
        running = True

        while running:
            ir = self.ram[self.pc]

            print("PC:", self.pc)
            print("IR:", ir)
            print("Program: ", self.ram[:32])
            print("Stack:", self.ram[240:])
            print("Register:", self.register)
            
            try:
                print(self.branchtable[ir]())
                output = self.branchtable[ir]()
                self.pc += output[0]
                running = output[1]
            
            except KeyError:
                print(f"ERROR: Instruction {ir} not recognized. Program exiting.")
                sys.exit(1)

    # def run(self):
    #     """Run the CPU."""
    #     running = True

    #     while running:
    #         ir = self.ram[self.pc]
    #         operand_a = self.ram_read(self.pc+1)
    #         operand_b = self.ram_read(self.pc+2)

    #         if ir == CPU.LDI:
    #             self._handle_ldi(operand_a, operand_b)

    #         elif ir == CPU.PRN:
    #             self._handle_prn(operand_a)

    #         elif ir == CPU.MUL:
    #             self.alu(CPU.MUL, operand_a, operand_b)
    #             self.pc += 3

    #         elif ir == CPU.HLT:
    #             running = False
            
    #         elif ir == CPU.PUSH:
    #             val = self.register[operand_a]
    #             self.register[CPU.SP] -= 1
    #             self.ram[self.register[CPU.SP]] = val
    #             self.pc += 2
            
    #         elif ir == CPU.POP:
    #             val = self.ram[self.register[CPU.SP]]
    #             self.register[operand_a] = val
    #             self.register[CPU.SP] += 1
    #             self.pc += 2

    #         else:
    #             print(f"ERROR: Instruction {ir} not recognized. Program exiting.")
    #             sys.exit(1)
