import os
from collections import Counter

def analyze_sentiment_per_file():
    file_sentiments = {}

    with open('MasterDictionary/positive-words.txt', 'r') as f:
        positive_words = set(f.read().splitlines())
    with open('MasterDictionary/negative-words.txt', 'r') as f:
        negative_words = set(f.read().splitlines())

    for filename in os.listdir('extracted_articles'):
        if filename.endswith('.txt'):
            filepath = os.path.join('extracted_articles', filename)
            
            positive_count = Counter()
            negative_count = Counter()
            total_words = 0

            with open(filepath, 'r', encoding='utf-8') as file:
                content = file.read().lower().split()
                total_words = len(content)
                
                positive_count.update(word for word in content if word in positive_words)
                negative_count.update(word for word in content if word in negative_words)

            positive_score = sum(positive_count.values())
            negative_score = sum(negative_count.values())
            
            # Calculate Polarity Score
            polarity_score = (positive_score - negative_score) / ((positive_score + negative_score) + 0.000001)
            
            # Calculate Subjectivity Score
            subjectivity_score = (positive_score + negative_score) / (total_words + 0.000001)
            
            file_sentiments[filename] = {
                'total_words': total_words,
                'positive_words': positive_score,
                'negative_words': negative_score,
                'positive_ratio': positive_score / total_words if total_words > 0 else 0,
                'negative_ratio': negative_score / total_words if total_words > 0 else 0,
                'most_common_positive': positive_count.most_common(5),
                'most_common_negative': negative_count.most_common(5),
                'polarity_score': polarity_score,
                'subjectivity_score': subjectivity_score
            }

    return file_sentiments

# Usage Uncomment to see all the data for diffenrent files
'''results = analyze_sentiment_per_file()
for filename, sentiment in results.items():
    print(f"File: {filename}")
    print(f"Positive Score:{sentiment['positive_words']:.4f}")
    print(f"Negative Score:{sentiment['negative_words']:.4f}")
    print(f"Polarity Score: {sentiment['polarity_score']:.4f}")
    print(f"Subjectivity Score: {sentiment['subjectivity_score']:.4f}")
    print("--------------------")'''