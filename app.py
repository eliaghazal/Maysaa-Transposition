"""
Flask Web Application for Columnar Transposition Cipher
Provides web interface for encryption, decryption, attacks, and AI recommendations
"""

from flask import Flask, render_template, request, jsonify, session
import secrets
import cipher
import scoring
import dictionary
import attack
import recommender

app = Flask(__name__)
app.secret_key = secrets.token_hex(32)


@app.route('/')
def index():
    """Home page."""
    return render_template('index.html')


@app.route('/encrypt')
def encrypt_page():
    """Encryption page."""
    return render_template('encrypt.html')


@app.route('/decrypt')
def decrypt_page():
    """Decryption page."""
    return render_template('decrypt.html')


@app.route('/attack')
def attack_page():
    """Attack/crack page."""
    return render_template('attack.html')


@app.route('/recommender')
def recommender_page():
    """AI recommender page."""
    return render_template('recommender.html')


@app.route('/api/encrypt', methods=['POST'])
def api_encrypt():
    """API endpoint for encryption."""
    try:
        data = request.get_json()
        plaintext = data.get('plaintext', '')
        key = data.get('key', '')
        keep_spaces = data.get('keep_spaces', False)
        
        if not plaintext or not key:
            return jsonify({'error': 'Missing plaintext or key'}), 400
        
        # Encrypt
        ciphertext = cipher.encrypt(plaintext, key, keep_spaces)
        
        # Get visualization data
        viz_data = cipher.visualize_encryption(plaintext, key)
        
        return jsonify({
            'success': True,
            'ciphertext': ciphertext,
            'visualization': viz_data
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 400


@app.route('/api/decrypt', methods=['POST'])
def api_decrypt():
    """API endpoint for decryption."""
    try:
        data = request.get_json()
        ciphertext = data.get('ciphertext', '')
        key = data.get('key', '')
        
        if not ciphertext or not key:
            return jsonify({'error': 'Missing ciphertext or key'}), 400
        
        # Decrypt
        plaintext = cipher.decrypt(ciphertext, key)
        
        # Score the plaintext
        base_score = scoring.score_text(plaintext)
        dict_score = dictionary.score_text_by_dictionary(plaintext)
        
        return jsonify({
            'success': True,
            'plaintext': plaintext,
            'score': base_score,
            'dictionary_score': dict_score
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 400


@app.route('/api/attack', methods=['POST'])
def api_attack():
    """API endpoint for attacking ciphertext."""
    try:
        data = request.get_json()
        ciphertext = data.get('ciphertext', '')
        attack_type = data.get('attack_type', 'smart')
        max_key_length = int(data.get('max_key_length', 7))
        
        if not ciphertext:
            return jsonify({'error': 'Missing ciphertext'}), 400
        
        results = []
        
        if attack_type == 'brute_force':
            # Brute-force attack
            attack_results = attack.brute_force_attack(ciphertext, max_key_length)
            results = [
                {
                    'key': key,
                    'plaintext': plaintext,
                    'score': score
                }
                for key, plaintext, score in attack_results[:20]
            ]
        elif attack_type == 'smart':
            # Smart attack (brute-force + heuristics)
            attack_results = attack.smart_attack(ciphertext, 1, max_key_length)
            results = [
                {
                    'key': key,
                    'plaintext': plaintext,
                    'score': score
                }
                for key, plaintext, score in attack_results[:20]
            ]
        else:
            return jsonify({'error': 'Invalid attack type'}), 400
        
        return jsonify({
            'success': True,
            'results': results,
            'total_found': len(results)
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 400


@app.route('/api/recommend', methods=['POST'])
def api_recommend():
    """API endpoint for AI key recommendations."""
    try:
        data = request.get_json()
        ciphertext = data.get('ciphertext', '')
        num_recommendations = int(data.get('num_recommendations', 10))
        max_key_length = int(data.get('max_key_length', 10))
        
        if not ciphertext:
            return jsonify({'error': 'Missing ciphertext'}), 400
        
        # Get recommendations
        recommendations = recommender.recommend_keys(ciphertext, num_recommendations, max_key_length)
        
        # Get key length suggestions
        key_length_suggestions = recommender.suggest_key_length(ciphertext)
        
        return jsonify({
            'success': True,
            'recommendations': recommendations,
            'key_length_suggestions': [
                {
                    'length': length,
                    'confidence': conf,
                    'reason': reason
                }
                for length, conf, reason in key_length_suggestions
            ]
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 400


@app.route('/api/analyze', methods=['POST'])
def api_analyze():
    """API endpoint for analyzing ciphertext."""
    try:
        data = request.get_json()
        ciphertext = data.get('ciphertext', '')
        
        if not ciphertext:
            return jsonify({'error': 'Missing ciphertext'}), 400
        
        # Analyze ciphertext
        analysis = attack.analyze_ciphertext(ciphertext)
        
        return jsonify({
            'success': True,
            'analysis': analysis
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 400


@app.route('/api/validate_key', methods=['POST'])
def api_validate_key():
    """API endpoint for validating a key."""
    try:
        data = request.get_json()
        key = data.get('key', '')
        
        if not key:
            return jsonify({'error': 'Missing key'}), 400
        
        # Validate key
        is_valid = cipher.validate_key(key)
        
        if is_valid:
            # Normalize to numeric format
            numeric_key = cipher.normalize_key(key)
            return jsonify({
                'success': True,
                'valid': True,
                'numeric_key': numeric_key
            })
        else:
            return jsonify({
                'success': True,
                'valid': False,
                'message': 'Invalid key format'
            })
    except Exception as e:
        return jsonify({'error': str(e)}), 400


@app.route('/api/segment_text', methods=['POST'])
def api_segment_text():
    """API endpoint for segmenting spaceless text."""
    try:
        data = request.get_json()
        text = data.get('text', '')
        
        if not text:
            return jsonify({'error': 'Missing text'}), 400
        
        # Segment text
        segmented = dictionary.segment_text(text)
        
        # Find words in text
        found_words = dictionary.find_words_in_text(text)
        
        return jsonify({
            'success': True,
            'segmented_text': segmented,
            'found_words': [
                {'word': word, 'start': start, 'end': end}
                for word, start, end in found_words[:50]
            ],
            'word_count': len(found_words)
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 400


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
