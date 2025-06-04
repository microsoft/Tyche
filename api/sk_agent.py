import os
import logging
from semantic_kernel import Kernel
from semantic_kernel.agents import Agent, ChatCompletionAgent, GroupChatOrchestration, RoundRobinGroupChatManager
from semantic_kernel.agents.runtime import InProcessRuntime
from semantic_kernel.connectors.ai.open_ai import AzureChatCompletion

from .chat_manager import ChatCompletionGroupChatManager
from .threshold_plugin import VectorSearchPlugin
from semantic_kernel.contents import ChatMessageContent
from .agents_config import AGENTS

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

    def create_agent(self, name: str, description: str, instructions: str, index_name: str = None) -> ChatCompletionAgent:
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
            description=description,
            instructions=instructions,
            kernel=kernel,
            service=AzureChatCompletion(
                endpoint=AZURE_OPENAI_ENDPOINT,
                api_key=AZURE_OPENAI_KEY,
                deployment_name=AZURE_OPENAI_DEPLOYMENT
            ),
        )
    
    def agent_response_callback(self, message: ChatMessageContent) -> None:
        """Observer function to print the messages from the agents."""
        print(f"**{message.name}**\n{message.content}")
    
    async def chat(self, user: str, message: str):
        agents = [self.create_agent(agent_cfg.name, agent_cfg.description, agent_cfg.instructions, agent_cfg.index_name) for agent_cfg in AGENTS]

        # group_chat_orchestration = GroupChatOrchestration(
        #     members=agents,
        #     manager=RoundRobinGroupChatManager(max_rounds=5),
        #     agent_response_callback=self.agent_response_callback,
        # )
        group_chat_orchestration = GroupChatOrchestration(
            members=agents,
            manager=ChatCompletionGroupChatManager(
                topic=message,
                service=AzureChatCompletion(
                    endpoint=AZURE_OPENAI_ENDPOINT,
                    api_key=AZURE_OPENAI_KEY,
                    deployment_name=AZURE_OPENAI_DEPLOYMENT
                ),
                max_rounds=10,
            ),
            agent_response_callback=self.agent_response_callback,
        )
        runtime = InProcessRuntime()
        runtime.start()

        orchestration_result = await group_chat_orchestration.invoke(
            task=message,
            runtime=runtime,
        )

        value = await orchestration_result.get()
        # results = []
        # for item in value:
        #     results.append({"agent": item.name, "answer": item.content})

        await runtime.stop_when_idle()
        return value#.items[0].text
