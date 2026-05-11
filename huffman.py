"""
JPEG Huffman Encoding/Decoding

Uses Algorithm 1 and the default JPEG Huffman tables:
  - Table 1 (Luminance DC):  BITS = [0,1,5,1,1,1,1,1,1,0,0,0,0,0,0,0]
  - Table 2 (Luminance AC):  BITS = [0,2,1,3,3,2,4,3,5,5,4,4,0,0,1,125]

Usage:
    bitstream, tree = huffman.encode_huffman(rle_blocks)        # from rle.encode()
    rle_blocks      = huffman.decode_huffman(bitstream, tree)   # back to rle format
"""

import numpy as np

# ── Standard JPEG Huffman Tables ─────────────────────────────────────────

LUMINANCE_DC_BITS = [0, 1, 5, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0]
LUMINANCE_DC_HUFFVAL = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11]

LUMINANCE_AC_BITS = [0, 2, 1, 3, 3, 2, 4, 3, 5, 5, 4, 4, 0, 0, 1, 125]
LUMINANCE_AC_HUFFVAL = [
    0x01, 0x02,
    0x03,
    0x00, 0x04, 0x11,
    0x05, 0x12, 0x21,
    0x31, 0x41,
    0x06, 0x13, 0x51, 0x61,
    0x07, 0x22, 0x71,
    0x14, 0x32, 0x81, 0x91, 0xA1,
    0x08, 0x23, 0x42, 0xB1, 0xC1,
    0x15, 0x52, 0xD1, 0xF0,
    0x24, 0x33, 0x62, 0x72,
    0x82,
    0x09, 0x0A, 0x16, 0x17, 0x18, 0x19, 0x1A, 0x25,
    0x26, 0x27, 0x28, 0x29, 0x2A, 0x34, 0x35, 0x36,
    0x37, 0x38, 0x39, 0x3A, 0x43, 0x44, 0x45, 0x46,
    0x47, 0x48, 0x49, 0x4A, 0x53, 0x54, 0x55, 0x56,
    0x57, 0x58, 0x59, 0x5A, 0x63, 0x64, 0x65, 0x66,
    0x67, 0x68, 0x69, 0x6A, 0x73, 0x74, 0x75, 0x76,
    0x77, 0x78, 0x79, 0x7A, 0x83, 0x84, 0x85, 0x86,
    0x87, 0x88, 0x89, 0x8A, 0x92, 0x93, 0x94, 0x95,
    0x96, 0x97, 0x98, 0x99, 0x9A, 0xA2, 0xA3, 0xA4,
    0xA5, 0xA6, 0xA7, 0xA8, 0xA9, 0xAA, 0xB2, 0xB3,
    0xB4, 0xB5, 0xB6, 0xB7, 0xB8, 0xB9, 0xBA, 0xC2,
    0xC3, 0xC4, 0xC5, 0xC6, 0xC7, 0xC8, 0xC9, 0xCA,
    0xD2, 0xD3, 0xD4, 0xD5, 0xD6, 0xD7, 0xD8, 0xD9,
    0xDA, 0xE1, 0xE2, 0xE3, 0xE4, 0xE5, 0xE6, 0xE7,
    0xE8, 0xE9, 0xEA, 0xF1, 0xF2, 0xF3, 0xF4, 0xF5,
    0xF6, 0xF7, 0xF8, 0xF9, 0xFA,
]

# ── Generate Huffman Table ──────────────────────────────────────────────

def generate_huffman_table(bits, huffval):
    """
    Algorithm 1: Generate Huffman table from BITS and HUFFVAL.

        i = 0; code_value = 0
        for k = 1 to 16:
            for j = 1 to number_of_codeword[k]:
                codeword[i]   = code_value
                codelength[i] = k
                code_value++;  i++
            code_value *= 2
    """
    table = {}
    i = 0
    code_value = 0
    for k in range(1, 17):
        for _ in range(bits[k - 1]):
            table[huffval[i]] = (code_value, k)
            code_value += 1
            i += 1
        code_value <<= 1
    return table


