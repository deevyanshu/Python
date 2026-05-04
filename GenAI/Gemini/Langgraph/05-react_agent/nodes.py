from dotenv import load_dotenv
from react_state import AgentState
from agent_reason_runnable import agent, tools

load_dotenv()

def reason_node(state: AgentState):
    try:
        agent_outcome = agent.invoke(state)
        return {"agent_outcome": agent_outcome}
    except Exception as e:
        # If Gemini returns an empty message that crashes the parser, 
        # this catch helps you see what's actually happening.
        print(f"Error in reason_node: {e}")
        raise e


def act_node(state:AgentState):
    agent_action = state["agent_outcome"]
    
    # Extract tool name and input from AgentAction
    tool_name = agent_action.tool
    tool_input = agent_action.tool_input
    
    # Find the matching tool function
    tool_function = None
    for tool in tools:
        if tool.name == tool_name:
            tool_function = tool
            break
    
    # Execute the tool with the input
    if tool_function:
        if isinstance(tool_input, dict):
            output = tool_function.invoke(**tool_input)
        else:
            output = tool_function.invoke(tool_input)
    else:
        output = f"Tool '{tool_name}' not found"
    
    return {"intermediate_steps": [(agent_action, str(output))]}