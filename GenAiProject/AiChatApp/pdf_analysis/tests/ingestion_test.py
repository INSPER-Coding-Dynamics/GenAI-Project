import pytest
from unittest.mock import patch, MagicMock
from AiChatApp.pdf_analysis.ingestion import ingest_pdf

local_pdf_path = "./test_document.pdf"


@pytest.fixture
def mock_unstructured_loader():
    with patch('AiChatApp.pdf_analysis.ingestion.UnstructuredPDFLoader') as mock:
        yield mock


@pytest.fixture
def mock_online_loader():
    with patch('AiChatApp.pdf_analysis.ingestion.OnlinePDFLoader') as mock:
        yield mock


def test_ingest_pdf_local(mock_unstructured_loader):
    mock_loader = MagicMock()
    mock_unstructured_loader.return_value = mock_loader
    mock_loader.load.return_value = ['document1', 'document2']

    result = ingest_pdf('local', 'local_pdf_path')

    mock_unstructured_loader.assert_called_once_with('local_pdf_path')
    mock_loader.load.assert_called_once()
    assert result == ['document1', 'document2']


def test_ingest_pdf_online(mock_online_loader):
    mock_loader = MagicMock()
    mock_online_loader.return_value = mock_loader
    mock_loader.load.return_value = ['document3', 'document4']

    result = ingest_pdf(
        'online', 'https://s29.q4cdn.com/175625835/files/doc_downloads/test.pdf')

    mock_online_loader.assert_called_once_with(
        'https://s29.q4cdn.com/175625835/files/doc_downloads/test.pdf')
    mock_loader.load.assert_called_once()
    assert result == ['document3', 'document4']


def test_ingest_pdf_invalid_loader():
    with pytest.raises(ValueError, match="Invalid loader type"):
        ingest_pdf('invalid', 'local_pdf_path')
