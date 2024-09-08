from langchain.prompts import ChatPromptTemplate, PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_community.chat_models import ChatOllama
from langchain_core.runnables import RunnablePassthrough
from langchain.retrievers.multi_query import MultiQueryRetriever

QUERY_PROMPT = PromptTemplate(
    input_variables=["question"],
    template="""You are an AI language model assistant. Your task is to generate five
    different versions of the given user question to retrieve relevant documents from
    a vector database. By generating multiple perspectives on the user question, your
    goal is to help the user overcome some of the limitations of the distance-based
    similarity search. Provide these alternative questions separated by newlines.
    Original question: {question}
    """
)


def create_retriever(vector_store):
    """
    create a retriever for the given vector store

    args:
        vector_store (Chroma): vector store for the given text
    """
    # create a retriever
    retriever = MultiQueryRetriever.from_llm(
        vector_store.as_retriever(),
        llm=ChatOllama(model="nomic-embed-text"),
        prompt=QUERY_PROMPT
    )
    return retriever


def create_chain(retriever, llm):
    """
    create a chain for the given retriever and llm
    
    args:
        retriever (MultiQueryRetriever): retriever for the given text
        llm (ChatOllama): llm for the given text
    """
    # create a chain
    template = """Answer the question based only on the following context:
    {context}
    """
    prompt = ChatPromptTemplate.from_template(template)
    chain = (
        {"context": retriever, "question": RunnablePassthrough()}
        | prompt
        | llm
        | StrOutputParser()
    )
    return chain
    