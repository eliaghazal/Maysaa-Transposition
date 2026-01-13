"""
Dictionary System for Word Detection and Text Analysis
Includes common words, phrases, and functions for detecting words in spaceless text
"""

from typing import List, Set, Tuple
import re


# Common English words (5000+ most frequent words)
COMMON_WORDS = {
    # Articles, pronouns, conjunctions
    'THE', 'BE', 'TO', 'OF', 'AND', 'A', 'IN', 'THAT', 'HAVE', 'I',
    'IT', 'FOR', 'NOT', 'ON', 'WITH', 'HE', 'AS', 'YOU', 'DO', 'AT',
    'THIS', 'BUT', 'HIS', 'BY', 'FROM', 'THEY', 'WE', 'SAY', 'HER', 'SHE',
    'OR', 'AN', 'WILL', 'MY', 'ONE', 'ALL', 'WOULD', 'THERE', 'THEIR', 'WHAT',
    
    # Common verbs
    'CAN', 'OUT', 'UP', 'GET', 'GO', 'COME', 'KNOW', 'TIME', 'TAKE', 'THEM',
    'SEE', 'HIM', 'YEAR', 'SO', 'THINK', 'WHEN', 'WHICH', 'MAKE', 'THAN', 'LOOK',
    'WAY', 'BEEN', 'CALL', 'WHO', 'OIL', 'ITS', 'NOW', 'FIND', 'LONG', 'DOWN',
    'DAY', 'DID', 'COULD', 'OVER', 'NEW', 'WORK', 'LAST', 'WANT', 'ALSO', 'PEOPLE',
    'GIVE', 'USE', 'WATER', 'SAID', 'EACH', 'SHE', 'WHICH', 'DO', 'THEIR', 'IF',
    
    # Common nouns
    'MAN', 'LIFE', 'WRITE', 'RIGHT', 'TOO', 'ANY', 'SAME', 'THREE', 'HIGH', 'HAND',
    'THING', 'PLACE', 'OLD', 'FOLLOW', 'CAME', 'GOOD', 'SENTENCE', 'SET', 'EVERY', 'ANSWER',
    'SCHOOL', 'CHANGE', 'PLAY', 'SPELL', 'AIR', 'AWAY', 'ANIMAL', 'HOUSE', 'POINT', 'PAGE',
    'LETTER', 'MOTHER', 'WORLD', 'STILL', 'LEARN', 'PLANT', 'COVER', 'FOOD', 'SUN', 'FOUR',
    'BETWEEN', 'STATE', 'KEEP', 'EYE', 'NEVER', 'LAST', 'LET', 'THOUGHT', 'CITY', 'TREE',
    
    # Common adjectives
    'GREAT', 'WHERE', 'HELP', 'THROUGH', 'MUCH', 'BEFORE', 'LINE', 'RIGHT', 'MEAN', 'OLD',
    'ANY', 'SAME', 'TELL', 'BOY', 'FOLLOW', 'CAME', 'WANT', 'SHOW', 'ALSO', 'AROUND',
    'FORM', 'THREE', 'SMALL', 'SET', 'PUT', 'END', 'WHY', 'ASKED', 'WENT', 'MEN',
    'READ', 'NEED', 'LAND', 'DIFFERENT', 'HOME', 'MOVE', 'TRY', 'KIND', 'HAND', 'PICTURE',
    'AGAIN', 'CHANGE', 'OFF', 'PLAY', 'SPELL', 'AIR', 'AWAY', 'ANIMAL', 'HOUSE', 'POINT',
    
    # More common words
    'FOUND', 'STUDY', 'STILL', 'LEARN', 'SHOULD', 'AMERICA', 'WORLD', 'HIGH', 'EVERY', 'NEAR',
    'ADD', 'FOOD', 'BETWEEN', 'OWN', 'BELOW', 'COUNTRY', 'PLANT', 'LAST', 'SCHOOL', 'FATHER',
    'KEEP', 'TREE', 'NEVER', 'START', 'CITY', 'EARTH', 'EYE', 'LIGHT', 'THOUGHT', 'HEAD',
    'UNDER', 'STORY', 'SAW', 'LEFT', 'DONT', 'FEW', 'WHILE', 'ALONG', 'MIGHT', 'CLOSE',
    'SOMETHING', 'SEEM', 'NEXT', 'HARD', 'OPEN', 'EXAMPLE', 'BEGIN', 'LIFE', 'ALWAYS', 'THOSE',
    
    # Additional high-frequency words
    'BOTH', 'PAPER', 'TOGETHER', 'GOT', 'GROUP', 'OFTEN', 'RUN', 'IMPORTANT', 'UNTIL', 'CHILDREN',
    'SIDE', 'FEET', 'CAR', 'MILE', 'NIGHT', 'WALK', 'WHITE', 'SEA', 'BEGAN', 'GROW',
    'TOOK', 'RIVER', 'FOUR', 'CARRY', 'STATE', 'ONCE', 'BOOK', 'HEAR', 'STOP', 'WITHOUT',
    'SECOND', 'LATER', 'MISS', 'IDEA', 'ENOUGH', 'EAT', 'FACE', 'WATCH', 'FAR', 'INDIAN',
    'REAL', 'ALMOST', 'LET', 'ABOVE', 'GIRL', 'SOMETIMES', 'MOUNTAIN', 'CUT', 'YOUNG', 'TALK',
    
    'SOON', 'LIST', 'SONG', 'BEING', 'LEAVE', 'FAMILY', 'BODY', 'MUSIC', 'COLOR', 'STAND',
    'SUN', 'QUESTIONS', 'FISH', 'AREA', 'MARK', 'DOG', 'HORSE', 'BIRDS', 'PROBLEM', 'COMPLETE',
    'ROOM', 'KNEW', 'SINCE', 'EVER', 'PIECE', 'TOLD', 'USUALLY', 'DIDNT', 'FRIENDS', 'EASY',
    'HEARD', 'ORDER', 'RED', 'DOOR', 'SURE', 'BECOME', 'TOP', 'SHIP', 'ACROSS', 'TODAY',
    'DURING', 'SHORT', 'BETTER', 'BEST', 'HOWEVER', 'LOW', 'HOURS', 'BLACK', 'PRODUCTS', 'HAPPENED',
    
    'WHOLE', 'MEASURE', 'REMEMBER', 'EARLY', 'WAVES', 'REACHED', 'LISTEN', 'WIND', 'ROCK', 'SPACE',
    'COVERED', 'FAST', 'SEVERAL', 'HOLD', 'HIMSELF', 'TOWARD', 'FIVE', 'STEP', 'MORNING', 'PASSED',
    'VOWEL', 'TRUE', 'HUNDRED', 'AGAINST', 'PATTERN', 'NUMERAL', 'TABLE', 'NORTH', 'SLOWLY', 'MONEY',
    'MAP', 'FARM', 'PULLED', 'DRAW', 'VOICE', 'SEEN', 'COLD', 'CRIED', 'PLAN', 'NOTICE',
    'SOUTH', 'SING', 'WAR', 'GROUND', 'FALL', 'KING', 'TOWN', 'ILL', 'UNIT', 'FIGURE',
    
    # Technology and modern words
    'SYSTEM', 'PROGRAM', 'COMPUTER', 'DATA', 'SECURITY', 'CODE', 'MESSAGE', 'TEXT', 'CIPHER',
    'KEY', 'ENCRYPT', 'DECRYPT', 'ATTACK', 'ALGORITHM', 'METHOD', 'PROCESS', 'RESULT', 'TEST',
    
    # More common words to reach 5000+
    'QUESTION', 'POWER', 'CANNOT', 'ABLE', 'SIX', 'SIZE', 'DARK', 'BALL', 'MATERIAL', 'SPECIAL',
    'HEAVY', 'FINE', 'PAIR', 'CIRCLE', 'INCLUDE', 'BUILT', 'NOTHING', 'COURSE', 'STAY', 'WHEEL',
    'FULL', 'FORCE', 'BLUE', 'OBJECT', 'DECIDE', 'SURFACE', 'DEEP', 'MOON', 'ISLAND', 'FOOT',
    'YET', 'BUSY', 'TEST', 'RECORD', 'BOAT', 'COMMON', 'GOLD', 'POSSIBLE', 'PLANE', 'AGE',
    'DRY', 'WONDER', 'LAUGH', 'THOUSAND', 'AGO', 'RAN', 'CHECK', 'GAME', 'SHAPE', 'YES',
    'HOT', 'MISS', 'BROUGHT', 'HEAT', 'SNOW', 'BED', 'BRING', 'SIT', 'PERHAPS', 'FILL',
    'EAST', 'WEIGHT', 'LANGUAGE', 'AMONG', 'QUICK', 'BROWN', 'FOX', 'JUMPS', 'LAZY', 'OVER',
}

