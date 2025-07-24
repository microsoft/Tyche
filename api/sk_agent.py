import os
import logging
from semantic_kernel import Kernel
from semantic_kernel.agents import Agent, ChatCompletionAgent, SequentialOrchestration
from semantic_kernel.agents.runtime import InProcessRuntime
from semantic_kernel.connectors.ai.open_ai import AzureChatCompletion


from api.plugins.prioritization_logic_doc import prioritization_logic_doc
from api.plugins.improve_order_velocity_plugin import ImproveOrderVelocityPlugin
from .plugins.threshold_plugin import ThresholdPlugin
from .plugins.account_owner_plugin import AccountOwnerPlugin
from .plugins.email_plugin import EmailPlugin

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
                api_key=AZURE_OPENAI_KEY,
                deployment_name=AZURE_OPENAI_DEPLOYMENT,
                api_version="2025-01-01-preview",
                base_url=AZURE_OPENAI_ENDPOINT
            )
        )
        
    
        threshold_plugin_instance = ThresholdPlugin()
        # account_owner_plugin_instance = AccountOwnerPlugin()
        # improve_order_velocity_plugin_instance = ImproveOrderVelocityPlugin()
        # email_plugin_instance = EmailPlugin()
        kernel.add_plugin(threshold_plugin_instance, plugin_name="ThresholdPlugin")
        # kernel.add_plugin(account_owner_plugin_instance, plugin_name="AccountOwnerPlugin")
        # kernel.add_plugin(improve_order_velocity_plugin_instance, plugin_name="ImproveOrderVelocityPlugin")
        # kernel.add_plugin(email_plugin_instance, plugin_name="EmailPlugin")
      
        return ChatCompletionAgent(
            name=name,
            instructions=instructions,
            kernel=kernel,
            service=AzureChatCompletion(
                api_key=AZURE_OPENAI_KEY,
                deployment_name=AZURE_OPENAI_DEPLOYMENT,
                api_version="2025-01-01-preview",
                base_url=AZURE_OPENAI_ENDPOINT
            ),
        )

    def get_agents(self) -> list[Agent]:
        """Return a list of agents that will participate in the concurrent orchestration.
        """
        # data_lookup_agent = self.create_agent(
        #     name="data_lookup",            
        #     instructions=f"""
        #     The input will be a customer name, and then gather the data for next best action analysis. 
        #     ONLY consider the Improve Order Velocity next best action.
        #     Credit Holds and finance information should not be included in the analysis.

        #     Check all orders without a hold release timestamp.
        #     Include the following data in your analysis:
        #     - Order number
        #     - Order requested date
        #     - Order release date
        #     - Order status
        #     - Order hold codes
                              
                     

        #     Lets include SPECIFIC data from the plugins about the question. For each action item, cite the relevant plugin and include any specific data or values retrieved from the plugin.
            
        #     """
        # )

        prioritization_agent = self.create_agent(
            name="PrioritizationAgent",
            instructions=prioritization_logic_doc
        )
#         reviewer_agents = self.create_agent(
#             name="Reviewer",            
#             instructions=f"""
#             You are a Reviewer agent specializing in reviewing the Next Best Action (NBA) for customer.
            
#             RULES FOR IMPROVING ORDER VELOCITY:
#             {self.improve_order_velocity_rules}

#             The answer should be a todo list of action items that the customer care expert can take to improve order velocity.
#             Each action item should be specific, actionable, and directly address the customer's situation based on your analysis. 
#             Avoid general statements; provide concrete steps. 
#             Also provide SPECIFIC data from the plugins about the question. For each action item, cite the relevant plugin and include any specific data or values retrieved from the plugin that support your recommendation.
#             Not only return the action items, send an email to the customer care expert with the action items and any relevant data from the plugins.
#             The email should be formatted in HTML for readability.
            
#             Ensure each action item is tailored to the scenario and leverages available plugin data.

#             ###EXAMPLE OUTPUT:####
#             - Check SO number 12345 for C2 credit holds.
#             - Order number 98765 is still on hold but past order realease date with HOLD CODE:XYZ.  Connect with team to release hold.
# """)
        #return [data_lookup_agent]
        return [prioritization_agent]

    async def chat(self, user: str, message: str):
        agents = self.get_agents()
        sequential_orchestration = SequentialOrchestration(members=agents)

        runtime = InProcessRuntime()
        runtime.start()

        orchestration_result = await sequential_orchestration.invoke(
            task=message,
            runtime=runtime,
        )

        value = await orchestration_result.get()
        # results = []
        # for item in value:
        #     results.append({"agent": item.name, "answer": item.content})

        await runtime.stop_when_idle()
        return value


    improve_order_velocity_rules = """1. C2 CREDIT HOLDS: Improve Order Velocity
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
                    """