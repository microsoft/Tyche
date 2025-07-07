from semantic_kernel.functions import kernel_function
from .base_vector_search_plugin import BaseVectorSearchPlugin
import os

class ImproveOrderVelocityPlugin(BaseVectorSearchPlugin):
    """Plugin to enable Azure AI Search improve order velocity search capabilities."""

    def __init__(self):
        IMPROVE_ORDER_VELOCITY_INDEX_NAME = os.getenv("IMPROVE_ORDER_VELOCITY_INDEX_NAME")
        super().__init__(IMPROVE_ORDER_VELOCITY_INDEX_NAME)

    @kernel_function(
        description="Improve order velocity search Azure AI Search index for relevant information",
        name="improve_order_velocity_search",
    )
    def improve_order_velocity_search(self, query: str, k: int = 3) -> str:
        """Improve order velocity search the Azure AI Search index for relevant information."""
        return self.search_index(query, k)


