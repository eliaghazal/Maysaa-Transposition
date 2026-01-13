"""
Columnar Transposition Cipher Implementation
Supports encryption and decryption with numeric and keyword-based keys
Handles text with or without spaces
"""

import math
from typing import List, Tuple


def keyword_to_numeric(keyword: str) -> str:
    """
    Convert a keyword to numeric key based on alphabetical order.
    Example: "SECRET" -> "351624"
    """
    # Create list of (char, original_index) tuples
    indexed_chars = [(char.upper(), i) for i, char in enumerate(keyword)]
    # Sort by character
    sorted_chars = sorted(indexed_chars, key=lambda x: x[0])
    # Assign numbers based on sorted order
    numeric_key = ['0'] * len(keyword)
    for rank, (char, original_idx) in enumerate(sorted_chars, start=1):
        numeric_key[original_idx] = str(rank)
    return ''.join(numeric_key)


def validate_key(key: str) -> bool:
    """
    Validate that a key is either numeric or alphabetic.
    """
    if not key:
        return False
    # Check if numeric key (digits only)
    if key.isdigit():
        # Must contain consecutive numbers from 1 to len(key)
        key_set = set(key)
        expected_set = set(str(i) for i in range(1, len(key) + 1))
        return key_set == expected_set
    # Check if alphabetic keyword
    return key.isalpha()


def normalize_key(key: str) -> str:
    """
    Normalize key to numeric format.
    If already numeric, return as is. If alphabetic, convert to numeric.
    """
    if not validate_key(key):
        raise ValueError(f"Invalid key: {key}")
    
    if key.isdigit():
        return key
    else:
        return keyword_to_numeric(key)


def encrypt(plaintext: str, key: str, keep_spaces: bool = False) -> str:
    """
    Encrypt plaintext using columnar transposition cipher.
    
    Args:
        plaintext: Text to encrypt
        key: Numeric key (e.g., "3142") or keyword (e.g., "SECRET")
        keep_spaces: If True, preserve spaces in ciphertext
        
    Returns:
        Encrypted ciphertext
    """
    # Normalize key to numeric format
    numeric_key = normalize_key(key)
    key_length = len(numeric_key)
    
    # Remove spaces from plaintext if not keeping them
    if not keep_spaces:
        plaintext = plaintext.replace(' ', '')
    
    # Calculate padding needed
    num_rows = math.ceil(len(plaintext) / key_length)
    total_chars = num_rows * key_length
    padding_needed = total_chars - len(plaintext)
    
    # Add padding with 'X'
    padded_text = plaintext + 'X' * padding_needed
    
    # Create the transposition matrix
    matrix = []
    for i in range(num_rows):
        row = []
        for j in range(key_length):
            idx = i * key_length + j
            if idx < len(padded_text):
                row.append(padded_text[idx])
            else:
                row.append('X')
        matrix.append(row)
    
    # Read columns in key order
    ciphertext = ''
    # Convert key to column order (1-indexed to 0-indexed)
    for col_num in range(1, key_length + 1):
        col_idx = numeric_key.index(str(col_num))
        for row in matrix:
            ciphertext += row[col_idx]
    
    return ciphertext


def decrypt(ciphertext: str, key: str) -> str:
    """
    Decrypt ciphertext using columnar transposition cipher.
    
    Args:
        ciphertext: Text to decrypt
        key: Numeric key (e.g., "3142") or keyword (e.g., "SECRET")
        
    Returns:
        Decrypted plaintext (with padding removed)
    """
    # Normalize key to numeric format
    numeric_key = normalize_key(key)
    key_length = len(numeric_key)
    
    # Calculate dimensions
    num_rows = math.ceil(len(ciphertext) / key_length)
    
    # Create empty matrix
    matrix = [['' for _ in range(key_length)] for _ in range(num_rows)]
    
    # Fill columns in key order
    chars_per_col = num_rows
    char_idx = 0
    
    for col_num in range(1, key_length + 1):
        col_idx = numeric_key.index(str(col_num))
        for row_idx in range(num_rows):
            if char_idx < len(ciphertext):
                matrix[row_idx][col_idx] = ciphertext[char_idx]
                char_idx += 1
    
    # Read row by row
    plaintext = ''
    for row in matrix:
        plaintext += ''.join(row)
    
    # Remove trailing 'X' padding
    plaintext = plaintext.rstrip('X')
    
    return plaintext


def get_key_permutations(length: int) -> List[str]:
    """
    Generate all permutations of keys of given length.
    For length n, generates all permutations of digits 1 to n.
    """
    from itertools import permutations
    
    digits = [str(i) for i in range(1, length + 1)]
    perms = [''.join(p) for p in permutations(digits)]
    return perms


def visualize_encryption(plaintext: str, key: str) -> dict:
    """
    Generate visualization data for encryption process.
    Returns matrix representation and column reading order.
    """
    numeric_key = normalize_key(key)
    key_length = len(numeric_key)
    
    # Prepare plaintext
    plaintext = plaintext.replace(' ', '')
    num_rows = math.ceil(len(plaintext) / key_length)
    total_chars = num_rows * key_length
    padding_needed = total_chars - len(plaintext)
    padded_text = plaintext + 'X' * padding_needed
    
    # Create matrix
    matrix = []
    for i in range(num_rows):
        row = []
        for j in range(key_length):
            idx = i * key_length + j
            if idx < len(padded_text):
                row.append(padded_text[idx])
            else:
                row.append('X')
        matrix.append(row)
    
    # Column reading order
    column_order = []
    for col_num in range(1, key_length + 1):
        col_idx = numeric_key.index(str(col_num))
        column_order.append(col_idx)
    
    return {
        'matrix': matrix,
        'key': list(numeric_key),
        'column_order': column_order,
        'num_rows': num_rows,
        'num_cols': key_length
    }
