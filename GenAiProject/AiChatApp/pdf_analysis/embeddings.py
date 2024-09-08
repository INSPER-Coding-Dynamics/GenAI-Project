from langchain_community.embeddings import OllamaEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma


def create_embeddings(text):
    """
    create embeddings for the parsed text from the pdf

    args:
        text (str): parsed text from the pdf

    returns:
        vector_store (Chroma): vector store for the given text
    """
    # split and create chunks
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=7500, chunk_overlap=100)
    chunks = text_splitter.split_text(text)

    # create embeddings
    embeddings = OllamaEmbeddings(model="nomic-embed-text")

    # create vector store
    vector_store = Chroma.from_documents(
        chunks, embeddings=embeddings, persist_directory="db", collection_name="pdf_analysis")

    return vector_store
