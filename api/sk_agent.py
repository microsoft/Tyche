import os
import logging
from semantic_kernel import Kernel
from semantic_kernel.agents import Agent, ChatCompletionAgent, ConcurrentOrchestration
from semantic_kernel.agents.runtime import InProcessRuntime
from semantic_kernel.connectors.ai.open_ai import AzureChatCompletion

from api.plugins.improve_order_velocity_plugin import ImproveOrderVelocityPlugin
from api.plugins.increase_credit_limit_plugin import IncreaseCreditLimitPlugin
from api.plugins.invoice_aging_plugin import InvoiceAgingPlugin
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
        # increase_credit_limit_plugin_instance = IncreaseCreditLimitPlugin(search_endpoint=AZURE_SEARCH_ENDPOINT,search_key=AZURE_SEARCH_KEY)
        # invoice_aging_plugin_instance = InvoiceAgingPlugin(search_endpoint=AZURE_SEARCH_ENDPOINT,search_key=AZURE_SEARCH_KEY)
        account_owner_plugin_instance = AccountOwnerPlugin()
        improve_order_velocity_plugin_instance = ImproveOrderVelocityPlugin()
        kernel.add_plugin(threshold_plugin_instance, plugin_name="ThresholdPlugin")
        kernel.add_plugin(account_owner_plugin_instance, plugin_name="AccountOwnerPlugin")
        kernel.add_plugin(improve_order_velocity_plugin_instance, plugin_name="ImproveOrderVelocityPlugin")
        # kernel.add_plugin(increase_credit_limit_plugin_instance, plugin_name="IncreaseCreditLimitPlugin")
        # kernel.add_plugin(invoice_aging_plugin_instance, plugin_name="InvoiceAgingPlugin")

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

            ROLE AND RESPONSIBILITIES:
            - Analyze the provided data and recommend the most appropriate next steps for the customer
            - Only use information from the knowledge base and threshold plugin to support your answer
            - There may be more than one possible answer to the query, so provide all relevant data
            - If the question is about the account owner, use the account owner plugin to get data
            - If the question is about improving order velocity, use the improve order velocity plugin to get data

            RULES FOR IMPROVING ORDER VELOCITY:

            1. C2 CREDIT HOLDS: Improve Order Velocity
            a. If a C2 hold has not been released, reach out to Credit Team for support releasing the hold or next steps required
            b. Identify the bill-to account numbers placed on credit hold
            c. Review the bill-to accounts placed on credit hold: do any accounts have negative available credit limit?
                i. If yes, review the account's open AR and past due AR
                ii. Do the accounts with credit holds have significant past due AR?
                    1. If yes, reach out to Collections Team for update on status of account
                    2. If no, reach out to Credit Team and request credit limit realignment
            d. Note: it is important to review credit holds even if all holds are released, there is still opportunity for action

            2. RR (REVENUE RECOGNITION) HOLDS: Improve Order Velocity
            a. Has the RR hold been released?
                i. If yes, then check:
                    1. Has the order been shipped?
                    2. If the order has not been shipped, when is the order release date?
                    3. If the order release date is in the past, use E1 to check TN for update on order then reach out to appropriate internal team for update/action
                ii. If no, then check:
                    1. Is the order requested date well in the future?
                    2. Are there any additional holds on the order? Can any actions be taken on other hold codes?
                    3. If the order requested date is not in the future, need to reach out to Finance for status update/action plan

            3. LENGTHY HOLD DURATIONS (i.e. CF, PM, S2, etc Holds): Improve Order Velocity
            a. Has the hold been released?
                i. If yes:
                    1. Has the order shipped? If yes, no action
                    2. Is the order release date in the past? If yes, check order in E1 for updates and reach out to appropriate internal team for update/action
                    3. If order release date in future, monitor to ensure order releases and ships as expected
                ii. If no:
                    1. When is the order release date?
                        a. If in the future, no action
                    2. If in the past, check order in E1 for updates and reach out to appropriate internal team for update/action

            ### EXAMPLE OUTPUT FORMAT ###
            User: What is the next best action for the customer and who is the owner?
            Response:
            - Offer a discount on their next purchase
            - Increase Credit Limit to 50,000
            - Account Owner: Bob Smith
            """
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
