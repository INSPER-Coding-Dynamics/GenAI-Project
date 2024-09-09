from django.test import TestCase
from unittest.mock import patch, MagicMock
from AiChatApp.pdf_analysis.retrieval import create_retriever, create_chain, QUERY_PROMPT


class RetrievalTestCase(TestCase):

    @patch('AiChatApp.pdf_analysis.retrieval.MultiQueryRetriever')
    @patch('AiChatApp.pdf_analysis.retrieval.ChatOllama')
    def test_create_retriever(self, MockChatOllama, MockMultiQueryRetriever):
        # mock the vector store
        mock_vector_store = MagicMock()
        mock_vector_store.as_retriever.return_value = MagicMock()

        # mock the ChatOllama instance
        mock_chat_ollama = MockChatOllama.return_value

        # mock the MultiQueryRetriever
        mock_retriever = MagicMock()
        MockMultiQueryRetriever.from_llm.return_value = mock_retriever

        # call the function
        result = create_retriever(mock_vector_store)

        # assertions
        mock_vector_store.as_retriever.assert_called_once()
        MockChatOllama.assert_called_once_with(model="nomic-embed-text")
        MockMultiQueryRetriever.from_llm.assert_called_once_with(
            mock_vector_store.as_retriever.return_value,
            llm=mock_chat_ollama,
            prompt=QUERY_PROMPT
        )
        self.assertEqual(result, mock_retriever)

    @patch('AiChatApp.pdf_analysis.retrieval.ChatPromptTemplate')
    @patch('AiChatApp.pdf_analysis.retrieval.RunnablePassthrough')
    @patch('AiChatApp.pdf_analysis.retrieval.StrOutputParser')
    def test_create_chain(self, MockStrOutputParser, MockRunnablePassthrough, MockChatPromptTemplate):
        # mock the retriever and llm
        mock_retriever = MagicMock()
        mock_llm = MagicMock()

        # mock ChatPromptTemplate
        mock_prompt = MagicMock()
        MockChatPromptTemplate.from_template.return_value = mock_prompt

        # mock RunnablePassthrough
        mock_runnable_passthrough = MagicMock()
        MockRunnablePassthrough.return_value = mock_runnable_passthrough

        # mock StrOutputParser
        mock_str_output_parser = MagicMock()
        MockStrOutputParser.return_value = mock_str_output_parser

        # call the function
        result = create_chain(mock_retriever, mock_llm)

        # assertions
        MockChatPromptTemplate.from_template.assert_called_once_with(
            "answer the question based only on the following context:\n    {context}\n    "
        )
        MockRunnablePassthrough.assert_called_once()
        MockStrOutputParser.assert_called_once()

        # check if the chain is constructed correctly
        # the result should be a mock object representing the chain
        self.assertIsInstance(result, MagicMock)
        # note: we can't easily test the structure of the chain
        # but we can ensure that all components are correctly used
