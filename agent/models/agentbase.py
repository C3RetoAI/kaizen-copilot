from abc import ABC, abstractmethod
from typing import Generic, Optional, Tuple
from agent.models.context import Context
from agent.models.input import InT, InputBase
from agent.models.mcpstep import ROLE
from agent.models.output import OutT, OutputBase
from agent.tools.tool import Tool

class AgentBase(ABC, Generic[InT, OutT]): 
    def __init__(self):
        self.agent_name: str = ""
        self.role: ROLE = None
        self.agent_input: InputBase = None
        self.output: OutputBase = None
        self.tool: Optional[Tool] = None
        self.context: Context = None
        self.purpose: str = ""

    @abstractmethod
    def run(self, input_data: InT, context: Context) -> Tuple[OutT, Context, int]:
        pass