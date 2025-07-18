import os
import logging
import requests
from azure.search.documents import SearchClient
from azure.core.credentials import AzureKeyCredential
from azure.search.documents.models import VectorizableTextQuery

# Set up logger
target_logger = logging.getLogger(__name__)

# Environment variables for embeddings
AZURE_OPENAI_KEY = os.getenv("AZURE_OPENAI_KEY")
AZURE_OPENAI_EMBEDDINGS_DEPLOYMENT = os.getenv("AZURE_OPENAI_EMBEDDINGS_DEPLOYMENT")
AZURE_OPENAI_EMBEDDINGS_ENDPOINT = os.getenv("AZURE_OPENAI_EMBEDDINGS_ENDPOINT")
AZURE_SEARCH_ENDPOINT = os.getenv("AZURE_SEARCH_ENDPOINT")
AZURE_SEARCH_KEY = os.getenv("AZURE_SEARCH_KEY")


class BaseVectorSearchPlugin:
    """Base plugin class for Azure AI Search capabilities."""

    def __init__(self, index_name: str):
        self.search_client = SearchClient(
            endpoint=AZURE_SEARCH_ENDPOINT,
            index_name=index_name,
            credential=AzureKeyCredential(AZURE_SEARCH_KEY)
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

    def search_index(self, query: str, k: int = 3) -> str:
        """Search the Azure AI Search index for relevant information."""
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
