from django.test import TestCase
import pytest
from unittest.mock import patch, MagicMock
from AiChatApp.pdf_analysis.ingestion import ingest_pdf

local_pdf_path = "./test_document.pdf"
online_pdf_path = "https://s29.q4cdn.com/175625835/files/doc_downloads/test.pdf"

class TestIngestion(TestCase):
    @patch('AiChatApp.pdf_analysis.ingestion.UnstructuredPDFLoader')
    def test_ingest_pdf_local(self, mock_unstructured_loader):
        mock_loader = MagicMock()
        mock_unstructured_loader.return_value = mock_loader
        mock_loader.load.return_value = ['document1', 'document2']

        result = ingest_pdf('local', local_pdf_path)

        mock_unstructured_loader.assert_called_once_with(local_pdf_path)
        mock_loader.load.assert_called_once()
        self.assertEqual(result, ['document1', 'document2'])

    @patch('AiChatApp.pdf_analysis.ingestion.OnlinePDFLoader')
    def test_ingest_pdf_online(self, mock_online_loader):
        mock_loader = MagicMock()
        mock_online_loader.return_value = mock_loader
        mock_loader.load.return_value = ['document3', 'document4']

        result = ingest_pdf('online', online_pdf_path)

        mock_online_loader.assert_called_once_with(online_pdf_path)
        mock_loader.load.assert_called_once()
        self.assertEqual(result, ['document3', 'document4'])

    def test_ingest_pdf_invalid_loader(self):
        with self.assertRaises(ValueError):
            ingest_pdf('invalid', local_pdf_path)
