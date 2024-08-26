import os
import re
import string
import chardet
from nltk.tokenize import word_tokenize

# Define the paths
text_files_path = "extracted_articles"
stop_words_path = "StopWords"

# Function to detect file encoding
def detect_encoding(file_path):
    with open(file_path, 'rb') as file:
        raw_data = file.read()
    result = chardet.detect(raw_data)
    return result['encoding']

# Load stop words from all text files in the stop words directory
def load_stop_words(directory):
    stop_words = set()
    for filename in os.listdir(directory):
        if filename.endswith(".txt"):
            file_path = os.path.join(directory, filename)
            encoding = detect_encoding(file_path)
            with open(file_path, 'r', encoding=encoding, errors='replace') as file:
                stop_words.update(file.read().splitlines())
    return stop_words

# Function to count words after removing stop words and punctuations
def word_count(text, stop_words):
    # Remove punctuation
    text = text.translate(str.maketrans('', '', string.punctuation))
    words = word_tokenize(text.lower())
    filtered_words = [word for word in words if word not in stop_words]
    return len(filtered_words), filtered_words

# Function to count syllables per word
def syllable_count(word):
    word = word.lower()
    syllable_count = 0
    vowels = "aeiouy"

    if word[0] in vowels:
        syllable_count += 1

    for index in range(1, len(word)):
        if word[index] in vowels and word[index - 1] not in vowels:
            syllable_count += 1

    if word.endswith("es") or word.endswith("ed"):
        if len(word) > 2 and word[-3] not in vowels:
            syllable_count -= 1

    if syllable_count == 0:
        syllable_count = 1

    return syllable_count

# Function to count personal pronouns
def count_personal_pronouns(text):
    pronouns = re.findall(r"\b(I|we|my|ours|us)\b", text, re.I)
    # Exclude the word 'US' if it's not intended as a pronoun
    pronouns = [p for p in pronouns if not re.fullmatch(r"US", p, re.I)]
    return len(pronouns)

# Function to calculate average word length
def average_word_length(words):
    total_chars = sum(len(word) for word in words)
    return total_chars / len(words) if words else 0

# Function to process and print analysis for each file
def analyze_and_print_files(text_files_path, stop_words_path):
    results = {}

    # Load stop words
    stop_words = load_stop_words(stop_words_path)

    # Process each file in the text files directory
    for filename in os.listdir(text_files_path):
        if filename.endswith(".txt"):
            file_path = os.path.join(text_files_path, filename)
            encoding = detect_encoding(file_path)

            with open(file_path, 'r', encoding=encoding, errors='replace') as file:
                text = file.read()

                # Word Count
                total_words, filtered_words = word_count(text, stop_words)

                # Syllable Count
                syllables_per_word = [syllable_count(word) for word in filtered_words]
                total_syllables = sum(syllables_per_word)

                # Personal Pronouns
                total_pronouns = count_personal_pronouns(text)

                # Average Word Length
                avg_word_length = average_word_length(filtered_words)

                # Store results in the dictionary
                results[filename] = {
                    'total_words': total_words,
                    'total_syllables': total_syllables,
                    'total_pronouns': total_pronouns,
                    'avg_word_length': avg_word_length,
                }

    return results

                # Output results
    '''print(f"Results for {filename}:")
                print(f"Total Cleaned Words: {total_words}")
                print(f"Total Syllables: {total_syllables}")
                print(f"Personal Pronouns Count: {total_pronouns}")
                print(f"Average Word Length: {avg_word_length:.2f}\n")'''
