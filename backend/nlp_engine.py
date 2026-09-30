import json
import os
import re

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

try:
    from nltk.corpus import stopwords
    from nltk.stem import WordNetLemmatizer
except Exception:
    stopwords = None
    WordNetLemmatizer = None

FALLBACK_STOPWORDS = {
    'a', 'about', 'above', 'after', 'again', 'against', 'all', 'am', 'an', 'and', 'any', 'are',
    'as', 'at', 'be', 'because', 'been', 'before', 'being', 'below', 'between', 'both', 'but',
    'by', 'can', 'did', 'do', 'does', 'doing', 'down', 'during', 'each', 'few', 'for', 'from',
    'further', 'had', 'has', 'have', 'having', 'he', 'her', 'here', 'hers', 'herself', 'him',
    'himself', 'his', 'how', 'i', 'if', 'in', 'into', 'is', 'it', 'its', 'itself', 'just', 'me',
    'more', 'most', 'my', 'myself', 'no', 'nor', 'not', 'of', 'off', 'on', 'once', 'only', 'or',
    'other', 'our', 'ours', 'ourselves', 'out', 'over', 'own', 'same', 'she', 'should', 'so',
    'some', 'such', 'than', 'that', 'the', 'their', 'theirs', 'them', 'themselves', 'then',
    'there', 'these', 'they', 'this', 'those', 'through', 'to', 'too', 'under', 'until', 'up',
    'very', 'was', 'we', 'were', 'what', 'when', 'where', 'which', 'while', 'who', 'whom', 'why',
    'with', 'you', 'your', 'yours', 'yourself', 'yourselves'
}

class NLPEngine:
    def __init__(self, data_path="data/dataset.json"):
        self.lemmatizer = None
        if WordNetLemmatizer is not None:
            try:
                self.lemmatizer = WordNetLemmatizer()
                self.lemmatizer.lemmatize("tests")
            except LookupError:
                self.lemmatizer = None

        try:
            self.stop_words = set(stopwords.words('english')) if stopwords is not None else FALLBACK_STOPWORDS
        except LookupError:
            self.stop_words = FALLBACK_STOPWORDS
        self.vectorizer = TfidfVectorizer()
        
        self.dataset = self.load_data(data_path)
        self.corpus = []
        self.disease_mapping = []
        self.prepare_corpus()

    def lemmatize_word(self, word):
        if self.lemmatizer is not None:
            return self.lemmatizer.lemmatize(word)

        if word.endswith("ies") and len(word) > 4:
            return word[:-3] + "y"
        if word.endswith("sses"):
            return word[:-2]
        if word.endswith("ing") and len(word) > 5:
            return word[:-3]
        if word.endswith("ed") and len(word) > 4:
            return word[:-2]
        if word.endswith("es") and len(word) > 3 and not word.endswith("ses"):
            return word[:-2]
        if word.endswith("s") and len(word) > 3 and not word.endswith("ss"):
            return word[:-1]
        return word

    def load_data(self, path):
        # Resolve absolute path relative to this script
        base_dir = os.path.dirname(os.path.abspath(__file__))
        full_path = os.path.join(base_dir, path)
        with open(full_path, 'r', encoding='utf-8') as f:
            return json.load(f)

    def preprocess_text(self, text):
        if text is None:
            return ""

        tokens = re.findall(r"[a-zA-Z]+(?:'[a-zA-Z]+)?", str(text).lower())
        processed_tokens = []
        for word in tokens:
            if word in self.stop_words or not word.isalpha():
                continue
            processed_tokens.append(self.lemmatize_word(word))
        return " ".join(processed_tokens)

    def prepare_corpus(self):
        for item in self.dataset:
            disease = item['disease']
            # We train on the symptoms
            for symptom in item['symptoms']:
                processed_symptom = self.preprocess_text(symptom)
                if processed_symptom.strip():
                    self.corpus.append(processed_symptom)
                    self.disease_mapping.append(disease)
            # Add the disease name itself as a feature
            self.corpus.append(self.preprocess_text(disease))
            self.disease_mapping.append(disease)
            
        # Fit vectorizer on corpus
        if self.corpus:
            self.tfidf_matrix = self.vectorizer.fit_transform(self.corpus)

    def get_disease_info(self, disease_name):
        for item in self.dataset:
            if item['disease'].lower() == disease_name.lower():
                return item
        return None

    def predict(self, user_input, knows_disease=False):
        try:
            if knows_disease:
                # Direct match
                for item in self.dataset:
                    if item['disease'].lower() in user_input.lower():
                        return {
                            "disease": item['disease'],
                            "treatment": item['treatment'],
                            "confidence": 1.0,
                            "disclaimer": "Disclaimer: This is an AI prediction. Please consult a real doctor for medical advice."
                        }
                return {
                    "disease": "Unknown",
                    "treatment": "Sorry, I couldn't find a direct match for that disease. Could you please check your spelling or try describing your symptoms instead?",
                    "confidence": 0.0,
                    "disclaimer": "Disclaimer: This is an AI prediction. Please consult a real doctor for medical advice."
                }
            
            # Predict based on symptoms
            processed_input = self.preprocess_text(user_input)
            if not processed_input.strip():
                return {
                    "disease": "Unknown",
                    "treatment": "I couldn't quite understand that. Please describe your symptoms using simple English words (e.g., 'I have a fever' or 'my head hurts').",
                    "confidence": 0.0,
                    "disclaimer": "Disclaimer: This is an AI prediction. Please consult a real doctor for medical advice."
                }

            input_vector = self.vectorizer.transform([processed_input])
            
            # Calculate cosine similarity
            similarities = cosine_similarity(input_vector, self.tfidf_matrix)
            best_match_idx = np.argmax(similarities)
            max_similarity = similarities[0][best_match_idx]
            
            # Lowered threshold to 0.01 to allow very simple English to match even a single token
            if max_similarity > 0.01: 
                predicted_disease = self.disease_mapping[best_match_idx]
                info = self.get_disease_info(predicted_disease)
                return {
                    "disease": info['disease'],
                    "treatment": info['treatment'],
                    "confidence": float(max_similarity),
                    "disclaimer": "Disclaimer: This is an AI prediction. Please consult a real doctor for medical advice."
                }
            else:
                return {
                    "disease": "Unknown",
                    "treatment": "Sorry, I couldn't clearly identify your condition from those symptoms. I recommend you visit a clinic or hospital for a professional checkup.",
                    "confidence": float(max_similarity),
                    "disclaimer": "Disclaimer: This is an AI prediction. Please consult a real doctor for medical advice."
                }
        except Exception as e:
            print(f"Error in prediction: {e}")
            return {
                "disease": "Error",
                "treatment": "An internal error occurred while processing your request. Please try again.",
                "confidence": 0.0,
                "disclaimer": "Disclaimer: This is an AI prediction. Please consult a real doctor for medical advice."
            }
