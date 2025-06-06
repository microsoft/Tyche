import os
import logging
from semantic_kernel import Kernel
from semantic_kernel.agents import Agent, ChatCompletionAgent, HandoffOrchestration, OrchestrationHandoffs
from semantic_kernel.agents.runtime import InProcessRuntime
from semantic_kernel.connectors.ai.open_ai import AzureChatCompletion
from semantic_kernel.contents import ChatMessageContent

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

    def create_agent(self, name: str, instructions: str, description: str, plugins: list[object]) -> ChatCompletionAgent:
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
        
    
        #threshold_plugin_instance = ThresholdPlugin(search_endpoint=AZURE_SEARCH_ENDPOINT,search_key=AZURE_SEARCH_KEY)
        # increase_credit_limit_plugin_instance = IncreaseCreditLimitPlugin(search_endpoint=AZURE_SEARCH_ENDPOINT,search_key=AZURE_SEARCH_KEY)
        # invoice_aging_plugin_instance = InvoiceAgingPlugin(search_endpoint=AZURE_SEARCH_ENDPOINT,search_key=AZURE_SEARCH_KEY)
        # account_owner_plugin_instance = AccountOwnerPlugin()
        # improve_order_velocity_plugin_instance = ImproveOrderVelocityPlugin()
        # kernel.add_plugin(threshold_plugin_instance, plugin_name="ThresholdPlugin")
        # kernel.add_plugin(account_owner_plugin_instance, plugin_name="AccountOwnerPlugin")
        # kernel.add_plugin(improve_order_velocity_plugin_instance, plugin_name="ImproveOrderVelocityPlugin")
        # kernel.add_plugin(increase_credit_limit_plugin_instance, plugin_name="IncreaseCreditLimitPlugin")
        # kernel.add_plugin(invoice_aging_plugin_instance, plugin_name="InvoiceAgingPlugin")

        return ChatCompletionAgent(
            name=name,
            instructions=instructions,
            description=description,
            kernel=kernel,
            service=AzureChatCompletion(
                endpoint=AZURE_OPENAI_ENDPOINT,
                api_key=AZURE_OPENAI_KEY,
                deployment_name=AZURE_OPENAI_DEPLOYMENT
            ),
            plugins=plugins
        )

    def get_agents(self) -> tuple[list[Agent], OrchestrationHandoffs]:
        """Return a list of agents that will participate in the Handoff orchestration and the handoff relationships.
        """
        orchestrator_agent = self.create_agent(
            name="OrchestratorAgent",
            description="Main orchestrator agent. Triages user requests and hands off to the appropriate specialized agent for resolution.",
            instructions="""
            You are the main orchestrator. Your job is to analyze the user's request, determine which specialized agent is best suited to handle it, and hand off the task. 
            If a request requires multiple steps, coordinate the handoff between agents as needed. 
            Do not attempt to solve specialized tasks yourself—always delegate to the appropriate agent.
            """,
            plugins=[]
        )



        threshold_review_agent = self.create_agent(
            name="ThresholdReview", 
            description="Agent that reviews the threshold for the next best action and determines the account owner.",           
            instructions="""
            You are an analyst specializing in determining the Next Best Action (NBA) for customers using the threshold plugin.
            You also have access to the AccountOwnerPlugin to determine the account owner.
            ### EXAMPLE OUTPUT FORMAT ###
            User: What is the next best action for the customer and who is the owner?
            Response:
            - Offer a discount on their next purchase
            - Increase Credit Limit to 50,000
            - Account Owner: Bob Smith
            """,
            plugins=[ThresholdPlugin(), AccountOwnerPlugin()]
        )


        order_velocity_agent = self.create_agent(
            name="OrderVelocity",
            description="Agent that improves order velocity for customers by analyzing order holds and taking appropriate actions.",
            instructions="""
            You are an expert in improving order velocity for customers. Use the ImproveOrderVelocityPlugin to analyze the data and provide recommendations.
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
            """,
            plugins=[ImproveOrderVelocityPlugin()]
        )

        
        # Define the handoff relationships between agents
        handoffs = (
            OrchestrationHandoffs()
            .add_many(
                source_agent=orchestrator_agent.name,
                target_agents={
                    threshold_review_agent.name: "Transfer to this agent first to determine the next best action or determine the account owner",
                    order_velocity_agent.name: "Transfer to this agent if they need to Improve Order Velocity",
                },
            )
            .add(
                source_agent=order_velocity_agent.name,
                target_agent=orchestrator_agent.name,
                description="Transfer to the orchestrator agent if the order velocity issue is resolved or requires further action.",
            )     
            .add(
                source_agent=threshold_review_agent.name,
                target_agent=orchestrator_agent.name,
                description="Transfer to the orchestrator agent if the NBA is determined, account owner is identified, or further action is required.",
            )
        )

        return [orchestrator_agent, order_velocity_agent, threshold_review_agent], handoffs

    def agent_response_callback(self, message: ChatMessageContent) -> None:
        """Observer function to print the messages from the agents."""
        print(f"{message.name}: {message.content}")

    async def chat(self, user: str, message: str):
        agents, handoffs = self.get_agents()
        handoff_orchestration = HandoffOrchestration(
            members=agents,
            handoffs=handoffs,
            agent_response_callback=self.agent_response_callback,
            # human_response_function=human_response_function,
        )

        runtime = InProcessRuntime()
        runtime.start()

        orchestration_result = await handoff_orchestration.invoke(
            task=message,
            runtime=runtime,
        )

        value = await orchestration_result.get()
        # results = []
        # for item in value:
        #     results.append({"agent": item.name, "answer": item.content})

        await runtime.stop_when_idle()
        return value
