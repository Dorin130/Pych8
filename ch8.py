import re

import numpy as np
import display
from font import font

# ignore all numpy runtime errors (like overflows)
np.seterr(all='ignore')

"""
More info: https://en.wikipedia.org/wiki/CHIP-8#Opcode_table
"""

opcodes = (
    (r'00ee'                                , 'return;'                         , 'f_00EE'),
    (r'00e0'                                , 'disp_clear()'                    , 'f_00E0'),
    (r'(?P<a>0[0-9a-f]{3})'                 , ''                                , 'f_0NNN'),
    (r'1(?P<a>[0-9a-f]{3})'                 , 'goto 0x0{a};'                    , 'f_1NNN'),
    (r'2(?P<a>[0-9a-f]{3})'                 , '*(0x0{a})()'                     , 'f_2NNN'),
    (r'3(?P<x>[0-9a-f])(?P<c>[0-9a-f]{2})'  , 'if(V{x}=={c})'                   , 'f_3XNN'),
    (r'4(?P<x>[0-9a-f])(?P<c>[0-9a-f]{2})'  , 'if(V{x}!={c})'                   , 'f_4XNN'),
    (r'5(?P<x>[0-9a-f])(?P<y>[0-9a-f])0'    , 'if(V{x}==V{y})'                  , 'f_5XY0'),
    (r'6(?P<x>[0-9a-f])(?P<c>[0-9a-f]{2})'  , 'V{x}={c}'                        , 'f_6XNN'),
    (r'7(?P<x>[0-9a-f])(?P<c>[0-9a-f]{2})'  , 'V{x}+={c}'                       , 'f_7XNN'),
    (r'8(?P<x>[0-9a-f])(?P<y>[0-9a-f])0'    , 'V{x}=V{y}'                       , 'f_8XY0'),
    (r'8(?P<x>[0-9a-f])(?P<y>[0-9a-f])1'    , 'V{x}=V{x}|V{y}'                  , 'f_8XY1'),
    (r'8(?P<x>[0-9a-f])(?P<y>[0-9a-f])2'    , 'V{x}=V{x}&V{y}'                  , 'f_8XY2'),
    (r'8(?P<x>[0-9a-f])(?P<y>[0-9a-f])3'    , 'V{x}=V{x}^V{y}'                  , 'f_8XY3'),
    (r'8(?P<x>[0-9a-f])(?P<y>[0-9a-f])4'    , 'V{x}+=V{y} '                     , 'f_8XY4'),
    (r'8(?P<x>[0-9a-f])(?P<y>[0-9a-f])5'    , 'V{x}-=V{y}'                      , 'f_8XY5'),
    (r'8(?P<x>[0-9a-f])(?P<y>[0-9a-f])6'    , 'V{x}>>=1'                        , 'f_8XY6'),
    (r'8(?P<x>[0-9a-f])(?P<y>[0-9a-f])7'    , 'V{x}=V{y}-V{x}'                  , 'f_8XY7'),
    (r'8(?P<x>[0-9a-f])(?P<y>[0-9a-f])e'    , 'V{x}<<=1 '                       , 'f_8XYE'),
    (r'9(?P<x>[0-9a-f])(?P<y>[0-9a-f])0'    , 'if(V{x}!=V{y})'                  , 'f_9XY0'),
    (r'a(?P<a>[0-9a-f]{3})'                 , 'I=0x0{a}'                        , 'f_ANNN'),
    (r'b(?P<a>[0-9a-f]{3})'                 , 'PC=V0+0x0{a}'                    , 'f_BNNN'),
    (r'c(?P<x>[0-9a-f])(?P<c>[0-9a-f]{2})'  , 'V{x}=rand()&{c}'                 , 'f_CXNN'),
    (r'd(?P<x>[0-9a-f])(?P<y>[0-9a-f])(?P<h>[0-9a-f])', 'draw(V{x},V{y},{h})'   , 'f_DXYN'),
    (r'e(?P<x>[0-9a-f])9e'                  , 'if(key()==V{x})'                 , 'f_EX9E'),
    (r'e(?P<x>[0-9a-f])a1'                  , 'if(key()!=V{x})'                 , 'f_EXA1'),
    (r'f(?P<x>[0-9a-f])07'                  , 'V{x} = get_delay()'              , 'f_FX07'),
    (r'f(?P<x>[0-9a-f])0a'                  , 'V{x} = get_key() '               , 'f_FX0A'),
    (r'f(?P<x>[0-9a-f])15'                  , 'delay_timer(V{x})'               , 'f_FX15'),
    (r'f(?P<x>[0-9a-f])18'                  , 'sound_timer(V{x})'               , 'f_FX18'),
    (r'f(?P<x>[0-9a-f])1e'                  , 'I+=V{x}'                         , 'f_FX1E'),
    (r'f(?P<x>[0-9a-f])29'                  , 'I=sprite_addr[V{x}]'             , 'f_FX29'),
    (r'f(?P<x>[0-9a-f])33'                  , 'set_BCD(V{x})'                   , 'f_FX33'),
    (r'f(?P<x>[0-9a-f])55'                  , 'reg_dump(V{x},&I)'               , 'f_FX55'),
    (r'f(?P<x>[0-9a-f])65'                  , 'reg_load(Vx,&I)'                 , 'f_FX65'),
)


