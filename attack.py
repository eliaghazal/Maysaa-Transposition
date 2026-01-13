"""
Attack Module for Columnar Transposition Cipher
Implements brute-force and heuristic attacks
"""

import random
from typing import List, Tuple, Dict, Callable
from itertools import permutations
import cipher
import scoring
import dictionary


def brute_force_attack(ciphertext: str, max_key_length: int = 7, 
                       progress_callback: Callable = None) -> List[Tuple[str, str, float]]:
    """
    Brute-force attack trying all key permutations up to max_key_length.
    
    Args:
        ciphertext: The encrypted text to crack
        max_key_length: Maximum key length to try (1-7 recommended)
        progress_callback: Optional callback function for progress updates
        
    Returns:
        List of (key, plaintext, score) tuples sorted by score (best first)
    """
    results = []
    total_attempts = 0
    
    # Calculate total permutations for progress tracking
    total_perms = sum(factorial(i) for i in range(1, max_key_length + 1))
    
    for key_length in range(1, max_key_length + 1):
        # Generate all permutations for this key length
        digits = [str(i) for i in range(1, key_length + 1)]
        key_perms = [''.join(p) for p in permutations(digits)]
        
        for key in key_perms:
            try:
                # Decrypt with this key
                plaintext = cipher.decrypt(ciphertext, key)
                
                # Score the plaintext
                base_score = scoring.score_text(plaintext)
                dict_score = dictionary.score_text_by_dictionary(plaintext)
                combined_score = scoring.score_with_dictionary(plaintext, dict_score)
                
                results.append((key, plaintext, combined_score))
                
                total_attempts += 1
                
                # Progress callback
                if progress_callback and total_attempts % 100 == 0:
                    progress_callback(total_attempts, total_perms)
                    
            except Exception as e:
                # Skip invalid decryptions
                continue
    
    # Sort by score (highest first)
    results.sort(key=lambda x: x[2], reverse=True)
    
    return results


def factorial(n: int) -> int:
    """Calculate factorial."""
    if n <= 1:
        return 1
    result = 1
    for i in range(2, n + 1):
        result *= i
    return result


def hill_climbing_attack(ciphertext: str, key_length: int, 
                         max_iterations: int = 1000,
                         progress_callback: Callable = None) -> Tuple[str, str, float]:
    """
    Hill-climbing heuristic attack for larger keys.
    
    Args:
        ciphertext: The encrypted text to crack
        key_length: Length of the key to search for
        max_iterations: Maximum number of iterations
        progress_callback: Optional callback for progress updates
        
    Returns:
        Tuple of (best_key, best_plaintext, best_score)
    """
    # Generate random initial key
    current_key = generate_random_key(key_length)
    current_plaintext = cipher.decrypt(ciphertext, current_key)
    current_score = evaluate_plaintext(current_plaintext)
    
    best_key = current_key
    best_plaintext = current_plaintext
    best_score = current_score
    
    no_improvement_count = 0
    max_no_improvement = 100
    
    for iteration in range(max_iterations):
        # Generate neighbor keys by swapping two positions
        neighbor_key = swap_random_positions(current_key)
        neighbor_plaintext = cipher.decrypt(ciphertext, neighbor_key)
        neighbor_score = evaluate_plaintext(neighbor_plaintext)
        
        # If neighbor is better, move to it
        if neighbor_score > current_score:
            current_key = neighbor_key
            current_plaintext = neighbor_plaintext
            current_score = neighbor_score
            no_improvement_count = 0
            
            # Update best if necessary
            if current_score > best_score:
                best_key = current_key
                best_plaintext = current_plaintext
                best_score = current_score
        else:
            no_improvement_count += 1
            
            # Restart from random position if stuck
            if no_improvement_count >= max_no_improvement:
                current_key = generate_random_key(key_length)
                current_plaintext = cipher.decrypt(ciphertext, current_key)
                current_score = evaluate_plaintext(current_plaintext)
                no_improvement_count = 0
        
        # Progress callback
        if progress_callback and iteration % 50 == 0:
            progress_callback(iteration, max_iterations, best_score)
    
    return (best_key, best_plaintext, best_score)


