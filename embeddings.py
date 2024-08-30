from langchain_community.embeddings import HuggingFaceBgeEmbeddings

class Embeddings:
    MODEL_NAME = "BAAI/bge-large-en"
    DEVICE = 'cpu'

    @classmethod
    def get_embeddings(cls):
        model_kwargs = {'device': cls.DEVICE}
        encode_kwargs = {'normalize_embeddings': True}
        return HuggingFaceBgeEmbeddings(
            model_name=cls.MODEL_NAME,
            model_kwargs=model_kwargs,
            encode_kwargs=encode_kwargs
        )