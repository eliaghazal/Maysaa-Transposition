"""
Text Scoring System for Cryptanalysis
Uses frequency analysis, n-grams, and other metrics to score plaintext candidates
"""

import math
from collections import Counter
from typing import Dict


# English letter frequencies (percentage)
ENGLISH_FREQ = {
    'A': 8.167, 'B': 1.492, 'C': 2.782, 'D': 4.253, 'E': 12.702,
    'F': 2.228, 'G': 2.015, 'H': 6.094, 'I': 6.966, 'J': 0.153,
    'K': 0.772, 'L': 4.025, 'M': 2.406, 'N': 6.749, 'O': 7.507,
    'P': 1.929, 'Q': 0.095, 'R': 5.987, 'S': 6.327, 'T': 9.056,
    'U': 2.758, 'V': 0.978, 'W': 2.360, 'X': 0.150, 'Y': 1.974,
    'Z': 0.074
}

# Common English bigrams (most frequent)
COMMON_BIGRAMS = {
    'TH': 3.56, 'HE': 3.07, 'IN': 2.43, 'ER': 2.05, 'AN': 1.99,
    'RE': 1.85, 'ON': 1.76, 'AT': 1.49, 'EN': 1.45, 'ND': 1.35,
    'TI': 1.34, 'ES': 1.34, 'OR': 1.28, 'TE': 1.20, 'OF': 1.17,
    'ED': 1.17, 'IS': 1.13, 'IT': 1.12, 'AL': 1.09, 'AR': 1.07,
    'ST': 1.05, 'TO': 1.04, 'NT': 1.04, 'NG': 0.95, 'SE': 0.93,
    'HA': 0.93, 'AS': 0.87, 'OU': 0.87, 'IO': 0.83, 'LE': 0.83
}

# Common English trigrams
COMMON_TRIGRAMS = {
    'THE': 3.51, 'AND': 1.59, 'ING': 1.14, 'HER': 0.82, 'HAT': 0.65,
    'HIS': 0.60, 'THA': 0.60, 'ERE': 0.56, 'FOR': 0.56, 'ENT': 0.53,
    'ION': 0.53, 'TER': 0.51, 'WAS': 0.51, 'YOU': 0.48, 'ITH': 0.48,
    'VER': 0.47, 'ALL': 0.46, 'WIT': 0.46, 'THI': 0.46, 'TIO': 0.45
}

# Common quadgrams (4-letter sequences)
COMMON_QUADGRAMS = {
    'TION': 0.31, 'THAT': 0.27, 'THER': 0.24, 'WITH': 0.23, 'MENT': 0.19,
    'IONS': 0.17, 'THES': 0.16, 'ATIO': 0.15, 'FTHE': 0.14, 'DTHE': 0.13,
    'ANDT': 0.13, 'INTH': 0.12, 'HERE': 0.12, 'STHE': 0.12, 'OTHE': 0.11
}


def chi_squared(text: str) -> float:
    """
    Calculate chi-squared statistic comparing text frequency to English.
    Lower values indicate closer match to English.
    """
    if not text:
        return float('inf')
    
    text = text.upper()
    text_length = len([c for c in text if c.isalpha()])
    
    if text_length == 0:
        return float('inf')
    
    # Count letter frequencies in text
    letter_counts = Counter(c for c in text if c.isalpha())
    
    chi_sq = 0.0
    for letter in 'ABCDEFGHIJKLMNOPQRSTUVWXYZ':
        observed = letter_counts.get(letter, 0)
        expected = (ENGLISH_FREQ[letter] / 100) * text_length
        
        if expected > 0:
            chi_sq += ((observed - expected) ** 2) / expected
    
    return chi_sq


def score_letter_frequency(text: str) -> float:
    """
    Score text based on letter frequency match to English.
    Returns normalized score (higher is better, 0-1 range).
    """
    chi_sq = chi_squared(text)
    # Normalize: typical chi-squared for random text is around 500-1000
    # Good English text has chi-squared < 100
    # Convert to 0-1 scale (inverse and bounded)
    score = max(0, 1 - (chi_sq / 500))
    return score


def score_bigrams(text: str) -> float:
    """
    Score text based on common English bigrams.
    """
    if len(text) < 2:
        return 0.0
    
    text = text.upper()
    bigram_count = 0
    total_bigrams = 0
    
    for i in range(len(text) - 1):
        if text[i].isalpha() and text[i + 1].isalpha():
            bigram = text[i:i + 2]
            total_bigrams += 1
            if bigram in COMMON_BIGRAMS:
                bigram_count += 1
    
    if total_bigrams == 0:
        return 0.0
    
    return bigram_count / total_bigrams


def score_trigrams(text: str) -> float:
    """
    Score text based on common English trigrams.
    """
    if len(text) < 3:
        return 0.0
    
    text = text.upper()
    trigram_count = 0
    total_trigrams = 0
    
    for i in range(len(text) - 2):
        if text[i].isalpha() and text[i + 1].isalpha() and text[i + 2].isalpha():
            trigram = text[i:i + 3]
            total_trigrams += 1
            if trigram in COMMON_TRIGRAMS:
                trigram_count += 1
    
    if total_trigrams == 0:
        return 0.0
    
    return trigram_count / total_trigrams


def score_quadgrams(text: str) -> float:
    """
    Score text based on common English quadgrams.
    """
    if len(text) < 4:
        return 0.0
    
    text = text.upper()
    quadgram_count = 0
    total_quadgrams = 0
    
    for i in range(len(text) - 3):
        if all(text[i + j].isalpha() for j in range(4)):
            quadgram = text[i:i + 4]
            total_quadgrams += 1
            if quadgram in COMMON_QUADGRAMS:
                quadgram_count += 1
    
    if total_quadgrams == 0:
        return 0.0
    
    return quadgram_count / total_quadgrams


def score_text(text: str) -> float:
    """
    Comprehensive text scoring combining multiple metrics.
    Returns score where higher is better (0-100 scale).
    """
    if not text or len(text) < 2:
        return 0.0
    
    # Weight different scoring methods
    freq_score = score_letter_frequency(text) * 30  # 30 points max
    bigram_score = score_bigrams(text) * 25  # 25 points max
    trigram_score = score_trigrams(text) * 25  # 25 points max
    quadgram_score = score_quadgrams(text) * 20  # 20 points max
    
    total_score = freq_score + bigram_score + trigram_score + quadgram_score
    
    return total_score


def score_with_dictionary(text: str, dictionary_score: float) -> float:
    """
    Combine regular scoring with dictionary-based scoring.
    """
    base_score = score_text(text)
    # Dictionary score contributes up to 50% bonus
    combined_score = base_score * (1 + dictionary_score * 0.5)
    return min(combined_score, 150)  # Cap at 150


def compare_texts(text1: str, text2: str) -> Dict[str, float]:
    """
    Compare two texts and return their scores.
    Useful for evaluating decryption attempts.
    """
    return {
        'text1_score': score_text(text1),
        'text2_score': score_text(text2),
        'text1_chi_squared': chi_squared(text1),
        'text2_chi_squared': chi_squared(text2)
    }
