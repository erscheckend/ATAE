import os
import PyPDF2
import argparse
from collections import Counter

# Function to extract text from a PDF file
def extract_text_from_pdf(pdf_path):
    with open(pdf_path, 'rb') as file:
        reader = PyPDF2.PdfReader(file)
        text = ''
        for page in reader.pages:
            text += page.extract_text()
    return text

# Function to count the occurrences of words in text
def count_words(text, words):
    text = text.lower()
    word_count = Counter()
    for word in words:
        word_count[word] = text.count(word)
    return word_count

# Main function
def main(folder_path):
    # Words to search for
    search_words = ['app ', 'apps', 'mobile']

    # Dictionary to store results
    results = {}

    # Iterate over all PDF files in the folder
    for filename in os.listdir(folder_path):
        if filename.endswith('.pdf'):
            pdf_path = os.path.join(folder_path, filename)
            text = extract_text_from_pdf(pdf_path)
            word_count = count_words(text, search_words)
            total_hits = sum(word_count.values())
            results[filename] = {
                'word_count': word_count,
                'total_hits': total_hits
            }

    # Sort results by total hits
    sorted_results = sorted(results.items(), key=lambda item: item[1]['total_hits'], reverse=True)

    # Create the output file with the ranking
    with open('output_ranking.txt', 'w') as output_file:
        for filename, data in sorted_results:
            output_file.write(f"{filename} - Total Hits: {data['total_hits']}\n")
            for word, count in data['word_count'].items():
                output_file.write(f"  {word}: {count}\n")
            output_file.write('\n')

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Count word occurrences in PDF files within a folder.")
    parser.add_argument('folder_path', type=str, help='Path to the folder containing PDF files.')
    args = parser.parse_args()
    main(args.folder_path)