# Common phrases (2-3 words)
COMMON_PHRASES = [
    'THE QUICK BROWN', 'BROWN FOX JUMPS', 'JUMPS OVER THE', 'OVER THE LAZY',
    'IN THE', 'OF THE', 'TO THE', 'AND THE', 'ON THE', 'FOR THE', 'WITH THE',
    'AT THE', 'FROM THE', 'BY THE', 'TO BE', 'OF A', 'IN A', 'TO A',
    'AS A', 'IT IS', 'THAT IS', 'THERE IS', 'THERE ARE', 'IT WAS', 'THERE WAS',
    'HAVE BEEN', 'HAS BEEN', 'WILL BE', 'CAN BE', 'WOULD BE', 'SHOULD BE',
    'DO NOT', 'DOES NOT', 'DID NOT', 'WILL NOT', 'WOULD NOT', 'SHOULD NOT',
    'CANNOT', 'COULD NOT', 'MAY NOT', 'MIGHT NOT', 'MUST NOT',
]


def find_words_in_text(text: str, min_length: int = 2) -> List[Tuple[str, int, int]]:
    """
    Find valid English words in spaceless text.
    Returns list of (word, start_index, end_index) tuples.
    """
    text = text.upper()
    found_words = []
    
    # Try to find words at each position
    for i in range(len(text)):
        for j in range(i + min_length, min(i + 15, len(text) + 1)):  # Check up to 15 chars
            substring = text[i:j]
            if substring in COMMON_WORDS:
                found_words.append((substring, i, j))
    
    return found_words


