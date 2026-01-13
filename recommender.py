"""
AI Recommender System for Columnar Transposition Cipher
Analyzes ciphertext and suggests plausible keys with confidence scores
"""

from typing import List, Tuple, Dict
import math
from collections import Counter
import cipher
import scoring
import dictionary
import attack


def recommend_keys(ciphertext: str, num_recommendations: int = 10,
                   max_key_length: int = 10) -> List[Dict]:
    """
    Analyze ciphertext and recommend plausible keys.
    
    Args:
        ciphertext: The encrypted text to analyze
        num_recommendations: Number of key recommendations to return
        max_key_length: Maximum key length to consider
        
    Returns:
        List of recommendation dictionaries with keys, scores, and confidence
    """
    recommendations = []
    
    # Analyze ciphertext
    analysis = attack.analyze_ciphertext(ciphertext)
    
    # Get suggested key lengths from analysis
    suggested_lengths = analysis['suggested_key_lengths'][:5]
    
    # Also try common key lengths
    common_lengths = [3, 4, 5, 6, 7]
    all_lengths = list(set(suggested_lengths + common_lengths))
    all_lengths = [l for l in all_lengths if l <= max_key_length]
    all_lengths.sort()
    
    # For each key length, try to find best keys
    for key_length in all_lengths:
        # Use pattern analysis to suggest keys
        pattern_keys = analyze_column_patterns(ciphertext, key_length)
        
        # Score each suggested key
        for key in pattern_keys[:3]:  # Top 3 for each length
            try:
                plaintext = cipher.decrypt(ciphertext, key)
                base_score = scoring.score_text(plaintext)
                dict_score = dictionary.score_text_by_dictionary(plaintext)
                combined_score = scoring.score_with_dictionary(plaintext, dict_score)
                
                # Calculate confidence based on score
                confidence = calculate_confidence(combined_score)
                
                recommendations.append({
                    'key': key,
                    'key_length': key_length,
                    'plaintext': plaintext,
                    'score': combined_score,
                    'confidence': confidence,
                    'reason': f'Pattern analysis suggests this {key_length}-column arrangement'
                })
            except:
                continue
    
    # Sort by score
    recommendations.sort(key=lambda x: x['score'], reverse=True)
    
    # Return top recommendations
    return recommendations[:num_recommendations]


def analyze_column_patterns(ciphertext: str, key_length: int) -> List[str]:
    """
    Analyze patterns in ciphertext to suggest key arrangements.
    Uses frequency analysis and n-gram patterns.
    """
    from itertools import permutations
    
    # For small key lengths, try a few promising permutations
    if key_length <= 5:
        # Try common patterns first
        common_patterns = get_common_key_patterns(key_length)
        return common_patterns
    
    # For larger keys, use heuristic analysis
    # Divide ciphertext into columns
    col_length = len(ciphertext) // key_length
    columns = []
    
    char_idx = 0
    for col in range(key_length):
        col_text = ''
        for row in range(col_length):
            if char_idx < len(ciphertext):
                col_text += ciphertext[char_idx]
                char_idx += 1
        columns.append(col_text)
    
    # Analyze each column's characteristics
    column_scores = []
    for i, col in enumerate(columns):
        # Score based on letter frequency distribution
        freq_score = scoring.score_letter_frequency(col)
        # Score based on common starting letters if this could be column 1
        start_letter_score = score_starting_letters(col)
        # Combined score
        total_score = freq_score * 0.7 + start_letter_score * 0.3
        column_scores.append((i + 1, total_score))
    
    # Sort columns by score to suggest key order
    column_scores.sort(key=lambda x: x[1], reverse=True)
    
    # Generate key suggestions based on column ordering
    suggested_keys = []
    
    # Try the "natural" order suggested by scores
    key_order = [str(cs[0]) for cs in column_scores]
    suggested_keys.append(''.join(key_order))
    
    # Try variations
    if key_length <= 7:
        # Generate a few random permutations
        import random
        digits = [str(i) for i in range(1, key_length + 1)]
        for _ in range(min(10, math.factorial(key_length))):
            random.shuffle(digits)
            suggested_keys.append(''.join(digits))
    
    return suggested_keys[:10]


def get_common_key_patterns(key_length: int) -> List[str]:
    """
    Return common key patterns for given length.
    These are based on typical usage patterns.
    """
    from itertools import permutations
    
    patterns = []
    
    if key_length == 2:
        patterns = ['12', '21']
    elif key_length == 3:
        patterns = ['123', '132', '213', '231', '312', '321']
    elif key_length == 4:
        patterns = ['1234', '1243', '1324', '1342', '1423', '1432',
                   '2134', '2143', '2314', '2341', '2413', '2431',
                   '3124', '3142', '3214', '3241', '3412', '3421',
                   '4123', '4132', '4213', '4231', '4312', '4321']
    else:
        # For length 5+, generate some permutations
        digits = [str(i) for i in range(1, key_length + 1)]
        all_perms = [''.join(p) for p in permutations(digits)]
        # Return a subset
        import random
        patterns = random.sample(all_perms, min(24, len(all_perms)))
    
    return patterns


