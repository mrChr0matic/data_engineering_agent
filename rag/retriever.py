from langchain_openai import AzureOpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from config.settings import settings

def get_retriever():
    embeddings = AzureOpenAIEmbeddings(
        api_key=settings.azure_openai_api_key,
        azure_endpoint=settings.azure_openai_embedding_endpoint,
        azure_deployment = settings.azure_openai_embedding_deployment,
        api_version="2024-12-01-preview"
    )
    
    vectorstore = FAISS.load_local(
        "vector_store",
        embeddings,
        allow_dangerous_deserialization=True
    )
    
    return vectorstore.as_retriever(search_kwargs={"k" : 7})