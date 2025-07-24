from semantic_kernel.functions import kernel_function
from .base_vector_search_plugin import BaseVectorSearchPlugin

class InvoiceAgingPlugin(BaseVectorSearchPlugin):
    """Plugin to enable Azure AI Search invoice aging search capabilities."""

    def __init__(self):
        super().__init__("invoice-aging-index")

    @kernel_function(
        description="Invoice aging search Azure AI Search index for relevant information",
        name="invoice_aging_search",
    )
    def invoice_aging_search(self, query: str, k: int = 3) -> str:
        """Invoice aging search the Azure AI Search index for relevant information."""
        return self.search_index(query, k)


