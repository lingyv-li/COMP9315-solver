from typing import Optional

def bit(b, num):
    """
    Get b-th bit in num.
    """
    return (num & 1 << b) >> b

def composite_hash(hashes: list[Optional[int]], cv: list[tuple[int, int]], d: int):
    """
    hashes: hash for each attr
    cv: choice vector
    d: number of digits of a hash
    """
    res = ""
    print("val\texplaination")
    for i in range(d):
        a = cv[i][0] # attr
        b = cv[i][1] # bit
        if hashes[a] is not None:
            one_bit = bit(b, hashes[a])
            res = str(one_bit) + res
            print(f'{one_bit}\tfrom {b}-th bit of attr {a}')
        else:
            res = '*' + res
            print(f'*\tfrom {b}-th bit of attr {a} (hash not specified)')
    return res

if __name__ == '__main__':
    # Example from exercise 6.
    res = composite_hash(
        hashes=[
            None,  # If the attribute index is 1-based, comment out if it's 0-based.
            0b0101010110110100,
            # 0b1011111101101111,
            None, # For partial 
            0b0001001011000000,
        ],
        cv=[(1, 0), (1, 1), (2, 0), (3, 0), (1, 2), (2, 1), (3, 1), (1, 3)],
        d=6,
    )
    print(f"composite hash: {res}")
