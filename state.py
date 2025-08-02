# state.py

from typing import TypedDict, List, Tuple


class GraphState(TypedDict):
    """
    Represents the state of a debate graph workflow.
    
    This TypedDict defines the structure of the state that flows through
    the debate graph, tracking the progress and content of a debate between
    two participants.
    
    Attributes:
        topic (str): The main subject or question being debated. This defines
            what the participants will be arguing about.
            
        debate_history (List[Tuple[str, str]]): A chronological record of the
            debate exchanges. Each tuple contains two strings representing
            a round of debate: the first string is the argument from one
            participant, and the second string is the counter-argument from
            the other participant.
            
        turn_number (int): The current turn or round number in the debate.
            Starts at 0 and increments after each exchange. Used to track
            progress and enforce turn limits.
            
        winner (str): The declared winner of the debate. This field is empty
            during the debate and gets populated when the debate concludes,
            either by reaching max_turns or through other termination criteria.
            
        max_turns (int): The maximum number of turns allowed in the debate.
            This serves as a termination condition to prevent infinite debates
            and ensure the conversation reaches a conclusion within a reasonable
            timeframe.
    """
    topic: str
    debate_history: List[Tuple[str, str]]
    turn_number: int
    winner: str
    max_turns: int