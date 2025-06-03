import os
import logging
from semantic_kernel import Kernel
from semantic_kernel.agents import Agent, ChatCompletionAgent, ConcurrentOrchestration
from semantic_kernel.agents.runtime import InProcessRuntime
from semantic_kernel.connectors.ai.open_ai import AzureChatCompletion
#from semantic_kernel.memory.azure_cognitive_search import AzureCognitiveSearchMemoryStore
import os
from dotenv import load_dotenv
load_dotenv()

# Configuration (use environment variables for security)
AZURE_OPENAI_ENDPOINT = os.getenv("AZURE_OPENAI_ENDPOINT")
AZURE_OPENAI_KEY = os.getenv("AZURE_OPENAI_KEY")
AZURE_OPENAI_DEPLOYMENT = os.getenv("AZURE_OPENAI_DEPLOYMENT")
AZURE_SEARCH_ENDPOINT = os.getenv("AZURE_SEARCH_ENDPOINT")
AZURE_SEARCH_KEY = os.getenv("AZURE_SEARCH_KEY")
AZURE_SEARCH_INDEX = os.getenv("AZURE_SEARCH_INDEX")

# Logging setup
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class SemanticKernelAgent:
    # def __init__(self, agent_name: str):
    #     self.agent_name = agent_name
    #     try:
    #         self.kernel = Kernel()
    #         self.kernel.add_service(
    #             AzureChatCompletion(
    #                 endpoint=AZURE_OPENAI_ENDPOINT,
    #                 api_key=AZURE_OPENAI_KEY,
    #                 deployment_name=AZURE_OPENAI_DEPLOYMENT
    #             )
    #         )
    #         self.agent = ChatCompletionAgent(
    #                 kernel= self.kernel,
    #                 name=agent_name,
    #                 instructions="Answer the user's questions.",
    #         )

    #         logger.info(f"Semantic Kernel initialized for agent {agent_name}.")
    #     except Exception as e:
    #         logger.error(f"Failed to initialize Semantic Kernel: {e}")
    #         self.kernel = None

    def get_agents(self) -> list[Agent]:
        """Return a list of agents that will participate in the concurrent orchestration.

        Feel free to add or remove agents.
        """
        physics_agent = ChatCompletionAgent(
            name="PhysicsExpert",
            instructions="You are an expert in physics. You answer questions from a physics perspective.",
            service=AzureChatCompletion(
                    endpoint=AZURE_OPENAI_ENDPOINT,
                    api_key=AZURE_OPENAI_KEY,
                    deployment_name=AZURE_OPENAI_DEPLOYMENT
                ),
        )

        chemistry_agent = ChatCompletionAgent(
            name="ChemistryExpert",
            instructions="You are an expert in chemistry. You answer questions from a chemistry perspective.",
            service=AzureChatCompletion(
                    endpoint=AZURE_OPENAI_ENDPOINT,
                    api_key=AZURE_OPENAI_KEY,
                    deployment_name=AZURE_OPENAI_DEPLOYMENT
                ),
        )

        return [physics_agent, chemistry_agent]

    async def chat(self, user: str, message: str):
        # if not self.kernel:
        #     raise RuntimeError("Kernel not initialized.")
        # try:
        #     response = await self.agent.get_response(messages=message)
        #     return response.content
        # except Exception as e:
        #     logger.error(f"Chat error: {e}")
        #     raise
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
    