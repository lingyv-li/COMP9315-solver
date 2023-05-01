import dataclasses
from typing import Optional

@dataclasses.dataclass
class Page(list):
    next: Optional['Page']

    def __repr__(self) -> str:
        return f"{','.join(super().copy())}" + (f" -> {self.next}" if self.next else "")

    def all(self):
        yield self
        overflow = self.next
        while overflow:
            yield overflow
            overflow = overflow.next

    def has_space(self):
        return len(self) < C

    def insert(self, val):
        for Q in self.all():
            if Q.has_space():
                Q.append(val)
                return True
        return False

    def add_overflow(self, overflow: 'Page'):
        list(self.all())[-1].next = overflow


def bits(b, n):
    """
    Get b least significant bits from n.
    """
    return n & ((1 << b) - 1)


class LinearHash:
    def __init__(self, hash_func):
        self.sp = SP
        self.b = 2 ** D + self.sp
        self.d = D
        self.data: list[Page] = [Page(None) for _ in range(self.b)]
        self.hash_func = hash_func

    def debug(self):
        print(f'sp={self.sp}, d={self.d}')
        print("\n".join([f"[{bin(i)}] {cell}" for i, cell in enumerate(self.data)]))
        print()

    def get_page(self, pid: int):
        return self.data[pid]

    def select(self, val):
        hash_val = self.hash_func(val)
        pid = bits(self.d, hash_val)
        if (pid < self.sp):
            pid = bits(self.d+1, hash_val)
        P = self.get_page(pid)
        for page in P.all():
            if val in page:
                return val
        return None

    def insert(self, val):
        pid = bits(self.d, self.hash_func(val))
        if pid < self.sp:
            pid = bits(self.d+1, self.hash_func(val))
        # bucket P = page P + its overflow pages
        P = self.get_page(pid)
        if not P.insert(val):
            # add new ovflow page to bucket P
            new_ovflow = Page(None)
            P.add_overflow(new_ovflow)
            # insert tuple into new page
            new_ovflow.append(val)

    def split(self):
        # partition tuples between two buckets
        newp = self.sp + 2 ** self.d
        oldp = self.sp
        newP = Page(None)
        oldP = Page(None)
        for page in self.data[oldp].all():
            for t in page:
                p = bits(self.d+1, self.hash_func(t))
                if (p == newp):
                    P = newP
                else:
                    P = oldP
                if not P.insert(t):
                    # add new ovflow page to bucket P
                    new_ovflow = Page(None)
                    P.add_overflow(new_ovflow)
                    # insert tuple into new page
                    new_ovflow.append(t)
        self.data[oldp] = oldP
        self.data.append(newP)
        self.sp += 1
        if self.sp == 2 ** self.d:
            self.d += 1
            self.sp = 0


if __name__ == '__main__':
    # Example from exercise 9

    # Tuples per page
    C = 3
    # Initial depth of data file
    D = 2
    # Initial split pointer
    SP = 0

    def hash_func(val) -> int:
        return {
            'a': 0b10001,     'g': 0b00000,     'm': 0b11001,     's': 0b01110,
            'b': 0b11010,     'h': 0b00000,     'n': 0b01000,     't': 0b10011,
            'c': 0b01111,     'i': 0b10010,     'o': 0b00110,     'u': 0b00010,
            'd': 0b01111,     'j': 0b10110,     'p': 0b11101,     'v': 0b11111,
            'e': 0b01100,     'k': 0b00101,     'q': 0b00010,     'w': 0b10000,
            'f': 0b00010,     'l': 0b00101,     'r': 0b00000,     'x': 0b00111,
            'y': 0b11110,     'z': 0b01010,
        }[val]

    h = LinearHash(hash_func=hash_func)

    for i, c in enumerate(range(ord('a'), ord('z')+1)):
        print(f"inserting {i} {chr(c)}")
        h.insert(chr(c))

        # Split heuristic: e.g. split on 6-th insert
        need_to_split = i % 6 == 5
        if need_to_split:
            print("before split")
            h.debug()
            h.split()

        h.debug()
