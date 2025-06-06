from semantic_kernel.functions import kernel_function
from .base_vector_search_plugin import BaseVectorSearchPlugin

class AccountOwnerPlugin(BaseVectorSearchPlugin):
    """Plugin to enable Azure AI Search account owner search capabilities."""

    def __init__(self):
        super().__init__("account-owner")

    @kernel_function(
        description="Return the full account owner CSV data as a string.",
        name="account_owner_csv",
    )
    def account_owner_csv(self) -> str:
        """Return the full account owner CSV data as a string."""
        csv_data = """account_name,Owner
                2SEVENTY BIO,Katherine
                ABBOTT,Stephanie
                ABBVIE,Stephanie
                ABBVIE BIOTECHNOLOGY LTD,Stephanie
                AMGEN,Katherine
                ARSENAL BIOSCIENCES,Melissa
                ARUP,Shannen
                ASTELLAS PHARMA,
                ASTRAZENECA,Stephanie
                BAYER,Shannen
                BE BIOPHARMA,Melissa
                BI,Stephanie
                BIOGEN,Stephanie
                BIONTECH,Stephanie
                BLUEROCK THERAPEUTICS,Shannen
                BMS,Katherine
                BRISTOL MYERS SQUIBB CO,Katherine
                CATALENT,Stephanie
                CATALENT ANAGNI SRL,Stephanie
                CATALENT GOSSELIES PS SA,Stephanie
                CATALENT INC,Stephanie
                CDC,Katherine
                CEDARS SINAI,Melissa
                CHARLES RIVER LABS,Shannen
                CORNELL UNIV,
                CORTEVA,Melissa
                CSL LTD,Shannen
                CUREVAC,Shannen
                DECIBEL THERAPEUTICS,Katherine
                DIASORIN,Katherine
                ELI LILLY,Shannen
                EUROFINS,Stephanie
                FUJIFILM,Stephanie
                GARUDA THERAPEUTICS,Katherine
                GILEAD KITE,
                GILEAD/KITE,Katherine
                GSK,Stephanie
                HARVARD UNIV,Melissa
                HEALTHTRACKRX,Melissa
                J&J,Shannen
                JOHNS HOPKINS UNIV,Melissa
                JOHNSON & JOHNSON SERVICES INC,Shannen
                KAISER PERMANENTE,Melissa
                KRYSTAL BIOTECH,Katherine
                LAB CORP,Shannen
                LAB CORP OF AMERICA,Shannen
                LARONDE,Katherine
                LONZA,Katherine
                MAKO MEDICAL LABS,Melissa
                MAYO CLINIC,Shannen
                MEMORIAL SLOAN KETTERING,Katherine
                MERCK,Stephanie
                MERCK KGAA,Stephanie
                MODERNA,Shannen
                NATIONAL RESILIENCE,Stephanie
                NOVARTIS,Stephanie
                NOVO NORDISK,Katherine
                OPKO HEALTH,Melissa
                PFIZER,Stephanie
                QUEST DIAGNOSTICS,Shannen
                REGENERON,Katherine
                REPLIGEN,Shannen
                RING THERAPEUTICS,Melissa
                ROCHE,Katherine
                SAIL BIOMEDICINES,Katherine
                SANA BIOTECHNOLOGY,Melissa
                SANOFI,Katherine
                SAREPTA THERAPEUTICS,Katherine
                SATELLITE BIO,Melissa
                ST JUDE,Shannen
                STANFORD UNIV,
                TAKEDA PHARMACEUTICALS,Shannen
                TESSERA THERAPEUTICS,Katherine
                TOME BIOSCIENCES,Shannen
                UNIV OF CALIFORNIA SYSTEM,Melissa
                UNIV OF NORTH CAROLINA SYSTEM,
                UNIV OF PENNSYLVANIA,Melissa
                VERTEX PHARMACEUTICALS,Stephanie
                VERVE THERAPEUTICS,Melissa
                WASHINGTON UNIV IN ST LOUIS,Melissa
                WUXI,Katherine
                ZOETIS,Stephanie
                """
        return csv_data
