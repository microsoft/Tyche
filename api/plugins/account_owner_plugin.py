from semantic_kernel.functions import kernel_function
from .base_vector_search_plugin import BaseVectorSearchPlugin

class AccountOwnerPlugin(BaseVectorSearchPlugin):
    """Plugin to enable Azure AI Search account owner search capabilities."""

    def __init__(self):
        super().__init__("account-owner")

    @kernel_function(
        description="Account owner search Azure AI Search index for relevant information",
        name="account_owner_search",
    )
    def account_owner_search(self, query: str, k: int = 3) -> str:
        """Account owner search the Azure AI Search index for relevant information."""
        return self.search_index(query, k)
