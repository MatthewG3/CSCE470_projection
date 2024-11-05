import json
import math

# Load the events data from the file
with open('events_data.json', 'r') as file:
    events_dict = json.load(file)

# Initialize data for TF, IDF, and BM25 scores
data = {}
N = len(events_dict)  # Total number of documents

# Calculate term frequency for each event title and text
for event in events_dict:
    event_id = event['id']
    data[event_id] = {
        'title': event['name'],
        'text': event['story'],
        'tf_title': {},
        'tf_text': {}
    }
    
    # Calculate TF for title
    words_title = event['name'].split()
    for word in words_title:
        data[event_id]['tf_title'][word] = data[event_id]['tf_title'].get(word, 0) + 1
    
    # Calculate TF for text
    words_text = event['story'].split()
    for word in words_text:
        data[event_id]['tf_text'][word] = data[event_id]['tf_text'].get(word, 0) + 1

# Calculate IDF for words in all titles and texts
idf_title = {}
idf_text = {}

for event in data.values():
    unique_words_title = set(event['tf_title'].keys())
    unique_words_text = set(event['tf_text'].keys())

    for word in unique_words_title:
        idf_title[word] = idf_title.get(word, 0) + 1

    for word in unique_words_text:
        idf_text[word] = idf_text.get(word, 0) + 1

# Finalize IDF calculations
for word in idf_title:
    idf_title[word] = math.log((N - idf_title[word] + 0.5) / (idf_title[word] + 0.5) + 1)

for word in idf_text:
    idf_text[word] = math.log((N - idf_text[word] + 0.5) / (idf_text[word] + 0.5) + 1)

# BM25 calculation function
def bm25(tf, idf, avg_len, doc_len, k1=1.5, b=0.75):
    score = 0
    for word, freq in tf.items():
        if word in idf:
            numerator = idf[word] * freq * (k1 + 1)
            denominator = freq + k1 * (1 - b + b * (doc_len / avg_len))
            score += numerator / denominator
    return score

# Average lengths for title and text
avg_len_title = sum(len(event['title'].split()) for event in data.values()) / N
avg_len_text = sum(len(event['text'].split()) for event in data.values()) / N

# Calculate BM25 scores for each title and text
for event_id, event_data in data.items():
    len_title = len(event_data['title'].split())
    len_text = len(event_data['text'].split())

    event_data['bm25_title'] = bm25(event_data['tf_title'], idf_title, avg_len_title, len_title)
    event_data['bm25_text'] = bm25(event_data['tf_text'], idf_text, avg_len_text, len_text)

# Display basic BM25 scores for titles
#for event_id, event_data in data.items():
 #   print(f"Event ID: {event_id}")
  #  print(f"Title: {event_data['title']}")
   # print(f"BM25 Score (Title): {event_data['bm25_title']:.2f}")
    #print(f"BM25 Score (Text): {event_data['bm25_text']:.2f}")
    #print()

# Extract top 10 BM25 scores for title and text
top_10_titles = sorted(data.items(), key=lambda x: x[1]['bm25_title'], reverse=True)[:10]
top_10_texts = sorted(data.items(), key=lambda x: x[1]['bm25_text'], reverse=True)[:10]

# Print the top 10 BM25 scores for titles
print("Top 10 BM25 Scores for Titles:")
for event_id, event_data in top_10_titles:
    print(f"Event ID: {event_id}")
    print(f"Title: {event_data['title']}")
    print(f"BM25 Score (Title): {event_data['bm25_title']:.2f}")
    print()

# Print the top 10 BM25 scores for texts
print("Top 10 BM25 Scores for Texts:")
for event_id, event_data in top_10_texts:
    print(f"Event ID: {event_id}")
    print(f"Title: {event_data['title']}")
    print(f"BM25 Score (Text): {event_data['bm25_text']:.2f}")
    print()


# Function to calculate TF for a query
def calculate_tf_for_query(query):
    tf_query = {}
    words = query.split()
    for word in words:
        tf_query[word] = tf_query.get(word, 0) + 1
    return tf_query

# Function to calculate BM25 score for a query
def bm25_query(query_tf, document_tf, idf, avg_len, doc_len, k1=1.5, b=0.75):
    return bm25({word: query_tf.get(word, 0) * freq for word, freq in document_tf.items()}, idf, avg_len, doc_len, k1, b)

# User search function
def search_events(query):
    query_tf = calculate_tf_for_query(query)
    results = []

    for event_id, event_data in data.items():
        score_title = bm25_query(query_tf, event_data['tf_title'], idf_title, avg_len_title, len(event_data['title'].split()))
        score_text = bm25_query(query_tf, event_data['tf_text'], idf_text, avg_len_text, len(event_data['text'].split()))
        results.append((event_id, event_data['title'], score_title, score_text))
    
    # Sort results by BM25 score for the title and return the top results
    results = sorted(results, key=lambda x: x[2], reverse=True)[:10]
    
    print("Top 10 Results for Your Query:")
    for event_id, title, score_title, score_text in results:
        print(f"Event ID: {event_id}")
        print(f"Title: {title}")
        print(f"BM25 Score (Title): {score_title:.2f}")
        print(f"BM25 Score (Text): {score_text:.2f}")
        print()

query = input("Enter your search query: ")
search_events(query)
