from langchain_community.document_loaders import UnstructuredPDFLoader
from langchain_community.document_loaders import OnlinePDFLoader


def ingest_pdf(loader_type, file_path):
    """
    ingest a PDF file based on the specified loader type.

    args:
        loader_type (str): the type of loader to use ('local' or 'online').
        file_path (str): the path to the PDF file.

    raises:
        ValueError: if the loader type is invalid.

    returns:
        List[Document]: a list of Document objects.
    """
    if loader_type == 'local':
        loader = UnstructuredPDFLoader(file_path)
    elif loader_type == 'online':
        loader = OnlinePDFLoader(file_path)
    else:
        raise ValueError("Invalid loader type")

    return loader.load()
