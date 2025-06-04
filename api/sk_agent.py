import os
import logging
from semantic_kernel import Kernel
from semantic_kernel.agents import Agent, ChatCompletionAgent, ConcurrentOrchestration
from semantic_kernel.agents.runtime import InProcessRuntime
from semantic_kernel.connectors.ai.open_ai import AzureChatCompletion
from .vector_search_plugin import VectorSearchPlugin

from dotenv import load_dotenv
load_dotenv()

# Configuration (use environment variables for security)
AZURE_OPENAI_ENDPOINT = os.getenv("AZURE_OPENAI_ENDPOINT")
AZURE_OPENAI_KEY = os.getenv("AZURE_OPENAI_KEY")
AZURE_OPENAI_DEPLOYMENT = os.getenv("AZURE_OPENAI_DEPLOYMENT")
AZURE_SEARCH_ENDPOINT = os.getenv("AZURE_SEARCH_ENDPOINT")
AZURE_SEARCH_KEY = os.getenv("AZURE_SEARCH_KEY")
AZURE_OPENAI_EMBEDDINGS_DEPLOYMENT = os.getenv("AZURE_OPENAI_EMBEDDINGS_DEPLOYMENT")
AZURE_OPENAI_EMBEDDINGS_ENDPOINT = os.getenv("AZURE_OPENAI_EMBEDDINGS_ENDPOINT")

# Logging setup
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


        

class SemanticKernelAgent:
    
    def create_agent(self, name: str, instructions: str, index_name: str = None) -> ChatCompletionAgent:
        """Create an agent with optional Azure AI Search capabilities."""
        
        # Create kernel for the agent
        kernel = Kernel()
        kernel.add_service(
            AzureChatCompletion(
                endpoint=AZURE_OPENAI_ENDPOINT,
                api_key=AZURE_OPENAI_KEY,
                deployment_name=AZURE_OPENAI_DEPLOYMENT
            )
        )
        
        if (index_name is not None and index_name != ""):
        # Add Azure AI Search plugin if index_name is provided  
            search_plugin = VectorSearchPlugin(
                search_endpoint=AZURE_SEARCH_ENDPOINT,
                search_key=AZURE_SEARCH_KEY,
                index_name=index_name
            )
            kernel.add_plugin(search_plugin, plugin_name="VectorSearchPlugin")
        
               
        return ChatCompletionAgent(
            name=name,
            instructions=instructions,
            kernel=kernel,
            service=AzureChatCompletion(
                endpoint=AZURE_OPENAI_ENDPOINT,
                api_key=AZURE_OPENAI_KEY,
                deployment_name=AZURE_OPENAI_DEPLOYMENT
            ),
        )

    def get_agents(self) -> list[Agent]:
        """Return a list of agents that will participate in the concurrent orchestration.

        Feel free to add or remove agents.
        """
        # Account Owner agent with search capabilities using the main search index
        account_owner_agent = self.create_agent(
            name="AccountOwner",
            instructions="You manage the relationship between an employee account owner and a customer.  Answer only questions from the knowledge base.",
            #index_name="azureblob-index"
            index_name="account-owner"              
        )

        # # Chemistry agent without search (regular agent)
        # chemistry_agent = self.create_agent(
        #     name="ChemistryExpert",
        #     instructions="You are an expert in chemistry. You answer questions from a chemistry perspective.",
        #     index_name=None  # This agent won't have search capabilities
        # )
        
        return [account_owner_agent]#, chemistry_agent]

    async def chat(self, user: str, message: str):
        agents = self.get_agents()
        concurrent_orchestration = ConcurrentOrchestration(members=agents)

        # 2. Create a runtime and start it
        runtime = InProcessRuntime()
        runtime.start()

        # 3. Invoke the orchestration with a task and the runtime
        orchestration_result = await concurrent_orchestration.invoke(
            task=message,
            runtime=runtime,
        )

        # 4. Wait for the results
        # Note: the order of the results is not guaranteed to be the same
        # as the order of the agents in the orchestration.
        value = await orchestration_result.get(timeout=20)
        results = []
        for item in value:
            results.append({"agent": item.name, "answer": item.content})

        # 5. Stop the runtime after the invocation is complete
        await runtime.stop_when_idle()
        return results
