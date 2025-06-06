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
        #return self.search_index(query, k)
        csv_data = """
as_of_date,order_created_year_quarter,primary_group,product_division_code,business_segment_code,account_name,nba_hier_level,nba_name,nba_child,threshold_value,threshold_deviation,nba_child_metrics_value,relative_benchmark_value,unit_of_measure,recommendation_type,ord_grp,company_region,company_sub_region
2025-02-01 13:48:43,Q1-2025,Life Sciences,-,-,ARSENAL BIOSCIENCES,primary_group,Improve Order Velocity,% of Orders on hold,0.1500,0.0038,0.1538,,%,Absolute,1,NA,-
2025-02-01 13:48:43,Q1-2025,Life Sciences,-,-,ARUP,primary_group,Improve Order Velocity,% of Orders on hold,0.1500,0.2406,0.3906,,%,Absolute,1,NA,-
2025-02-01 13:48:43,Q1-2025,Life Sciences,-,-,BIOGEN,primary_group,Improve Order Velocity,Average hold duration,10.0000,1.5600,11.5600,,days,Absolute,1,NA,-
2025-02-01 13:48:43,Q1-2025,Life Sciences,-,-,BMS,primary_group,Improve Order Velocity,% of Orders on hold,0.1500,0.3467,0.4967,,%,Absolute,1,NA,-
2025-02-01 13:48:43,Q1-2025,Life Sciences,-,-,CATALENT,primary_group,Improve Order Velocity,% of Orders on hold,0.1500,0.1912,0.3412,,%,Absolute,1,NA,-
2025-02-01 13:48:43,Q1-2025,Life Sciences,-,-,CEDARS SINAI,primary_group,Improve Order Velocity,% of Orders on hold,0.1500,0.2506,0.4006,,%,Absolute,1,NA,-
2025-02-01 13:48:43,Q1-2025,Life Sciences,-,-,CSL LTD,primary_group,Improve Order Velocity,% of Orders on hold,0.1500,0.0328,0.1828,,%,Absolute,1,NA,-
    """
        return csv_data.strip()
