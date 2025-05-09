from sentence_transformers import SentenceTransformer
import pickle

embedding_model_name = "vector_models/all-MiniLM-L6-v2"
faiss_index_path = "files/faiss_index.pkl"


def load_vector_store(load_path):
    try:
        with open(load_path, "rb") as f:
            loaded_vector_store = pickle.load(f)
            print(f"FAISS index loaded from: {load_path}")
            return loaded_vector_store
    except Exception as e:
        print(f"Error loading FAISS index from '{load_path}': {e}")
        return None


embedding_model = SentenceTransformer(embedding_model_name)  # Load model for loading
vector_store = load_vector_store(faiss_index_path)


class UserQueryContext(object):

    def retrieve_relevant_chunks(self, vector_store, query, embedding_model, k=5):
        query_embedding = embedding_model.encode(query)
        similar_docs = vector_store.similarity_search_by_vector(query_embedding, k=k)
        print(f"\nRetrieved {len(similar_docs)} relevant chunks for the query: '{query}'")
        return similar_docs

    def get_query_context(self, query, top_matches):
        context = ""
        relevant_chunks = self.retrieve_relevant_chunks(vector_store, query, embedding_model, top_matches)
        for chunk in relevant_chunks:
            context = context + " " + chunk.page_content
        return context