def score_starting_letters(text: str) -> float:
    """
    Score text based on how often it uses common starting letters.
    Common starting letters in English: T, A, O, S, W
    """
    if not text:
        return 0.0
    
    common_starters = {'T': 0.16, 'A': 0.12, 'O': 0.08, 'S': 0.08, 'W': 0.07,
                      'I': 0.07, 'H': 0.06, 'B': 0.05, 'F': 0.04, 'M': 0.04}
    
    text = text.upper()
    first_letters = [text[i] for i in range(0, len(text), 10) if i < len(text)]
    
    score = 0.0
    for letter in first_letters:
        if letter in common_starters:
            score += common_starters[letter]
    
    if first_letters:
        return score / len(first_letters)
    return 0.0


def calculate_confidence(score: float) -> float:
    """
    Calculate confidence level (0-100%) based on score.
    Scores typically range from 0-150.
    """
    # Normalize score to 0-100 range
    confidence = (score / 150) * 100
    confidence = max(0, min(100, confidence))
    
    return round(confidence, 2)


def analyze_key_statistics(key: str, ciphertext: str) -> Dict:
    """
    Provide detailed statistics about a specific key and its decryption.
    """
    try:
        plaintext = cipher.decrypt(ciphertext, key)
        
        base_score = scoring.score_text(plaintext)
        dict_score = dictionary.score_text_by_dictionary(plaintext)
        combined_score = scoring.score_with_dictionary(plaintext, dict_score)
        
        # Additional statistics
        word_count = dictionary.count_dictionary_words(plaintext)
        longest_word = dictionary.find_longest_word(plaintext)
        
        # Letter frequency analysis
        chi_sq = scoring.chi_squared(plaintext)
        
        return {
            'key': key,
            'plaintext': plaintext,
            'base_score': base_score,
            'dictionary_score': dict_score,
            'combined_score': combined_score,
            'confidence': calculate_confidence(combined_score),
            'word_count': word_count,
            'longest_word': longest_word[0],
            'longest_word_length': longest_word[1],
            'chi_squared': chi_sq,
            'is_likely_english': chi_sq < 200 and dict_score > 0.3
        }
    except Exception as e:
        return {
            'key': key,
            'error': str(e)
        }


def compare_keys(ciphertext: str, keys: List[str]) -> List[Dict]:
    """
    Compare multiple keys and rank them.
    """
    results = []
    
    for key in keys:
        stats = analyze_key_statistics(key, ciphertext)
        if 'error' not in stats:
            results.append(stats)
    
    # Sort by combined score
    results.sort(key=lambda x: x['combined_score'], reverse=True)
    
    return results


def suggest_key_length(ciphertext: str) -> List[Tuple[int, float, str]]:
    """
    Suggest most likely key lengths with confidence and reasoning.
    
    Returns:
        List of (key_length, confidence, reason) tuples
    """
    analysis = attack.analyze_ciphertext(ciphertext)
    suggestions = []
    
    # Factor-based suggestions
    if analysis['factors']:
        for factor in analysis['factors'][:5]:
            suggestions.append((
                factor,
                70.0,
                f"Length {factor} is a factor of ciphertext length {analysis['length']}"
            ))
    
    # IC-based suggestions
    ic_scores = analysis['ic_scores']
    for key_len in analysis['suggested_key_lengths']:
        ic_value = ic_scores[key_len]
        confidence = 50 + abs(ic_value - 0.067) * 100
        suggestions.append((
            key_len,
            min(confidence, 95.0),
            f"Index of Coincidence analysis suggests length {key_len}"
        ))
    
    # Common key length suggestions
    common_lengths = [3, 4, 5, 6]
    for length in common_lengths:
        if length not in [s[0] for s in suggestions]:
            suggestions.append((
                length,
                60.0,
                f"Length {length} is commonly used in transposition ciphers"
            ))
    
    # Remove duplicates and sort by confidence
    seen = set()
    unique_suggestions = []
    for length, conf, reason in suggestions:
        if length not in seen:
            seen.add(length)
            unique_suggestions.append((length, conf, reason))
    
    unique_suggestions.sort(key=lambda x: x[1], reverse=True)
    
    return unique_suggestions[:10]


def get_recommendation_explanation(recommendation: Dict) -> str:
    """
    Generate a human-readable explanation for a recommendation.
    """
    key = recommendation['key']
    confidence = recommendation['confidence']
    score = recommendation['score']
    
    explanation = f"Key '{key}' (length {len(key)}) "
    
    if confidence >= 80:
        explanation += "is highly likely to be correct. "
    elif confidence >= 60:
        explanation += "shows strong potential. "
    elif confidence >= 40:
        explanation += "is a reasonable candidate. "
    else:
        explanation += "is a possible option but less likely. "
    
    explanation += f"Score: {score:.2f}, Confidence: {confidence:.1f}%."
    
    return explanation
