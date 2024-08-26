import pandas as pd
import requests
from bs4 import BeautifulSoup
import os

def extract_article_text(url):
    try:
        # Send a GET request to the URL
        response = requests.get(url)
        response.raise_for_status()  # Raise an exception for bad status codes
        
        # Parse the HTML content
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Extract the title
        title = soup.find('h1').text.strip()
        
        # Extract the article text
        # This is a basic implementation and may need to be adjusted based on the specific structure of the websites
        article_body = soup.find('article') or soup.find('div', class_='article-body')
        if article_body:
            paragraphs = article_body.find_all('p')
            article_text = '\n\n'.join([p.text.strip() for p in paragraphs])
        else:
            article_text = "Could not extract article text."
        
        return f"{title}\n\n{article_text}"
    
    except Exception as e:
        return f"Error extracting article: {str(e)}"