import os
import re

def count_syllables(word):
    word = word.lower()
    count = 0
    vowels = "aeiouy"
    if word[0] in vowels:
        count += 1
    for index in range(1, len(word)):
        if word[index] in vowels and word[index - 1] not in vowels:
            count += 1
    if word.endswith("e"):
        count -= 1
    if count == 0:
        count += 1
    return count

def simple_sentence_tokenize(text):
    return re.split(r'(?<=[.!?])\s+', text)

def calculate_avg_words_per_sentence(num_words, num_sentences):
    return num_words / num_sentences if num_sentences > 0 else 0

def analyze_readability_per_file():
    file_readability = {}

    for filename in os.listdir('extracted_articles'):
        if filename.endswith('.txt'):
            filepath = os.path.join('extracted_articles', filename)
            
            with open(filepath, 'r', encoding='utf-8') as file:
                content = file.read()

            # Count sentences using the simple tokenizer
            sentences = simple_sentence_tokenize(content)
            num_sentences = len(sentences)

            # Count words
            words = re.findall(r'\b\w+\b', content.lower())
            num_words = len(words)

            # Count complex words
            complex_words = [word for word in words if count_syllables(word) > 2]
            num_complex_words = len(complex_words)

            # Calculate metrics
            avg_sentence_length = calculate_avg_words_per_sentence(num_words, num_sentences)
            percent_complex_words = (num_complex_words / num_words) * 100 if num_words > 0 else 0
            fog_index = 0.4 * (avg_sentence_length + percent_complex_words)

            file_readability[filename] = {
                'num_sentences': num_sentences,
                'num_words': num_words,
                'num_complex_words': num_complex_words,
                'avg_sentence_length': avg_sentence_length,
                'percent_complex_words': percent_complex_words,
                'fog_index': fog_index
            }

    return file_readability

# Usage
'''results = analyze_readability_per_file()
for filename, readability in results.items():
    print(f"File: {filename}")
    print(f"Average Sentence length: {readability['avg_sentence_length']:.2f}")
    print(f"Percentage of Complex Words: {readability['percent_complex_words']:.2f}%")
    print(f"Fog Index: {readability['fog_index']:.2f}")
    print(f"Total Complex Words: {readability['num_complex_words']}")
    print("--------------------")'''