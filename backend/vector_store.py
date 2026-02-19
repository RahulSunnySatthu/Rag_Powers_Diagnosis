from sklearn.metrics.pairwise import cosine_similarity


class VectorStore:
    def __init__(self):
        self.embedding_model = None

    def set_embedding_model(self, embedding_model):
        """
        Attach embedding model (TF-IDF wrapper)
        """
        self.embedding_model = embedding_model

    def add_documents(self, texts):
        """
        Fit TF-IDF on document chunks
        """
        if not texts:
            return

        self.embedding_model.fit_transform(texts)

    def search(self, query, top_k=3, threshold=0.05):
        """
        Retrieve top-k relevant chunks and return:
        - list of retrieved chunks
        - highest similarity score (confidence)
        """

        # Safety check
        if (
            self.embedding_model is None
            or self.embedding_model.document_matrix is None
        ):
            return [], 0.0

        query = query.lower()
        query_vector = self.embedding_model.transform_query(query)

        similarities = cosine_similarity(
            query_vector,
            self.embedding_model.document_matrix
        )[0]

        # 🔥 Keyword boosting (important for medical queries)
        for i, doc in enumerate(self.embedding_model.documents):
            if any(word in doc.lower() for word in query.split()):
                similarities[i] += 0.1

        max_similarity = float(similarities.max())

        # Sort indices by similarity (descending)
        top_indices = similarities.argsort()[-top_k:][::-1]

        results = []
        for i in top_indices:
            if similarities[i] >= threshold:
                results.append(self.embedding_model.documents[i])

        return results, max_similarity
