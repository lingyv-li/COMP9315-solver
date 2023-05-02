def bit_wise_simc(page_descriptors, bit_slices, query_descriptor):
    b = len(page_descriptors)
    m = len(bit_slices)

    # Initialize matches to all ones
    matches = ~0

    for i in range(m):
        # Get i-th bit (from left to right)
        bit = query_descriptor & (1 << (m-i-1))
        if not bit:
            continue
        slice = bit_slices[i]
        matches = matches & slice
        print(f"matches = matches & bit_slices[{i}] = {bin(matches)}")

    # Initialize the list of potential matching pages to an empty list
    potential_pages = []

    for i in range(b):
        # Get i-th bit (from left to right)
        bit = matches & (1 << (b-i-1))
        if not bit:
            continue
        potential_pages.append(i)

    print(f"The pages that may contain matching tuples are: {potential_pages}")


if __name__ == '__main__':
    # Example from 22T1 exam Q8
    bit_wise_simc(
        page_descriptors=[
            0b0100010110,
            0b1000110010,
            0b0101010100,
            0b1010101010,
            0b0001111000,
            0b1111000000,
            0b1011000001,
            0b0100110100,
        ],
        bit_slices=[
            0b01010110,
            0b10100101,
            0b00010110,
            0b00101110,
            0b01011001,
            0b11101001,
            0b00011000,
            0b10100001,
            0b11010000,
            0b00000010,
        ],
        query_descriptor=0b0100010100,
    )
