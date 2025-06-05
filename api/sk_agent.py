import os
import logging
from semantic_kernel import Kernel
from semantic_kernel.agents import Agent, ChatCompletionAgent, ConcurrentOrchestration
from semantic_kernel.agents.runtime import InProcessRuntime
from semantic_kernel.connectors.ai.open_ai import AzureChatCompletion
from .plugins.threshold_plugin import ThresholdPlugin
from .plugins.account_owner_plugin import AccountOwnerPlugin

from dotenv import load_dotenv
load_dotenv()

# Configuration (use environment variables for security)
AZURE_OPENAI_ENDPOINT = os.getenv("AZURE_OPENAI_ENDPOINT")
AZURE_OPENAI_KEY = os.getenv("AZURE_OPENAI_KEY")
AZURE_OPENAI_DEPLOYMENT = os.getenv("AZURE_OPENAI_DEPLOYMENT")
AZURE_SEARCH_ENDPOINT = os.getenv("AZURE_SEARCH_ENDPOINT")
AZURE_SEARCH_KEY = os.getenv("AZURE_SEARCH_KEY")

# Logging setup
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


        

class SemanticKernelAgent:
    
    def create_agent(self, name: str, instructions: str) -> ChatCompletionAgent:
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
        
    
        threshold_plugin_instance = ThresholdPlugin(search_endpoint=AZURE_SEARCH_ENDPOINT,search_key=AZURE_SEARCH_KEY)
        account_owner_plugin_instance = AccountOwnerPlugin(search_endpoint=AZURE_SEARCH_ENDPOINT,search_key=AZURE_SEARCH_KEY)
        kernel.add_plugin(threshold_plugin_instance, plugin_name="ThresholdPlugin")
        kernel.add_plugin(account_owner_plugin_instance, plugin_name="AccountOwnerPlugin")

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
        """
        action_review_agent = self.create_agent(
            name="ActionReview",
            instructions="""
            You are an analyst specializing in determining the Next Best Action (NBA) for customers using the threshold plugin.
            Analyze the provided data and recommend the most appropriate next steps for the customer.
            Your answer must be concise, actionable, and formatted as a bulleted list.
            Only use information from the knowledge base and threshold plugin to support your answer.
            There may be more than one possible action in the query, so provide all relevant answers.
            ###Example###
            User: What is the next best action for the customer and who is the owner?
            - Offer a discount on their next purchase
            - Increase Credit Limit to 50,000
            - Account Owner: Bob Smith""",
        )
        # account_owner_agent = self.create_agent(
        #     name="AccountOwner",
        #     instructions="You manage the relationship between an employee account owner and a customer.  Answer only questions from the knowledge base.",
        #     index_name="account-owner"              
        # )

        
        # threshold_agent = self.create_agent(
        #     name="Threshold",
        #     instructions="You are and analyst that will examine the data to determine the next best action for the customer.  Answer only questions from the knowledge base.",
        #     index_name="threshold"
        # )

        return [action_review_agent]

    async def chat(self, user: str, message: str):
        agents = self.get_agents()
        concurrent_orchestration = ConcurrentOrchestration(members=agents)

        runtime = InProcessRuntime()
        runtime.start()

        orchestration_result = await concurrent_orchestration.invoke(
            task=message,
            runtime=runtime,
        )

        value = await orchestration_result.get(timeout=20)
        results = []
        for item in value:
            results.append({"agent": item.name, "answer": item.content})

        await runtime.stop_when_idle()
        return results
