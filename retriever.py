from embeddings import Embeddings
from langchain_community.vectorstores import Chroma

from model import Model


class Retriever:
    CHROMA_PATH = "chroma"

    def __init__(self, db:Chroma):
        self.embedding_function = Embeddings.get_embeddings()
        self.db = db

    def search_db(self, query_text, k=3, score_threshold=0.7):
        results = self.db.similarity_search_with_relevance_scores(query_text, k=k)
        if not results or results[0][1] < score_threshold:
            return None
        return results

    @staticmethod
    def format_context(results):
        return "\n\n---\n\n".join([doc.page_content for doc, _score in results])

    @staticmethod
    def format_output(response_text, sources):
        return f"Response: {response_text}\nSources: {sources}"

    def process_query(self, query_text):
        results = self.search_db(query_text)
        if results is None:
            return "Unable to find matching results."

        context_text = self.format_context(results)
        messages = f"Answer the question based only on the following context: {context_text}\nQuestion: {query_text}"

        response_text = ''.join([chunk for chunk in Model.call_api(messages)])

        sources = [doc.metadata.get("source", None) for doc, _score in results]
        formatted_response = self.format_output(response_text, sources)
        print("context:\n", context_text)
        print(formatted_response)
        return response_text
