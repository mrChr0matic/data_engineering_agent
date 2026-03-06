from langchain_openai import AzureChatOpenAI
from config.settings import settings

def get_llm():
    '''
    Initialize Azure OpenAI GPT model.
    '''
    llm = AzureChatOpenAI(
        api_key=settings.azure_openai_api_key,
        azure_endpoint=settings.azure_openai_endpoint,
        deployment_name=settings.azure_openai_deployment,
        api_version=settings.azure_openai_api_version,
        temperature=0
    )

    return llm