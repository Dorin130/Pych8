import re

from opcodes import opcodes


class Memory:
    _bytes = None

    def load_ch8(self, filename):
        with open(filename, 'rb') as f:
            self._bytes = f.read()

    def disassemble(self):
        addr = 0x0200
        print("ADDR  : HEX : NOTES")
        for i in range(0, len(self._bytes), 2):
            word = self._bytes[i:i + 2]
            for pattern, note in opcodes:
                match = re.search(pattern, word.hex())
                if match:
                    break
            if match:
                print('{0:#06x}: {1}: {2}'.format(addr + i, word.hex(), note.format(**match.groupdict())))
            else:
                print('{0:#06x}: {1}: '.format(addr + i, word.hex()))