def get_inst(byte_str, ops=opcodes):
    for pattern, note, fname in ops:
        match = re.search(pattern, byte_str)
        if match:
            return fname, match.groupdict()


class Ch8State:
    def __init__(self):
        self.V = np.zeros(16, dtype='uint8')
        self.I = np.uint16()
        self.SP = np.uint8()
        self.PC = np.uint16(0x200)
        self.delay = np.uint8()
        self.sound = np.uint8()
        self.display = display.Display()

        self.ram = np.zeros(4096, dtype='uint8')
        self.stack = np.zeros(16, dtype='uint16')

        # initialize the font
        i = 0
        for char in font:
            for byte in np.packbits(char):
                self.ram[i] = byte
                i += 1

    def load_ram(self, filename):
        code = np.fromfile(filename, dtype='uint8')
        self.ram[0x200: 0x200 + len(code)] = code

    def step(self):
        instr = "{0:02x}{1:02x}".format(*self.ram[self.PC:self.PC + 2])
        func, args = get_inst(instr)
        self.PC += np.uint16(2)
        getattr(self, func)(**{k: int(v, 16) for k, v in args.items()})
        print(func, args)

    """
    00E0 - CLS
    Clear the display.  
    """
    def f_00E0(self, **kwargs):
        self.display.clear()
        print('Clear Screen!')

    """
    00EE - RET
    Return from a subroutine.

    The interpreter sets the program counter to the address at the top of the stack, then subtracts 1 from the stack pointer.
    """
    def f_00EE(self, **kwargs):
        self.PC = np.uint16(self.stack[self.SP])
        self.SP -= np.uint16(1)

    """
    0nnn - SYS addr
    Jump to a machine code routine at nnn.
    
    This instruction is only used on the old computers on which Chip-8 was originally implemented. It is ignored by modern interpreters.
    """
    def f_0NNN(self, **kwargs):
        print('syscall', kwargs)

    """
    1nnn - JP addr
    Jump to location nnn.
    
    The interpreter sets the program counter to nnn.
    """
    def f_1NNN(self, **kwargs):
        self.PC = np.uint16(kwargs['a'])

    """
    2nnn - CALL addr
    Call subroutine at nnn.
    
    The interpreter increments the stack pointer, then puts the currimportent PC on the top of the stack. The PC is then set to nnn.
    """
    def f_2NNN(self, **kwargs):
        self.SP += np.uint8(1)
        self.stack[self.SP] = np.uint16(self.PC)
        self.PC = np.uint16(kwargs['a'])

    """
    3xkk - SE Vx, byte
    Skip next instruction if Vx = kk.
    (c = kk)
    The interpreter compares register Vx to kk, and if they are equal, increments the program counter by 2.
    """
    def f_3XNN(self, **kwargs):
        if self.V[kwargs['x']] == np.uint8(kwargs['c']):
            self.PC += np.uint16(2)

    """
    4xkk - SNE Vx, byte
    Skip next instruction if Vx != kk.
    (c=kk)
    The interpreter compares register Vx to kk, and if they are not equal, increments the program counter by 2.
    """
    def f_4XNN(self, **kwargs):
        if self.V[kwargs['x']] != np.uint8(kwargs['c']):
            self.PC += np.uint16(2)

    """
    5xy0 - SE Vx, Vy
    Skip next instruction if Vx = Vy.
    
    The interpreter compares register Vx to register Vy, and if they are equal, increments the program counter by 2.
    """
    def f_5XY0(self, **kwargs):
        if self.V[kwargs['x']] == self.V[kwargs['y']]:
            self.PC += np.uint16(2)

    """
    6xkk - LD Vx, byte
    Set Vx = kk.
    (c=kk)
    The interpreter puts the value kk into register Vx.
    """
    def f_6XNN(self, **kwargs):
        self.V[kwargs['x']] = np.uint8(kwargs['c'])

    """
    7xkk - ADD Vx, byte
    Set Vx = Vx + kk.
    (c=kk)
    Adds the value kk to the value of register Vx, then stores the result in Vx. 
    """
    def f_7XNN(self, **kwargs):
        self.V[kwargs['x']] += np.uint8(kwargs['c'])

    """
    8xy0 - LD Vx, Vy
    Set Vx = Vy.
    
    Stores the value of register Vy in register Vx.    
    """
    def f_8XY0(self, **kwargs):
        self.V[kwargs['x']] = self.V[kwargs['y']]

    """
    8xy1 - OR Vx, Vy
    Set Vx = Vx OR Vy.
    
    Performs a bitwise OR on the values of Vx and Vy, then stores the result in Vx. A bitwise OR compares the corrseponding 
    bits from two values, and if either bit is 1, then the same bit in the result is also 1. Otherwise, it is 0.
    """
    def f_8XY1(self, **kwargs):
        self.V[kwargs['x']] |= self.V[kwargs['y']]

    """
    8xy2 - AND Vx, Vy
    Set Vx = Vx AND Vy.
    
    Performs a bitwise AND on the values of Vx and Vy, then stores the result in Vx. A bitwise AND compares the corrseponding
    bits from two values, and if both bits are 1, then the same bit in the result is also 1. Otherwise, it is 0.
    """
    def f_8XY2(self, **kwargs):
        self.V[kwargs['x']] &= self.V[kwargs['y']]

    """
    
    8xy3 - XOR Vx, Vy
    Set Vx = Vx XOR Vy.
    
    Performs a bitwise exclusive OR on the values of Vx and Vy, then stores the result in Vx. An exclusive OR compares the corrseponding
    bits from two values, and if the bits are not both the same, then the corresponding bit in the result is set to 1. Otherwise, it is 0. 
    """
    def f_8XY3(self, **kwargs):
        self.V[kwargs['x']] ^= self.V[kwargs['y']]

    """
    8xy4 - ADD Vx, Vy
    Set Vx = Vx + Vy, set VF = carry.
    
    The values of Vx and Vy are added together. If the result is greater than 8 bits (i.e., > 255,) VF is set to 1, otherwise 0.
    Only the lowest 8 bits of the result are kept, and stored in Vx.
    """
    def f_8XY4(self, **kwargs):
        self.V[0xf] = np.uint8(1) if int(self.V[kwargs['x']]) + int(self.V[kwargs['y']]) > 255 else np.uint8(0)
        self.V[kwargs['x']] += self.V[kwargs['y']]

    """
    8xy5 - SUB Vx, Vy
    Set Vx = Vx - Vy, set VF = NOT borrow.
    
    If Vx > Vy, then VF is set to 1, otherwise 0. Then Vy is subtracted from Vx, and the results stored in Vx.
    """
    def f_8XY5(self, **kwargs):
        self.V[0xf] = np.uint8(1) if self.V[kwargs['x']] > self.V[kwargs['y']] else np.uint8(0)
        self.V[kwargs['x']] -= self.V[kwargs['y']]

    """
    8xy6 - SHR Vx {, Vy}
    Set Vx = Vx SHR 1.
    
    If the least-significant bit of Vx is 1, then VF is set to 1, otherwise 0. Then Vx is divided by 2.
    """
    def f_8XY6(self, **kwargs):
        self.V[0xf] = self.V[kwargs['x']] & np.uint8(0x1)
        self.V[kwargs['x']] >>= np.uint8(0x1)

    """
    8xy7 - SUBN Vx, Vy
    Set Vx = Vy - Vx, set VF = NOT borrow.
    
    If Vy > Vx, then VF is set to 1, otherwise 0. Then Vx is subtracted from Vy, and the results stored in Vx.
    """
    def f_8XY7(self, **kwargs):
        self.V[0xf] = np.uint8(1) if self.V[kwargs['y']] > self.V[kwargs['x']] else np.uint8(0)
        self.V[kwargs['x']] = self.V[kwargs['y']] - self.V[kwargs['x']]

    """
    8xyE - SHL Vx {, Vy}
    Set Vx = Vx SHL 1.
    
    If the most-significant bit of Vx is 1, then VF is set to 1, otherwise to 0. Then Vx is multiplied by 2.
    """
    def f_8XYE(self, **kwargs):
        self.V[0xf] = self.V[kwargs['x']] >> np.uint8(7)
        self.V[kwargs['x']] <<= np.uint8(1)

    """
    9xy0 - SNE Vx, Vy
    Skip next instruction if Vx != Vy.
    
    The values of Vx and Vy are compared, and if they are not equal, the program counter is increased by 2.
    """
    def f_9XY0(self, **kwargs):
        if self.V[kwargs['x']] != self.V[kwargs['y']]:
            self.PC += np.uint16(2)

    """
    Annn - LD I, addr
    Set I = nnn.
    (a=nnn)
    The value of register I is set to nnn.
    """
    def f_ANNN(self, **kwargs):
        self.I = np.uint16(kwargs['a'])

    """
    Bnnn - JP V0, addr
    Jump to location nnn + V0.
    
    The program counter is set to nnn plus the value of V0.
    """
    def f_BNNN(self, **kwargs):
        self.PC = np.uint16(kwargs['a']) + np.uint16(self.V[0x0])

    """
    Cxkk - RND Vx, byte
    Set Vx = random byte AND kk.
    (c=kk)
    The interpreter generates a random number from 0 to 255, which is then ANDed with the value kk. The results are stored
     in Vx. See instruction 8xy2 for more information on AND.
    """
    def f_CXNN(self, **kwargs):
        self.V[kwargs['x']] = np.random.randint(0xff, dtype='uint8') & np.uint8(kwargs['c'])

    """
    Dxyn - DRW Vx, Vy, nibble
    Display n-byte sprite starting at memory location I at (Vx, Vy), set VF = collision.
    
    The interpreter reads n bytes from memory, starting at the address stored in I. These bytes are then displayed as sprites 
    on screen at coordinates (Vx, Vy). Sprites are XORed onto the existing screen. If this causes any pixels to be erased,
    VF is set to 1, otherwise it is set to 0. If the sprite is positioned so part of it is outside the coordinates of the 
    display, it wraps around to the opposite side of the screen. See instruction 8xy3 for more information on XOR, and 
    section 2.4, Display, for more information on the Chip-8 screen and sprites."""
    def f_DXYN(self, **kwargs):
        data = np.unpackbits(self.ram[self.I:self.I + kwargs['h']]).astype(bool).reshape((kwargs['h'],8))
        self.V[0xf] = np.uint8(1) if self.display.draw(kwargs['x'], kwargs['y'], data) else np.uint8(0)

    """
    Ex9E - SKP Vx
    Skip next instruction if key with the value of Vx is pressed.
    
    Checks the keyboard, and if the key corresponding to the value of Vx is currently in the down position,
    PC is increased by 2.
    """
    def f_EX9E(self, **kwargs):
        pass

    """
    ExA1 - SKNP Vx
    Skip next instruction if key with the value of Vx is not pressed.
    
    Checks the keyboard, and if the key corresponding to the value of Vx is currently in the up position, PC is increased by 2.
    """
    def f_EXA1(self, **kwargs):
        pass

    """
    Fx07 - LD Vx, DT
    Set Vx = delay timer value.
    
    The value of DT is placed into Vx.
    """
    def f_FX07(self, **kwargs):
        pass

    def f_FX0A(self, **kwargs):
        pass

    def f_FX15(self, **kwargs):
        pass

    def f_FX18(self, **kwargs):
        pass

    def f_FX1E(self, **kwargs):
        pass

    def f_FX29(self, **kwargs):
        pass

    def f_FX33(self, **kwargs):
        pass

    def f_FX55(self, **kwargs):
        pass

    def f_FX65(self, **kwargs):
        pass

    def f_1NNN(self, **kwargs):
        pass
