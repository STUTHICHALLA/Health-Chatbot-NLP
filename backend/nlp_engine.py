import json
import nltk
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
import os

# Download necessary NLTK data
nltk.download('punkt', quiet=True)
nltk.download('punkt_tab', quiet=True)
nltk.download('stopwords', quiet=True)
nltk.download('wordnet', quiet=True)

from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer

class NLPEngine:
    def __init__(self, data_path="data/dataset.json"):
        self.lemmatizer = WordNetLemmatizer()
        self.stop_words = set(stopwords.words('english'))
        self.vectorizer = TfidfVectorizer()
        
        self.dataset = self.load_data(data_path)
        self.corpus = []
        self.disease_mapping = []
        self.prepare_corpus()

    def load_data(self, path):
        # Resolve absolute path relative to this script
        base_dir = os.path.dirname(os.path.abspath(__file__))
        full_path = os.path.join(base_dir, path)
        with open(full_path, 'r', encoding='utf-8') as f:
            return json.load(f)

    def preprocess_text(self, text):
        # Tokenize and lowercase
        tokens = word_tokenize(text.lower())
        # Remove stopwords and non-alphabetic tokens, then lemmatize
        processed_tokens = [
            self.lemmatizer.lemmatize(word) 
            for word in tokens 
            if word.isalpha() and word not in self.stop_words
        ]
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
