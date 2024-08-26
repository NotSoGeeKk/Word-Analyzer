import pandas as pd
import os
from DataExtraction import extract_article_text
from sentimentAnalysis import analyze_sentiment_per_file
from AnalysisOfReadability import analyze_readability_per_file
from WordAnalysis import analyze_and_print_files

text_files_path = "extracted_articles"
stop_words_path = "StopWords"
def main():
    # Step 1: Data Extraction
    print("Starting Data Extraction...")
    df = pd.read_excel('Input.xlsx')
    
    if not os.path.exists('extracted_articles'):
        os.makedirs('extracted_articles')
    
    for index, row in df.iterrows():
        url_id = row['URL_ID']
        url = row['URL']
        article_content = extract_article_text(url)
        file_name = f"extracted_articles/{url_id}.txt"
        with open(file_name, 'w', encoding='utf-8') as file:
            file.write(article_content)
        print(f"Article {url_id} extracted and saved.")
    
    print("Data Extraction completed.")

    # Step 2: Sentiment Analysis
    print("Starting Sentiment Analysis...")
    sentiment_results = analyze_sentiment_per_file()
    print("Sentiment Analysis completed.")

    # Step 3: Readability Analysis
    print("Starting Readability Analysis...")
    readability_results = analyze_readability_per_file()
    print("Readability Analysis completed.")

    # Step 4: Word Analysis
    print("Starting Word Analysis...")
    word_results = analyze_and_print_files(text_files_path, stop_words_path)
    print("Word Analysis completed.")

    # Step 5: Combine results and save to CSV
    print("Combining results and saving to CSV...")
    output_data = []
    for filename in os.listdir('extracted_articles'):
        if filename.endswith('.txt'):
            url_id = filename.split('.')[0]
            try:
                # Fetch the URL from the dataframe without converting to int
                row_data = {
                    'URL_ID': url_id,
                    'URL': df[df['URL_ID'] == url_id]['URL'].values[0],
                    'POSITIVE SCORE': sentiment_results[filename]['positive_words'],
                    'NEGATIVE SCORE': sentiment_results[filename]['negative_words'],
                    'POLARITY SCORE': sentiment_results[filename]['polarity_score'],
                    'SUBJECTIVITY SCORE': sentiment_results[filename]['subjectivity_score'],
                    'AVG SENTENCE LENGTH': readability_results[filename]['avg_sentence_length'],
                    'PERCENTAGE OF COMPLEX WORDS': readability_results[filename]['percent_complex_words'],
                    'FOG INDEX': readability_results[filename]['fog_index'],
                    'COMPLEX WORD COUNT': readability_results[filename]['num_complex_words'],
                    'WORD COUNT': readability_results[filename]['num_words'],
                    'SYLLABLE PER WORD': word_results[filename]['total_syllables'],
                    'PERSONAL PRONOUNS': word_results[filename]['total_pronouns'],
                    'AVG WORD LENGTH': word_results[filename]['avg_word_length'],
                }
                output_data.append(row_data)
            except IndexError:
                print(f"No matching URL found for URL_ID: {url_id}")
                continue

    output_df = pd.DataFrame(output_data)
    output_df.to_csv('Output.csv', index=False)
    print("Results saved to Output.csv")

    print("All tasks completed successfully!")

if __name__ == "__main__":
    main()
