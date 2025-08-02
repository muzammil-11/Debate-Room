# app.py

from state import GraphState
from agents import create_debater_agent

# Create proposition agent with a specific persona
proposition_agent = create_debater_agent(
    "You are a confident proposition debater who argues in favor of the given topic. "
    "Your primary goal is to first address and rebut the opponent's last point, then "
    "present your own compelling arguments supported by evidence and logical reasoning. "
    "Be assertive, use credible sources, and maintain a professional yet persuasive tone."
)


def proposition_node(state: GraphState) -> dict:
    """
    Node function for the proposition debater in the debate graph.
    
    This function handles the proposition side's turn in the debate by:
    1. Invoking the proposition agent with current context
    2. Processing the agent's response
    3. Updating the debate state with the new argument
    4. Incrementing the turn counter
    
    Args:
        state (GraphState): Current state containing topic, debate_history, 
                           turn_number, and other debate metadata
    
    Returns:
        dict: Updated state with new debate_history entry and incremented turn_number
    """
    # Format debate history for the agent
    formatted_history = "\n".join([
        f"Turn {i+1}:\n{speaker}: {argument}\n"
        for i, (speaker, argument) in enumerate(state["debate_history"])
    ]) if state["debate_history"] else "No previous arguments."
    
    # Invoke the proposition agent with current topic and debate history
    response = proposition_agent.invoke({
        "topic": state["topic"],
        "debate_history": formatted_history
    })
    
    # Extract the agent's response text
    agent_response = response["output"]
    
    # Create updated debate history with new proposition argument
    updated_debate_history = state["debate_history"].copy()
    updated_debate_history.append(("Proposition", agent_response))
    
    # Increment turn number
    updated_turn_number = state["turn_number"] + 1
    
    # Return dictionary with updated state fields
    return {
        "debate_history": updated_debate_history,
        "turn_number": updated_turn_number
    }


def should_continue(state: GraphState) -> str:
    """
    Determines whether the debate should continue or proceed to judging.
    
    This function acts as a conditional router in the debate graph workflow,
    checking if the maximum number of turns has been exceeded and directing
    the flow accordingly.
    
    Args:
        state (GraphState): Current debate state containing turn_number and max_turns
    
    Returns:
        str: "judge" if turn_number > max_turns, indicating the debate should end
             and proceed to judging; "proposition" if the debate should continue
             with the next proposition argument
    """
    if state["turn_number"] > state["max_turns"]:
        return "judge"
    else:
        return "proposition"