import os
import logging
from semantic_kernel import Kernel
from semantic_kernel.agents import Agent, ChatCompletionAgent, SequentialOrchestration
from semantic_kernel.agents.runtime import InProcessRuntime
from semantic_kernel.connectors.ai.open_ai import AzureChatCompletion
from semantic_kernel.contents import ChatMessageContent

from .plugins.improve_order_velocity_plugin import ImproveOrderVelocityPlugin
from .plugins.threshold_plugin import ThresholdPlugin

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
    
    def get_agents(self) -> list[Agent]:
        """Return a list of agents that will participate in the concurrent orchestration.
        """
        threshold_review_agent = ChatCompletionAgent(
            name="ThresholdReview", 
            description="Agent that reviews the threshold for the next best action and determines the account owner.",           
            instructions="""
            You are an analyst specializing in determining the Next Best Action (NBA) for customers using the threshold plugin.
            ### EXAMPLE OUTPUT FORMAT ###
            User: What is the next best action for the customer and who is the owner?
            Response:
            - Offer a discount on their next purchase
            - Increase Credit Limit to 50,000
            """,
            service=AzureChatCompletion(
                endpoint=AZURE_OPENAI_ENDPOINT,
                api_key=AZURE_OPENAI_KEY,
                deployment_name=AZURE_OPENAI_DEPLOYMENT
            ),
            plugins=[ThresholdPlugin()]
        )

        order_velocity_agent = ChatCompletionAgent(
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
            service=AzureChatCompletion(
                endpoint=AZURE_OPENAI_ENDPOINT,
                api_key=AZURE_OPENAI_KEY,
                deployment_name=AZURE_OPENAI_DEPLOYMENT
            ),
            plugins=[ImproveOrderVelocityPlugin()]
        )
        final_answer_agent = ChatCompletionAgent(
            name="FinalAnswerAgent",
            description="An agent that provides the final answer with no additional questions or comments.",
            instructions="Provide the final answer to the user without any additional questions or comments.",
            service=AzureChatCompletion(
                endpoint=AZURE_OPENAI_ENDPOINT,
                api_key=AZURE_OPENAI_KEY,
                deployment_name=AZURE_OPENAI_DEPLOYMENT
            ),
            plugins=[] 
        )

        return [threshold_review_agent, order_velocity_agent, final_answer_agent]

    def agent_response_callback(self, message: ChatMessageContent) -> None:
        """Observer function to print the messages from the agents."""
        print(f"# {message.name}\n{message.content}")

    async def chat(self, user: str, message: str):
        agents = self.get_agents()
        sequential_orchestration = SequentialOrchestration(
            members=agents,
            agent_response_callback=self.agent_response_callback,
            )

        runtime = InProcessRuntime()
        runtime.start()

        orchestration_result = await sequential_orchestration.invoke(
            task=message,
            runtime=runtime,
        )

        value = await orchestration_result.get(timeout=20)
        # results = []
        # for item in value:
        #     results.append({"agent": item.name, "answer": item.content})

        await runtime.stop_when_idle()
        return value