def genetic_algorithm_attack(ciphertext: str, key_length: int,
                             population_size: int = 100,
                             generations: int = 500,
                             progress_callback: Callable = None) -> Tuple[str, str, float]:
    """
    Genetic algorithm attack for larger keys.
    
    Args:
        ciphertext: The encrypted text to crack
        key_length: Length of the key to search for
        population_size: Size of population
        generations: Number of generations
        progress_callback: Optional callback for progress updates
        
    Returns:
        Tuple of (best_key, best_plaintext, best_score)
    """
    # Initialize population with random keys
    population = [generate_random_key(key_length) for _ in range(population_size)]
    
    best_key = None
    best_plaintext = None
    best_score = 0
    
    for generation in range(generations):
        # Evaluate fitness for all individuals
        fitness_scores = []
        for key in population:
            plaintext = cipher.decrypt(ciphertext, key)
            score = evaluate_plaintext(plaintext)
            fitness_scores.append((key, plaintext, score))
            
            if score > best_score:
                best_key = key
                best_plaintext = plaintext
                best_score = score
        
        # Sort by fitness
        fitness_scores.sort(key=lambda x: x[2], reverse=True)
        
        # Selection: keep top 50%
        selected = [item[0] for item in fitness_scores[:population_size // 2]]
        
        # Create new population through crossover and mutation
        new_population = selected[:]
        
        while len(new_population) < population_size:
            # Select two parents
            parent1 = random.choice(selected)
            parent2 = random.choice(selected)
            
            # Crossover
            child = crossover_keys(parent1, parent2)
            
            # Mutation (10% chance)
            if random.random() < 0.1:
                child = mutate_key(child)
            
            new_population.append(child)
        
        population = new_population
        
        # Progress callback
        if progress_callback and generation % 50 == 0:
            progress_callback(generation, generations, best_score)
    
    return (best_key, best_plaintext, best_score)


def generate_random_key(length: int) -> str:
    """Generate a random valid key of given length."""
    digits = list(range(1, length + 1))
    random.shuffle(digits)
    return ''.join(str(d) for d in digits)


def swap_random_positions(key: str) -> str:
    """Swap two random positions in a key."""
    key_list = list(key)
    i, j = random.sample(range(len(key)), 2)
    key_list[i], key_list[j] = key_list[j], key_list[i]
    return ''.join(key_list)


def crossover_keys(key1: str, key2: str) -> str:
    """
    Perform crossover between two keys.
    Uses order crossover (OX) to maintain valid permutation.
    """
    length = len(key1)
    
    # Select random crossover points
    point1, point2 = sorted(random.sample(range(length), 2))
    
    # Start with middle section from parent1
    child = ['0'] * length
    for i in range(point1, point2):
        child[i] = key1[i]
    
    # Fill remaining positions with parent2's order
    parent2_pos = 0
    for i in list(range(0, point1)) + list(range(point2, length)):
        while key2[parent2_pos] in child:
            parent2_pos += 1
        child[i] = key2[parent2_pos]
        parent2_pos += 1
    
    return ''.join(child)


def mutate_key(key: str) -> str:
    """Mutate a key by swapping two random positions."""
    return swap_random_positions(key)


def evaluate_plaintext(plaintext: str) -> float:
    """
    Evaluate the quality of a plaintext candidate.
    Combines multiple scoring methods.
    """
    base_score = scoring.score_text(plaintext)
    dict_score = dictionary.score_text_by_dictionary(plaintext)
    combined_score = scoring.score_with_dictionary(plaintext, dict_score)
    
    return combined_score


def smart_attack(ciphertext: str, min_key_length: int = 1, max_key_length: int = 10,
                progress_callback: Callable = None) -> List[Tuple[str, str, float]]:
    """
    Smart attack that uses brute-force for small keys and heuristics for larger keys.
    
    Args:
        ciphertext: The encrypted text to crack
        min_key_length: Minimum key length to try
        max_key_length: Maximum key length to try
        progress_callback: Optional callback for progress updates
        
    Returns:
        List of (key, plaintext, score) tuples sorted by score
    """
    all_results = []
    
    # Use brute-force for keys 1-7
    if min_key_length <= 7:
        brute_force_max = min(7, max_key_length)
        if progress_callback:
            progress_callback(f"Brute-forcing keys of length {min_key_length}-{brute_force_max}...")
        
        brute_results = brute_force_attack(ciphertext, brute_force_max, progress_callback)
        all_results.extend(brute_results[:10])  # Keep top 10 from brute force
    
    # Use heuristics for keys 8+
    if max_key_length > 7:
        for key_length in range(max(8, min_key_length), max_key_length + 1):
            if progress_callback:
                progress_callback(f"Using heuristics for key length {key_length}...")
            
            # Try both hill climbing and genetic algorithm
            hc_result = hill_climbing_attack(ciphertext, key_length, 
                                            max_iterations=1000, 
                                            progress_callback=progress_callback)
            all_results.append(hc_result)
            
            ga_result = genetic_algorithm_attack(ciphertext, key_length,
                                                population_size=100,
                                                generations=300,
                                                progress_callback=progress_callback)
            all_results.append(ga_result)
    
    # Sort all results by score
    all_results.sort(key=lambda x: x[2], reverse=True)
    
    return all_results


def analyze_ciphertext(ciphertext: str) -> Dict:
    """
    Analyze ciphertext to provide hints about the key.
    Returns statistics that might help in determining key length.
    """
    length = len(ciphertext)
    
    # Calculate possible key lengths based on factors
    factors = []
    for i in range(2, min(length, 20)):
        if length % i == 0:
            factors.append(i)
    
    # Calculate Index of Coincidence for different key lengths
    ic_scores = {}
    for key_len in range(2, min(length // 2, 15)):
        columns = ['' for _ in range(key_len)]
        for i, char in enumerate(ciphertext):
            columns[i % key_len] += char
        
        # Calculate average IC for columns
        ic_sum = 0
        for col in columns:
            ic_sum += calculate_ic(col)
        ic_scores[key_len] = ic_sum / key_len
    
    return {
        'length': length,
        'factors': factors,
        'ic_scores': ic_scores,
        'suggested_key_lengths': sorted(ic_scores.keys(), 
                                       key=lambda k: abs(ic_scores[k] - 0.067))[:5]
    }


def calculate_ic(text: str) -> float:
    """
    Calculate Index of Coincidence for text.
    English text typically has IC around 0.067.
    """
    if len(text) < 2:
        return 0.0
    
    text = text.upper()
    letter_counts = {}
    total_letters = 0
    
    for char in text:
        if char.isalpha():
            letter_counts[char] = letter_counts.get(char, 0) + 1
            total_letters += 1
    
    if total_letters < 2:
        return 0.0
    
    ic = 0.0
    for count in letter_counts.values():
        ic += count * (count - 1)
    
    ic /= (total_letters * (total_letters - 1))
    
    return ic
