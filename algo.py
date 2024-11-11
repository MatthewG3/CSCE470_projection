import json
import math
from flask import Flask, request

class Algo:

    def __init__(self):
        self.data, self.N, self.idf_title, self.idf_text = self.retrieve_data()
        # Average lengths for title and text
        self.avg_len_title = sum(len(event['title'].split()) for event in self.data.values()) / self.N
        self.avg_len_text = sum(len(event['text'].split()) for event in self.data.values()) / self.N

    def retrieve_data(self):
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

        return (data, N, idf_title, idf_text)

    # BM25 calculation function
    def bm25(self, tf, idf, avg_len, doc_len, k1=1.5, b=0.75):
        score = 0
        for word, freq in tf.items():
            if word in idf:
                numerator = idf[word] * freq * (k1 + 1)
                denominator = freq + k1 * (1 - b + b * (doc_len / avg_len))
                score += numerator / denominator
        return score
    
    # Function to calculate TF for a query
    def calculate_tf_for_query(self, query):
        tf_query = {}
        words = query.split()
        for word in words:
            tf_query[word] = tf_query.get(word, 0) + 1
        return tf_query

    # Function to calculate BM25 score for a query
    def bm25_query(self, query_tf, document_tf, idf, avg_len, doc_len, k1=1.5, b=0.75):
        return self.bm25({word: query_tf.get(word, 0) * freq for word, freq in document_tf.items()}, idf, avg_len, doc_len, k1, b)

    # User search function
    def search_events(self, query):
        query_tf = self.calculate_tf_for_query(query)
        results = []

        for event_id, event_data in self.data.items():
            score_title = self.bm25_query(query_tf, event_data['tf_title'], self.idf_title, self.avg_len_title, len(event_data['title'].split()))
            score_text = self.bm25_query(query_tf, event_data['tf_text'], self.idf_text, self.avg_len_text, len(event_data['text'].split()))
            results.append((event_id, event_data['title'], score_title, score_text))
        
        # Sort results by BM25 score for the title and return the top results
        results = sorted(results, key=lambda x: x[2], reverse=True)[:10]

        res = {}
        res['results'] = results
        return res


app = Flask(__name__)
algo = Algo()

# ex: http://127.0.0.1:5000/search?query=Denver+Broncos
@app.route("/search")
def search():
    query = request.args.get("query")
    query = query.replace('+', ' ')
    results = algo.search_events(query)
    return results


if __name__ == "__main__":
    app.run(debug=True)
