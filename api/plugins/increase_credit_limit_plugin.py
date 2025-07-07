import os
import logging
import requests
from semantic_kernel.functions import kernel_function
from azure.search.documents import SearchClient
from azure.core.credentials import AzureKeyCredential
from azure.search.documents.models import VectorizableTextQuery

# Set up logger
target_logger = logging.getLogger(__name__)

# Environment variables for embeddings
AZURE_OPENAI_ENDPOINT = os.getenv("AZURE_OPENAI_ENDPOINT")
AZURE_OPENAI_KEY = os.getenv("AZURE_OPENAI_EMBEDDINGS_KEY")
AZURE_OPENAI_EMBEDDINGS_DEPLOYMENT = os.getenv("AZURE_OPENAI_EMBEDDINGS_DEPLOYMENT")
AZURE_OPENAI_EMBEDDINGS_ENDPOINT = os.getenv("AZURE_OPENAI_EMBEDDINGS_ENDPOINT")

class IncreaseCreditLimitPlugin:
    """Plugin to enable Azure AI Search to find relevant information about increasing credit limits."""

    def __init__(self, search_endpoint: str, search_key: str):
        self.search_client = SearchClient(
            endpoint=search_endpoint,
            index_name="increase-credit-limit",
            credential=AzureKeyCredential(search_key)
        )

    def get_aoai_embedding(self, text: str) -> list:
        """Get embedding from Azure OpenAI embeddings deployment."""
        endpoint = AZURE_OPENAI_EMBEDDINGS_ENDPOINT
        key = AZURE_OPENAI_KEY
        headers = {"Content-Type": "application/json", "api-key": key}
        data = {"input": text}

        response = requests.post(endpoint, headers=headers, json=data)
        response.raise_for_status()
        return response.json()["data"][0]["embedding"]

    @kernel_function(
        description="Use Azure AI Search to find relevant information about increasing credit limits.",
        name="increase_credit_limit_search",
    )
    def increase_credit_limit_search(self, query: str, k: int = 3) -> str:
        """Increase credit limit search the Azure AI Search index for relevant information."""
        embedding = self.get_aoai_embedding(query)

        vector_queries = [VectorizableTextQuery(text=query, k_nearest_neighbors=k, fields="text_vector")]
        results = self.search_client.search(
            search_text=None,
            vector_queries=vector_queries,
            top=k
        )
        contexts = []
        for doc in results:
            content = doc.get("content") or doc.get("text") or str(doc)
            contexts.append(f"Document: {content}")
        return "\n\n".join(contexts) if contexts else "No results found"
