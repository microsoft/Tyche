

class AgentConfig:
    def __init__(self, name, description, instructions, index_name=None):
        self.name = name
        self.description = description
        self.instructions = instructions
        self.index_name = index_name

# List of agent configs
AGENTS = [
    AgentConfig(
        name="AccountOwner",
        description="Account owner finder",
        instructions="You can get access to the employee account owner and customers that they manage data. Answer only questions found in the account-owner index.",
        index_name="account-owner"
    ),
    AgentConfig(
        name="NBA_Threshold",
        description="Next Best Action threshold analysis agent",
        instructions="""
            NBA means Next Best Action.
            You are an analyst that will examine the data to determine the next best action for the customer. Retrieve information from the threshold index.
            """,
        index_name="threshold"
    ),
    AgentConfig(
        name="ActionReviewer",
        description="Action review agent",
        instructions="""
            You are a reviewer that will examine the information provided by the other agents and determine if it answers the query.
            If the answer to the question is not found, verify that all agents have provided their answers.
            """,
        index_name=None
    ),
   
]