DC_TABLE = generate_huffman_table(LUMINANCE_DC_BITS, LUMINANCE_DC_HUFFVAL)
AC_TABLE = generate_huffman_table(LUMINANCE_AC_BITS, LUMINANCE_AC_HUFFVAL)


# ── Helpers ──────────────────────────────────────────────────────────────

def _bits(code_int, length):
    return format(code_int, f'0{length}b')


def _category(value):
    """Return (category, additional_bits_string) for a coefficient value."""
    if value == 0:
        return 0, ''
    cat = int(np.floor(np.log2(abs(value)))) + 1
    if value > 0:
        extra = format(value, f'0{cat}b')
    else:
        extra = format(value - 1 + (1 << cat), f'0{cat}b')
    return cat, extra


# ── Encode ───────────────────────────────────────────────────────────────

def encode_huffman(rle_blocks):
    """
    Huffman-encode a list of RLE-encoded blocks (from rle.encode()).

    Args:
        rle_blocks: list of lists of (run, value) tuples.
                    First tuple per block is DC, rest are AC.

    Returns:
        bitstream (str): binary string of '0'/'1'.
        tree (dict):     decoding tables for decode_huffman().
    """
    bitstream = ''

    for block_rle in rle_blocks:
        for i, (run, value) in enumerate(block_rle):
            if i == 0:
                # ── DC: Huffman(category) + extra bits ──────────────
                cat, extra = _category(value)
                c, l = DC_TABLE[cat]
                bitstream += _bits(c, l) + extra
            else:
                # ── AC ──────────────────────────────────────────────
                # EOB
                if run == 0 and value == 0:
                    c, l = AC_TABLE[0x00]
                    bitstream += _bits(c, l)
                # ZRL
                elif run == 15 and value == 0:
                    c, l = AC_TABLE[0xF0]
                    bitstream += _bits(c, l)
                # Normal AC: Huffman(run/size) + extra bits
                else:
                    cat, extra = _category(value)
                    symbol = (run << 4) | cat
                    c, l = AC_TABLE[symbol]
                    bitstream += _bits(c, l) + extra

    tree = {
        'dc': {_bits(c, l): s for s, (c, l) in DC_TABLE.items()},
        'ac': {_bits(c, l): s for s, (c, l) in AC_TABLE.items()},
    }
    return bitstream, tree


# ── Decode ───────────────────────────────────────────────────────────────

def _read_extra(bitstream, pos, cat):
    if cat == 0:
        return 0, pos
    bits = bitstream[pos:pos + cat]
    pos += cat
    val = int(bits, 2)
    if bits[0] == '0':
        val = val - (1 << cat) + 1
    return val, pos


def decode_huffman(bitstream, tree):
    """
    Decode a Huffman-encoded bitstream back into RLE blocks (for rle.decode()).

    Args:
        bitstream (str): encoded binary string.
        tree (dict):     decode tables from encode_huffman().

    Returns:
        list of lists: per-block (run, value) tuples, same format as rle.encode() output.
    """
    dc_decode = tree['dc']
    ac_decode = tree['ac']

    rle_blocks = []
    pos = 0

    while pos < len(bitstream):
        block_rle = []

        # ── DC ───────────────────────────────────────────────────────
        buf = ''
        while pos < len(bitstream):
            buf += bitstream[pos]; pos += 1
            if buf in dc_decode:
                break
        cat = dc_decode[buf]
        dc_val, pos = _read_extra(bitstream, pos, cat)
        block_rle.append((0, dc_val))

        coeff_count = 1

        # ── AC ───────────────────────────────────────────────────────
        while coeff_count < 64:
            buf = ''
            while pos < len(bitstream):
                buf += bitstream[pos]; pos += 1
                if buf in ac_decode:
                    break

            symbol = ac_decode[buf]
            run  = (symbol >> 4) & 0x0F
            size = symbol & 0x0F

            if symbol == 0x00:          # EOB
                block_rle.append((0, 0))
                break

            if symbol == 0xF0:          # ZRL
                block_rle.append((15, 0))
                coeff_count += 16
                continue

            ac_val, pos = _read_extra(bitstream, pos, size)
            block_rle.append((run, ac_val))
            coeff_count += run + 1

        rle_blocks.append(block_rle)

    return rle_blocks