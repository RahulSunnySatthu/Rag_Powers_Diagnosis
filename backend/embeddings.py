from sklearn.feature_extraction.text import TfidfVectorizer


class TfidfEmbedding:

    def __init__(self):
        self.vectorizer = TfidfVectorizer(stop_words="english")
        self.document_matrix = None
        self.documents = []

    def fit_transform(self, texts):
        self.documents = texts
        self.document_matrix = self.vectorizer.fit_transform(texts)

    def transform_query(self, query):
        return self.vectorizer.transform([query])
