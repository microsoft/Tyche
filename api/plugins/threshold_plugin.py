from semantic_kernel.functions import kernel_function
from .base_vector_search_plugin import BaseVectorSearchPlugin

class ThresholdPlugin(BaseVectorSearchPlugin):
    """Plugin to enable Azure AI Search threshold search capabilities."""

    def __init__(self):
        super().__init__("threshold")

    @kernel_function(
        description="Threshold search Azure AI Search index for relevant information",
        name="threshold_search",
    )
    def threshold_search(self, query: str, k: int = 3) -> str:
        """Vector search the Azure AI Search index for relevant information."""
        return self.search_index(query, k)
