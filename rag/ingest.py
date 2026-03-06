from langchain_community.document_loaders import DirectoryLoader, TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import AzureOpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from config.settings import settings

def build_vector_store():
    loader = DirectoryLoader(
        "docs",
        glob="**/*.txt",
        loader_cls=TextLoader
    )
    
    documents = loader.load()
    
    splitter = RecursiveCharacterTextSplitter(
        chunk_size = 800,
        chunk_overlap = 100
    )
    
    chunks = splitter.split_documents(documents)
    
    embeddings = AzureOpenAIEmbeddings(
        api_key=settings.azure_openai_api_key,
        azure_endpoint=settings.azure_openai_embedding_endpoint,
        azure_deployment= settings.azure_openai_embedding_deployment,
        api_version="2024-02-15-preview"    
    )
    
    vectorstore = FAISS.from_documents(chunks, embeddings)
    vectorstore.save_local("vector_store")
    