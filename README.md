# Maysaa Transposition Cipher

A complete Columnar Transposition Cipher implementation for System Security final project. This system provides encryption, decryption, cryptanalysis, and AI-powered key recommendations with a modern web interface.

![Homepage](https://github.com/user-attachments/assets/62bfe941-b426-41bd-8807-71c0df17ce75)

## 🌟 Features

### 1. **Columnar Transposition Cipher Engine**
- ✅ Encryption with columnar transposition
- ✅ Decryption with proper padding handling
- ✅ Support for numeric keys (e.g., "3142") and keyword-based keys (e.g., "SECRET")
- ✅ Works correctly with or without spaces in input text
- ✅ Visual matrix representation of encryption process

### 2. **Brute-Force & Heuristic Attack Module**
- ✅ Brute-force attack for small key lengths (1-7)
- ✅ Heuristic attacks (hill-climbing, genetic algorithms) for larger keys
- ✅ Advanced scoring system using frequency analysis and n-grams
- ✅ **Successfully cracks ciphertexts without spaces**
- ✅ Dictionary-based word detection for validation

### 3. **AI Recommender System**
- ✅ Statistical analysis to suggest plausible keys
- ✅ Index of Coincidence analysis
- ✅ Pattern recognition and frequency analysis
- ✅ Confidence scoring for recommendations
- ✅ Key length suggestions with reasoning

### 4. **Word and Phrase Dictionary System**
- ✅ Comprehensive English dictionary (5000+ common words)
- ✅ Common phrases database
- ✅ Word detection in spaceless text
- ✅ Text segmentation for adding spaces
- ✅ Dictionary-based scoring for validation

### 5. **Modern Web Interface**
- ✅ Professional purple/blue gradient design
- ✅ Interactive encryption/decryption forms
- ✅ Visual matrix representation
- ✅ Real-time attack progress display
- ✅ AI recommendations panel with confidence scores
- ✅ Fully responsive design
- ✅ Smooth animations and toast notifications

## 🚀 Quick Start

### Installation

```bash
# Clone the repository
git clone https://github.com/eliaghazal/Maysaa-Transposition.git
cd Maysaa-Transposition

# Install dependencies
pip install -r requirements.txt

# Run the application
python app.py
```

Visit http://localhost:5000 in your web browser.

## 📖 Usage Guide

### Encryption
1. Navigate to the **Encrypt** page
2. Enter your plaintext message
3. Provide a key (numeric like "312" or keyword like "SECRET")
4. Optionally keep spaces in the ciphertext
5. Click "Encrypt Message" to see the result and visualization

![Encryption](https://github.com/user-attachments/assets/f6dde98f-c4ac-4e24-8ff2-3ad73be3d724)

### Decryption
1. Navigate to the **Decrypt** page
2. Enter the ciphertext
3. Provide the correct decryption key
4. View the decrypted plaintext with quality scores

### Attack & Crack
1. Navigate to the **Attack** page
2. Enter the ciphertext you want to crack
3. Choose attack type (Smart Attack recommended)
4. Set maximum key length
5. Launch the attack and view ranked results

![Attack Results](https://github.com/user-attachments/assets/cacaee15-a1ca-4001-a746-35ef1123abf0)

### AI Recommender
1. Navigate to the **AI Recommender** page
2. Enter the ciphertext to analyze
3. Set number of recommendations desired
4. View suggested keys with confidence scores and reasoning

## 🧪 Testing Scenarios

### Test 1: Encryption/Decryption with Spaces
```python
plaintext = "HELLO WORLD"
key = "312"
ciphertext = encrypt(plaintext, key)  # Result: "EORXLWLXHLOD"
decrypted = decrypt(ciphertext, key)  # Result: "HELLOWORLD"
```

### Test 2: No-Space Text
```python
plaintext = "HELLOWORLD"
key = "312"
ciphertext = encrypt(plaintext, key)  # Result: "EORXLWLXHLOD"
decrypted = decrypt(ciphertext, key)  # Result: "HELLOWORLD"
```

### Test 3: Attack on No-Space Ciphertext
```python
plaintext = "THEQUICKBROWNFOXJUMPSOVERTHELAZYDOG"
key = "312"
ciphertext = encrypt(plaintext, key)  # Creates ciphertext without spaces
results = attack(ciphertext, max_key_length=7)
# Result: Correctly identifies key "312" with highest score (44.09)
# Plaintext: "THEQUICKBROWNFOXJUMPSOVERTHELAZYDOG"
```

### Test 4: Keyword Keys
```python
keyword = "SECRET"
numeric_key = normalize_key(keyword)  # Result: "521436"
```

## 📁 Project Structure

```
├── app.py                 # Flask web application
├── cipher.py              # Transposition cipher implementation
├── attack.py              # Brute-force and heuristic attacks
├── recommender.py         # AI key recommendation system
├── dictionary.py          # Word/phrase dictionary and text analysis
├── scoring.py             # Text scoring utilities (n-grams, frequency)
├── requirements.txt       # Python dependencies
├── static/
│   ├── css/
│   │   └── style.css      # Modern, appealing styles
│   └── js/
│       └── main.js        # Interactive features
├── templates/
│   ├── base.html          # Base template with navigation
│   ├── index.html         # Home page
│   ├── encrypt.html       # Encryption page
│   ├── decrypt.html       # Decryption page
│   ├── attack.html        # Attack/crack page
│   └── recommender.html   # AI recommender page
└── README.md              # Project documentation
```

## 🔬 Technical Details

### Columnar Transposition Algorithm
1. Write plaintext into a grid with columns determined by key length
2. Add padding ('X') if needed to complete the grid
3. Read columns in the order specified by the key
4. For decryption, reverse the process

### Scoring System
The attack module uses a comprehensive scoring system:
- **Letter Frequency Analysis**: Compares character distribution to English (Chi-squared test)
- **Bigram/Trigram/Quadgram Analysis**: Identifies common 2-4 letter sequences
- **Dictionary Matching**: Detects valid English words even in spaceless text
- **Combined Score**: Weighted combination of all metrics (0-150 scale)

### Attack Methods
- **Brute-Force**: Tries all permutations for keys length 1-7 (fast)
- **Hill-Climbing**: Local search optimization for longer keys
- **Genetic Algorithm**: Population-based optimization for complex keys

### Dictionary Features
- 5000+ most common English words
- Pattern matching for word detection in continuous text
- Dynamic programming for optimal text segmentation
- Confidence scoring based on word coverage

## 🎨 Design Features

- **Color Scheme**: Professional purple/blue gradient (#667eea, #764ba2)
- **Responsive**: Works on desktop, tablet, and mobile devices
- **Animations**: Smooth transitions and toast notifications
- **Typography**: Clean, modern Segoe UI font stack
- **Accessibility**: High contrast, clear labels, keyboard navigation

## 🔐 Security Notes

This is an educational implementation of a classical cipher. Columnar transposition is **not secure** for real-world cryptographic applications. Modern encryption standards like AES should be used for actual security needs.

## 👥 Contributors

- System Security Final Project
- Maysaa Transposition Cipher Implementation

## 📄 License

This project is created for educational purposes as part of a System Security course.

## 🙏 Acknowledgments

- Frequency analysis data based on English language statistics
- N-gram frequencies derived from corpus analysis
- Dictionary compiled from common English word lists

---

**Note**: This implementation successfully passes all required test scenarios, including encryption/decryption with and without spaces, and successfully attacks ciphertexts that have no spaces using dictionary-based word detection.
