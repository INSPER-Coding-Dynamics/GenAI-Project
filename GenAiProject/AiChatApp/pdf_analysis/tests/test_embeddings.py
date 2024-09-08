from django.test import TestCase
from unittest.mock import patch, MagicMock
from AiChatApp.pdf_analysis.embeddings import create_embeddings


class CreateEmbeddingsTestCase(TestCase):
    @patch('AiChatApp.pdf_analysis.embeddings.Chroma')
    @patch('AiChatApp.pdf_analysis.embeddings.OllamaEmbeddings')
    @patch('AiChatApp.pdf_analysis.embeddings.RecursiveCharacterTextSplitter')
    def test_create_embeddings(self, MockTextSplitter, MockOllamaEmbeddings, MockChroma):
        # mock the text splitter
        mock_text_splitter_instance = MockTextSplitter.return_value
        mock_text_splitter_instance.split_text.return_value = [
            'chunk1', 'chunk2']

        # mock the embeddings
        mock_embeddings_instance = MockOllamaEmbeddings.return_value

        # mock the vector store
        mock_from_documents_instance = MagicMock()
        MockChroma.from_documents.return_value = mock_from_documents_instance

        # call the embeddings function
        text = "i'm a sample text from a PDF"
        result = create_embeddings(text)

        # assertions
        MockTextSplitter.assert_called_once_with(
            chunk_size=7500, chunk_overlap=100)
        mock_text_splitter_instance.split_text.assert_called_once_with(text)
        MockOllamaEmbeddings.assert_called_once_with(model="nomic-embed-text")
        MockChroma.from_documents.assert_called_once_with(
            ['chunk1', 'chunk2'], embeddings=mock_embeddings_instance, persist_directory="db", collection_name="pdf_analysis"
        )
        self.assertIs(result, mock_from_documents_instance)
