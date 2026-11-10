import sys

DEST_TABLE = {
    "": "000", "M": "001", "D": "010", "MD": "011",
    "A": "100", "AM": "101", "AD": "110", "AMD": "111"
}

JUMP_TABLE = {
    "": "000", "JGT": "001", "JEQ": "010", "JGE": "011",
    "JLT": "100", "JNE": "101", "LE": "110", "JMP": "111"
}

COMP_TABLE = {
    "0": "0101010", "1": "0111111", "-1": "0111010",
    "D": "0001100", "A": "0110000", "!D": "0001101",
    "!A": "0110001", "-D": "0001111", "-A": "0110011",
    "D+1": "0011111", "A+1": "0110111", "D-1": "0001110",
    "A-1": "0110010", "D+A": "0000010", "D-A": "0010011",
    "A-D": "0000111", "D&A": "0000000", "D|A": "0010101",
    "M": "1110000", "!M": "1110001", "-M": "1110011",
    "M+1": "1110111", "M-1": "1110010", "D+M": "1000010",
    "D-M": "1010011", "M-D": "1000111", "D&M": "1000000",
    "D|M": "1010101"
}

class Assembler:
    def __init__(self):
        self.symbol_table = {
            f"R{i}": i for i in range(16)
        }
        self.symbol_table.update({
            "SP": 0, "LCL": 1, "ARG": 2, "THIS": 3, "THAT": 4,
            "SCREEN": 16384, "KBD": 24576
        })
        self.next_var_addr = 16

    def clean_line(self, line):
        line = line.split("//")[0].strip()
        return line

    def assemble(self, filename):
        with open(filename, 'r') as f:
            lines = f.readlines()

        cleaned_lines = []
        # Pass 1: Handle Labels
        rom_addr = 0
        for line in lines:
            code = self.clean_line(line)
            if not code:
                continue
            if code.startswith("(") and code.endswith(")"):
                label = code[1:-1]
                self.symbol_table[label] = rom_addr
            else:
                cleaned_lines.append(code)
                rom_addr += 1

        # Pass 2: Translate instructions
        binary_output = []
        for code in cleaned_lines:
            if code.startswith("@"):
                val = code[1:]
                if val.isdigit():
                    addr = int(val)
                else:
                    if val not in self.symbol_table:
                        self.symbol_table[val] = self.next_var_addr
                        self.next_var_addr += 1
                    addr = self.symbol_table[val]
                binary_output.append(f"0{addr:015b}")
            else:
                # C-Instruction parsing
                dest, comp, jump = "", "", ""
                if "=" in code:
                    dest, code = code.split("=")
                if ";" in code:
                    comp, jump = code.split(";")
                else:
                    comp = code

                c_bits = COMP_TABLE[comp]
                d_bits = DEST_TABLE[dest]
                j_bits = JUMP_TABLE[jump]
                binary_output.append(f"111{c_bits}{d_bits}{j_bits}")

        out_name = filename.rsplit('.', 1)[0] + ".hack"
        with open(out_name, 'w') as f:
            f.write("\n".join(binary_output) + "\n")
        print(f"Assembly completed successfully: Generated {out_name}")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        Assembler().assemble(sys.argv[1])
    else:
        print("Usage: python assembler.py <file.asm>")