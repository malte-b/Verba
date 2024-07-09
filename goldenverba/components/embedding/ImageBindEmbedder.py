from goldenverba.components.embedding.SentenceTransformersEmbedder import (
    SentenceTransformersEmbedder,
)


class ImageBindEmbedder(SentenceTransformersEmbedder):
    """
    ImageBindEmbedder for Verba.
    """ 

    def __init__(self):
        super().__init__(vectorizer="nielsr/imagebind-huge")
       