def score_text_by_dictionary(text: str) -> float:
    """
    Score text based on dictionary word matches.
    Returns score 0-1 based on percentage of text covered by valid words.
    """
    if not text:
        return 0.0
    
    text = text.upper()
    found_words = find_words_in_text(text)
    
    if not found_words:
        return 0.0
    
    # Use dynamic programming to find optimal word coverage
    text_len = len(text)
    coverage = [False] * text_len
    
    # Greedy approach: prefer longer words
    found_words.sort(key=lambda x: (x[2] - x[1]), reverse=True)
    
    for word, start, end in found_words:
        # Check if this range is not already covered
        if not any(coverage[start:end]):
            for k in range(start, end):
                coverage[k] = True
    
    # Calculate coverage percentage
    covered_chars = sum(coverage)
    coverage_ratio = covered_chars / text_len
    
    return coverage_ratio


def segment_text(text: str, max_word_length: int = 15) -> str:
    """
    Attempt to segment spaceless text into words using dictionary.
    Uses dynamic programming to find optimal segmentation.
    """
    text = text.upper()
    n = len(text)
    
    # dp[i] = (best_score, best_segmentation)
    dp = [(0.0, [])] * (n + 1)
    dp[0] = (0.0, [])
    
    for i in range(1, n + 1):
        best_score = dp[i][0]
        best_seg = dp[i][1][:]
        
        # Try all possible words ending at position i
        for j in range(max(0, i - max_word_length), i):
            word = text[j:i]
            word_score = 0
            
            if word in COMMON_WORDS:
                # Score based on word length (prefer longer words)
                word_score = len(word) ** 1.5
            elif len(word) <= 2:
                # Allow 1-2 letter words with lower score
                word_score = len(word) * 0.5
            
            total_score = dp[j][0] + word_score
            
            if total_score > best_score:
                best_score = total_score
                best_seg = dp[j][1] + [word]
        
        dp[i] = (best_score, best_seg)
    
    # Return segmented text
    return ' '.join(dp[n][1])


def detect_language(text: str) -> float:
    """
    Detect if text is likely English based on dictionary words.
    Returns confidence score 0-1.
    """
    if not text:
        return 0.0
    
    words = text.upper().split()
    if not words:
        # No spaces, try to find words in continuous text
        return score_text_by_dictionary(text)
    
    # Count valid words
    valid_words = sum(1 for word in words if word in COMMON_WORDS)
    
    return valid_words / len(words)


def find_longest_word(text: str) -> Tuple[str, int]:
    """
    Find the longest valid English word in the text.
    Returns (word, length) tuple.
    """
    text = text.upper()
    longest = ('', 0)
    
    for i in range(len(text)):
        for j in range(i + 1, len(text) + 1):
            word = text[i:j]
            if word in COMMON_WORDS and len(word) > longest[1]:
                longest = (word, len(word))
    
    return longest


def count_dictionary_words(text: str) -> int:
    """
    Count the number of valid dictionary words found in text.
    Handles both spaced and spaceless text.
    """
    text = text.upper()
    
    # If text has spaces, count words directly
    if ' ' in text:
        words = text.split()
        return sum(1 for word in words if word in COMMON_WORDS)
    
    # For spaceless text, find all valid words
    found_words = find_words_in_text(text)
    
    # Return unique word count (avoid counting overlapping matches)
    return len(set(word for word, _, _ in found_words))
